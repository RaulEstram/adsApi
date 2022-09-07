import json

default_locale = "queries"
cached_queries = {}


def refresh():
    global cached_queries
    with open(f"strings/{default_locale}.json") as file:
        cached_queries = json.load(file)


def getQuery(name):
    return cached_queries[name]


refresh()
