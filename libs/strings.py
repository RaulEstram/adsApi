import json

default_locale = "es-mx"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json", encoding='utf-8') as file:
        cached_strings = json.load(file)



def getText(name):
    return cached_strings[name]


refresh()
