import signal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from fundus import PublisherCollection, Crawler
from typing import Dict, Any
import datetime
from filter import Filters, get_text
from db import ArticleDatabase
import json
    

class Fundus ():
    def __init__(self, Fileters, db: ArticleDatabase):
        self.crawler = Crawler
        self.Filters = filters
        self.db = db
    def start(self):
        self.crawler = Crawler(self.Filters.source)
        for article in self.crawler.crawl():
            # print(article.html.source_info.publisher)
            if self.Filters.filter(article):
                self.db.insert_article_data(article=article)
                print("Added new article to DB:", article.title)
            # print(article.html.source_info.publisher)


    def shutdown_handler(self, signum, frame):
        print("Received signal {}, shutting down...".format(signum))
        self.db.disconnect()
        sys.exit(0)


def create_config(config_path):
    config = {
        "filters": {
            "title": ["Hacker", "Ukraine", "Currency"],
            "text": [""],
            "authors": [""],
            "time": "2024-05-30 - 2024-06-30",
            "publisher": "",
            "source": "us.FoxNews"
        },
        "db": "articles.db"
    }

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def read_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: main.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]

    if not os.path.exists(config_path):
        print(f"Configuration file {config_path} does not exist. Creating default configuration.")
        create_config(config_path)
        print(f"Configuration saved to {config_path}")
    
    cfg = read_config(config_path=config_path)

    # # print(cfg.title)
    # print(cfg["filters"]["title"])

    
    filters = Filters(
        cfg["filters"]["title"], # Title
        cfg["filters"]["text"], # Text
        cfg["filters"]["authors"], # Autrors
        cfg["filters"]["time"], # time 2024-05-30 - 2024-06-30
        publisher=cfg["filters"]["publisher"], # Fox News or etc....
        source=eval("PublisherCollection."+cfg["filters"]["source"]) # Collector of news
    )

    db = ArticleDatabase(cfg["db"])
    db.connect()
    db.create_table()

    f = Fundus(Fileters=filters, db=db)

    print("Starting...")
    signal.signal(signal.SIGINT, f.shutdown_handler)
    signal.signal(signal.SIGTERM, f.shutdown_handler)
    f.start()
    