from typing import List, Any
import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))



from fundus.scraping.article import Article
from fundus import PublisherCollection
from fundus.parser.data import ArticleBody


def get_text(article_body: ArticleBody) -> str:
    text = str(article_body.summary)  # Convert summary to string
    for section in article_body.sections:
        text += str(section)  # Convert section to string and concatenate
    return text

class Filters:
    def __init__(self, title: List[str], text: List[str], author, time: str, publisher: str, source: List[str]) -> None:
        self.title = title
        self.text = text
        self.author = author
        self.time = time
        self.publisher = publisher
        self.source = source

    def title_filter(self, article: Article) -> bool:
        if not self.title:
            return True
        if self.title and (title := article.title):
            for t in self.title:
                if t.lower() in title.lower():
                    return True
        # print("Title filter did not match")
        return False

    def text_filter(self, article: Article) -> bool:
        if not self.text:
            return True
        if self.text and (text := article.body):
            for t in self.text:
                if t.lower() in get_text(text).lower():
                    return True
        # print("Text filter did not match")
        return False

    def author_filter(self, article: Article) -> bool:
        if not self.author:
            return True
        if isinstance(self.author, str):  # Check if author is a string
            authors = [self.author]  # Convert it to a list for consistency
        else:
            authors = self.author  # Otherwise, assume it's already a list
        for single_author in authors:
            if article.authors:
                for author in article.authors:
                    if single_author.lower() in author.lower():
                        return True
        # print("Author filter did not match")
        return False

    def time_filter(self, article: Article) -> bool:
        if not self.time:
            return True
        if self.time and (publication_date := article.publishing_date):
            start_date_str, end_date_str = self.time.split(" - ")
            start_date = datetime.datetime.strptime(start_date_str.strip(), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date_str.strip(), "%Y-%m-%d")
            # Convert publication_date to string and then to datetime object without timezone info
            pub_date = datetime.datetime.strptime(str(publication_date)[:10], "%Y-%m-%d")
            if start_date <= pub_date <= end_date:
                return True
        return False

    def source_filter(self, article: Article) -> bool:
        if not self.publisher:
            return True
        if news_outlet := article.html.source_info.publisher:
            if news_outlet in self.publisher:
                return True
        # print("Source filter did not match")
        return False

    def filter(self, article: Article) -> bool:
        return all([
            self.title_filter(article),
            self.text_filter(article),
            self.author_filter(article),
            self.time_filter(article),
            self.source_filter(article)
        ])

# Example usage of filters
if __name__ == "__main__":
    filters = Filters(
        title="usa",
        text="",
        author="bbc",
        time="2024-04-01 - 2024-05-01",
        publisher="BBC",
        source=PublisherCollection.us
    )

    # Example extracted data
    example_article = Article(
        title="USA Today",
        body="Sample text content.",
        authors=["BBC Reporter", "Another Author"],
        publishing_date="2024-04-15 13:57:11+00:00",
    )

    # Apply filters
    result = filters.filter(example_article)
    print("All filters passed:", result)
