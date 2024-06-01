# Start
1. On start example config will be created automaticly!

How to install and start app:
```bash
python3 -m venv en
. ./env/bin/activate
pip install -r requirements.txt
python3 main.py ./config.json
```

# Config 
if you dont want to use some filters leave it empty

```json
{
    "filters": {
        "title": [ # All titles with this words will be aded to db
            "Hacker",
            "Ukraine",
            "Currency"
        ],
        "text": [ # Search keywords from text
            ""
        ],
        "authors": [ # Specify the authors from whom you want to receive news
            ""
        ],
        "time": "2024-05-30 - 2024-06-30", # Set the time period when the Article was created
        "publisher": "", # Get articles from a specific publisher
        "source": "us.FoxNews" # Choose two letters by region and put the publisher through a dot. If you want to collect data from all publishers, specify only 2 letters of the region
    },
    "db": "articles.db" # DB path
}               

```

Sources Table - https://github.com/flairNLP/fundus/blob/master/docs/supported_publishers.md



