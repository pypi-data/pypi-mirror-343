from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Annotated, Optional, Sequence
from urllib.parse import urlparse

import httpx
from kgdata.wikipedia.models.linked_html_table import LinkedHTMLTable
from libactor.actor import Actor
from libactor.cache import BackendFactory, IdentObj, cache
from loguru import logger
from rsoup.core import ContextExtractor, Document, TableExtractor
from sm.dataset import FullTable
from tqdm import tqdm


@dataclass
class TableScraperArgs:
    max_num_hop: int = field(
        default=0,
        metadata={
            "help": "Max number of hops to follow. 0 means we do not follow any links, 1 means we follow only the links on the page, etc."
        },
    )
    max_num_links: int = field(
        default=1000, metadata={"help": "Max number of links to follow."}
    )
    only_follow_same_domain: bool = field(
        default=True,
        metadata={"help": "Whether to only follow links on the same domain."},
    )


URL = Annotated[str, "Http URL"]


class TableScraperActor(Actor[TableScraperArgs]):
    VERSION = 101

    def __init__(
        self, params: TableScraperArgs, dep_actors: Optional[Sequence[Actor]] = None
    ):
        super().__init__(params, dep_actors=dep_actors)
        self.table_extractor = TableExtractor(
            context_extractor=ContextExtractor(), html_error_forgiveness=True
        )

    @cache(
        backend=BackendFactory.actor.sqlite.pickle(mem_persist=True),
    )
    def forward(self, url: URL) -> Sequence[IdentObj[FullTable]]:
        queue = deque([(0, url)])
        output = []
        visited_urls = {url}

        domain = urlparse(url).netloc

        with tqdm(desc="Scraping", total=len(visited_urls)) as pbar:
            while len(queue) > 0:
                hop, url = queue.popleft()
                pbar.total = len(visited_urls)
                pbar.update(1)

                # extract HTML from the current URL
                html = self.get_html(url)

                # extract tables
                output += self.extract_table(url)

                # do not follow links if we have reached the max number of hops or the max number of links
                if (
                    hop >= self.params.max_num_hop
                    or len(visited_urls) >= self.params.max_num_links
                ):
                    continue
                doc = Document(url, html)
                for a in doc.select("a"):
                    href = a.attr("href")
                    if href.startswith("#"):
                        # local url
                        continue

                    if href.startswith("/"):
                        # domain-relative url
                        href = f"{domain}{href}"
                    elif not (href.startswith("http") or href.startswith("https")):
                        if url.endswith("/"):
                            href = f"{url}{href}"
                        else:
                            href = f"{url}/{href}"

                    if self.params.only_follow_same_domain:
                        if urlparse(href).netloc != domain:
                            continue

                    if href in visited_urls:
                        continue

                    visited_urls.add(href)
                    queue.append((hop + 1, href))

                    if len(visited_urls) >= self.params.max_num_links:
                        break

        return output

    @cache(
        backend=BackendFactory.actor.sqlite.pickle(mem_persist=True),
    )
    def get_html(self, url: URL) -> str:
        return httpx.get(url, follow_redirects=True).raise_for_status().text

    def extract_table(self, url: URL) -> Sequence[IdentObj[FullTable]]:
        try:
            tables = self.table_extractor.extract(
                url,
                self.get_html(url),
                auto_span=True,
                auto_pad=True,
                extract_context=True,
            )
        except Exception as e:
            logger.error(
                "Error while extracting tables from webpage: {}",
                url,
            )
            raise
        return [
            IdentObj(
                key=tbl.id,
                value=LinkedHTMLTable(tbl, {}, page_wikidata_id=None).to_full_table(),
            )
            for tbl in tables
        ]
