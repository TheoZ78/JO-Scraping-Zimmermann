import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://olympics-statistics.com"
SPORTS_PAGE  = "/olympic-sports"
JSON_SORTIE  = "sports.json"
MEDAILLE = {"1": "gold", "2": "silver", "3": "bronze"}

def get_all_sports():
    r = requests.get(urljoin(URL, SPORTS_PAGE))
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    sports = []
    for a in soup.select("a.card.sport.visible"):
        name = a.select_one("div.bez").text.strip()
        href = a["href"]
        sports.append({
            "sport": name,
            "url":   urljoin(URL, href)
        })
    return sports

def get_medals_by_country(sport_url):
    r = requests.get(sport_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    top_n = soup.select_one('div.top[data-which="n"]')
    if not top_n:
        return []

    cards = top_n.select("div.card.nation.visible")
    result = []
    for c in cards:
        img = c.select_one("img.f")
        country = img["title"].strip() if img and img.has_attr("title") else None
        counts = {"gold":0, "silver":0, "bronze":0}
        for medal_div in c.select("div.medals div.the-medal"):
            code = medal_div["data-medal"]
            parent = medal_div.parent
            qty = int(parent.select_one("span.mal").text.strip())
            key = MEDAILLE.get(code, None)
            if key:
                counts[key] = qty
        result.append({
            "country": country,
            **counts
        })
    return result

def main():
    sports = get_all_sports()
    output = []

    for idx, sp in enumerate(sports, 1):
        print(f"{sp['sport']}")
        medals = get_medals_by_country(sp["url"])
        output.append({
            "sport": sp["sport"],
            "medals_by_country": medals
        })

    with open(JSON_SORTIE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
