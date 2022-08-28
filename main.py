import json
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    token = "TnEWAPDi8n5R3taijqXleJDTZ5LNDr2LMJjOOsec"
    results = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?q=docs(06491901cc391f1930e6b5e79207efdb)&rows=50&fl=id, first_author,date,doi,bibcode,author,title&sort=date desc",
        headers={'Authorization': 'Bearer ' + token})

    data = results.json()
    return json.dumps(data)

if __name__ == "__main__":
    app.run()