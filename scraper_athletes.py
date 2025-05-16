import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote

URL = "https://olympics-statistics.com"
ATH_PAGE = "/olympic-athletes"
JSON_SORTIE = "athletes.json"

MEDAILLE = {'1': 'gold', '2': 'silver', '3': 'bronze'}

def get_letter_urls():
    r = requests.get(urljoin(URL, ATH_PAGE))
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return [
        urljoin(URL, a["href"])
        for a in soup.select('div.alpha a[href^="/olympic-athletes/"]')
    ]

def fetch_athlete_detail(card):
    first = card.select_one(".vn").get_text(strip=True)
    last = card.select_one(".nn").get_text(strip=True)
    raw_url = urljoin(URL, card["href"])
    parsed = urlparse(raw_url)
    encoded_path = quote(parsed.path, safe='/')
    detail_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"

    try:
        r = requests.get(detail_url, timeout=10)
        r.raise_for_status()
        dsoup = BeautifulSoup(r.text, "html.parser")

        flag = dsoup.select_one("img.f")
        country = flag["title"] if flag and flag.has_attr("title") else None

        pal = []
        for med in dsoup.select("div.medaille.visible"):
            code = med.select_one("div.the-medal")["data-medal"]
            pal.append({
                "medal": MEDAILLE.get(code, "unknown"),
                "sport": med.select_one("div.m-sport").get_text(strip=True),
                "event": med.select_one("a.m-event .m-eventname").get_text(strip=True),
                "date": med.select_one("a.m-event .m-event-am")
                              .get_text(strip=True)
                              .replace("on ", "")
            })

        return {
            "first_name": first,
            "last_name": last,
            "country": country,
            "palmares": pal
        }
    except Exception as e:
        return {
            "first_name": first,
            "last_name": last,
            "country": None,
            "palmares": [],
            "error": str(e)
        }

def scrape_all_athletes():
    letter_urls = get_letter_urls()

    cards = []
    for url in letter_urls:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        cards.extend(soup.select("a.card.athlet.visible"))

    total = len(cards)
    print(f"Total athletes to fetch: {total}")

    results = []
    for idx, card in enumerate(cards, 1):
        athlete = fetch_athlete_detail(card)
        results.append(athlete)
        print(f"{idx}/{total}")

    with open(JSON_SORTIE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Done: {len(results)} athletes saved to {JSON_SORTIE}")

if __name__ == "__main__":
    scrape_all_athletes()