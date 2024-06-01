import sqlite3
from filter import get_text
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))



from fundus.scraping.article import Article

class ArticleDatabase:
    def __init__(self, db_name='articles.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        if self.conn:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS articles
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT, authors TEXT, publishing_date DATE, publisher TEXT)''')
            self.conn.commit()
        else:
            print("Connection to database not established.")

    def insert_article_data(self, article: Article):
        try:
            if not self.conn:
                self.connect()
            c = self.conn.cursor()
            c.execute("INSERT INTO articles (title, body, authors, publishing_date, publisher) VALUES (?, ?, ?, ?, ?)",
                    (article.title, get_text(article.body), ', '.join(article.authors), article.publishing_date, article.html.source_info.publisher))
            self.conn.commit()
            # print("Article inserted successfully.")
        except Exception as e:
            print("Error inserting article:", e)
