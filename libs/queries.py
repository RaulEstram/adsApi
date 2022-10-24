import json

default_locale = "queries"
cached_queries = {}


def refresh():
    global cached_queries
    with open(f"/var/www/html/apiAds/strings/{default_locale}.json", encoding='utf-8') as file:
        cached_queries = json.load(file)


def getQuery(name):
    return cached_queries[name]


refresh()
