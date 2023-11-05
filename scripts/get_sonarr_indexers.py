import os
import requests
import xml.etree.ElementTree as ET

JACKETT_API_KEY = os.environ.get("JACKETT_API_KEY", None)
SONARR_API_KEY = os.environ.get("SONARR_API_KEY", None)

if JACKETT_API_KEY is None:
    raise RuntimeError("JACKETT_API_KEY is required")
if SONARR_API_KEY is None:
    raise RuntimeError("SONARR_API_KEY is required")

jackett_url = f"http://127.0.0.1:9117/api/v2.0/indexers/all/results/torznab?t=indexers&configured=true&apikey={JACKETT_API_KEY}"
resp = requests.get(jackett_url, headers={"Accept": "application/json"})

if resp.status_code == 200:
    with open("indexers.xml", "w+") as out:
        out.write(resp.content.decode())
else:
    print(f"Received resp status {resp.status_code}")
    print(resp.content)

tree = ET.parse('indexers.xml')
root = tree.getroot()
for indexer in root:
    print(indexer.attrib.get("id"))
    print(indexer.find("title").text)

    indexer = {
        "enableRss": True,
        "enableAutomaticSearch": True,
        "enableInteractiveSearch": True,
        "supportsRss": True,
        "supportsSearch": True,
        "protocol": "torrent",
        "priority": 25,
        "downloadClientId": 0,
        "name": indexer.find("title").text,
        "fields": [
            {
                "order": 0,
                "name": "baseUrl",
                "label": "URL",
                "value": f"http://jackett:9117/api/v2.0/indexers/{indexer.attrib.get('id')}/results/torznab/",
                "type": "textbox",
                "advanced": False
            },
            {
                "order": 1,
                "name": "apiPath",
                "label": "API Path",
                "helpText": "Path to the api, usually /api",
                "value": "/api",
                "type": "textbox",
                "advanced": True
            },
            {
                "order": 2,
                "name": "apiKey",
                "label": "API Key",
                "value": JACKETT_API_KEY,
                "type": "textbox",
                "advanced": False
            },
            {
                "order": 3,
                "name": "categories",
                "label": "Categories",
                "helpText": "Drop down list, leave blank to disable standard/daily shows",
                "value": [
                    id.attrib.get("id") for id in indexer.find("caps").find("categories").findall("category")
                ],
                "type": "select",
                "advanced": False,
                "selectOptionsProviderAction": "newznabCategories"
            },
            {
                "order": 4,
                "name": "animeCategories",
                "label": "Anime Categories",
                "helpText": "Drop down list, leave blank to disable anime",
                "value": [],
                "type": "select",
                "advanced": False,
                "selectOptionsProviderAction": "newznabCategories"
            },
            {
                "order": 5,
                "name": "animeStandardFormatSearch",
                "label": "Anime Standard Format Search",
                "helpText": "Also search for anime using the standard numbering",
                "value": False,
                "type": "checkbox",
                "advanced": False
            },
            {
                "order": 6,
                "name": "additionalParameters",
                "label": "Additional Parameters",
                "helpText": "Additional Newznab parameters",
                "type": "textbox",
                "advanced": True
            },
            {
                "order": 7,
                "name": "minimumSeeders",
                "label": "Minimum Seeders",
                "helpText": "Minimum number of seeders required.",
                "value": 1,
                "type": "number",
                "advanced": True
            },
            {
                "order": 8,
                "name": "seedCriteria.seedRatio",
                "label": "Seed Ratio",
                "helpText": "The ratio a torrent should reach before stopping, empty is download client's default",
                "type": "textbox",
                "advanced": True
            },
            {
                "order": 9,
                "name": "seedCriteria.seedTime",
                "label": "Seed Time",
                "unit": "minutes",
                "helpText": "The time a torrent should be seeded before stopping, empty is download client's default",
                "type": "number",
                "advanced": True
            },
            {
                "order": 10,
                "name": "seedCriteria.seasonPackSeedTime",
                "label": "Season-Pack Seed Time",
                "unit": "minutes",
                "helpText": "The time a torrent should be seeded before stopping, empty is download client's default",
                "type": "number",
                "advanced": True
            }
        ],
        "implementationName": "Torznab",
        "implementation": "Torznab",
        "configContract": "TorznabSettings",
        "infoLink": "https://wiki.servarr.com/sonarr/supported#torznab",
        "tags": [],
    }

    resp = requests.post("http://127.0.0.1:8989/api/v3/indexer", json=indexer, headers={"authorization": SONARR_API_KEY})
    print(resp.status_code)
    print(resp.content)