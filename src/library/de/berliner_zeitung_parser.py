import datetime
from typing import List, Optional

from lxml.cssselect import CSSSelector
from lxml.etree import XPath

from src.parser.html_parser import ArticleBody, BaseParser, attribute
from src.parser.html_parser.utility import (
    extract_article_body_with_selector,
    extract_article_body_with_selector_precompiled,
    generic_author_parsing,
    generic_date_parsing,
    generic_topic_parsing,
)


class BerlinerZeitungParser(BaseParser):
    @attribute
    def body(self) -> ArticleBody:
        selector = CSSSelector("div[id=articleBody] > p")
        summary_selector = CSSSelector("div[id=articleBody] > p")
        subheadline_selector = CSSSelector("div[id=articleBody] > h2")
        return extract_article_body_with_selector_precompiled(
            self.precomputed.doc,
            paragraph_selector=selector,
            subheadline_selector=subheadline_selector,
            summary_selector=summary_selector,
        )

    @attribute
    def title(self) -> Optional[str]:
        return self.precomputed.meta.get("og:title")

    @attribute
    def authors(self) -> List[str]:
        return generic_author_parsing(self.precomputed.meta.get("article:author"))

    @attribute
    def publishing_date(self) -> Optional[datetime.datetime]:
        return generic_date_parsing(self.precomputed.ld.bf_search("datePublished"))

    @attribute
    def topics(self) -> List[str]:
        return generic_topic_parsing(self.precomputed.ld.bf_search("keywords"))
