import datetime
from bs4 import BeautifulSoup
import requests
from es import index


def get_alerts():
    url = "http://www.healthmap.org/getAlerts.php"

    querystring = {"locations": "", "diseases": "", "sources": "", "species": "", "category%5B%5D": ["1", "2", "29"], "vaccines": "", "time_interval": "1 week",
                   "zoom_lat": "15.000000", "zoom_lon": "18.000000", "zoom_level": "2", "displayapi": "", "heatscore": "1", "partner": "hm"}

    response = requests.request("GET", url, params=querystring)
    response = response.json()
    items = []

    for lv in response.get('listview'):
        source = lv[0]
        tag = BeautifulSoup(source, "html.parser")
        source_name = tag.find("img").get('title')

        date = lv[1]
        date_object = datetime.datetime.strptime(date, "%d %b %Y")

        summary = lv[2]
        tag = BeautifulSoup(summary, "html.parser")
        url_context = tag.find("a").get("href").split("?")[1]
        hm_link = "http://www.healthmap.org/ai.php?" + url_context
        article_link = "http://www.healthmap.org/ln.php?" + url_context.split("&")[0]
        hm_id = url_context.split("&")[0]
        summary_text = tag.find("a").getText()

        desease = lv[3]

        location = lv[4]
        tag = BeautifulSoup(location, "html.parser")
        location_name = tag.find("a").getText()
        location_parts = location.split("'")
        location_object = {"lat": float(location_parts[1]), "lon": float(location_parts[3])}

        species = lv[5]

        cases_count = None
        if lv[6]:
            cases_count = int(lv[6])

        deaths_count = None
        if lv[7]:
            deaths_count = int(lv[7])

        significance = lv[8]
        tag = BeautifulSoup(lv[8], "html.parser")
        significance_score = int(tag.findAll("span")[1].getText())

        item = {
            "source": source_name,
            "@timestamp": date_object.strftime("%Y-%m-%d"),
            "summary": summary_text,
            "desease": desease,
            "location_name": location_name,
            "location": location_object,
            "species": species,
            "deaths": deaths_count,
            "cases": cases_count,
            "significance_score": significance_score,
            "link": hm_link,
            "article_link": article_link,
            "id": hm_id
        }

        items.append(item)

    return items


if __name__ == '__main__':
    items = get_alerts()
    for item in items:
        index("alert", item)