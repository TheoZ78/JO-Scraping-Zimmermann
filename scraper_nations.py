import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://olympics-statistics.com"
NATIONS_PAGE = "/nations"
JSON_SORTIE = "nations.json"
MEDAILLE = {"1": "gold", "2": "silver", "3": "bronze"}

def load_soup_from_file(path):
    with open(path, encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def get_countries(soup):
    countries = []
    for a in soup.select("a.card.nation.visible"):
        name = a.select_one("div.bez").get_text(strip=True)
        href = a["href"]
        url = urljoin(URL, href)
        countries.append((name, url))
    return countries

def get_medal_counts(country_url):
    r = requests.get(country_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    counts = {"gold": 0, "silver": 0, "bronze": 0}
    teaser = soup.select_one(".rnd.teaser")
    if teaser:
        for cell in teaser.select("div:has(div.the-medal)"):
            medal_code = cell.select_one("div.the-medal")["data-medal"]
            qty = int(cell.select_one("span.mal").get_text(strip=True))
            counts[MEDAILLE[medal_code]] = qty
    return counts

def main():
    soup = load_soup_from_file(NATIONS_PAGE)
    countries = get_countries(soup)

    result = []
    for name, url in countries:
        counts = get_medal_counts(url)
        entry = {"country": name, **counts}
        result.append(entry)
        print(f"{name}: {counts}")

    with open(JSON_SORTIE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
