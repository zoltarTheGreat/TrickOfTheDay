import requests
from bs4 import BeautifulSoup
import yaml
import urllib.parse
import re
import time

INPUT_FILE = "tricks.txt"
OUTPUT_FILE = "tricks.yaml"

def load_tricks_txt():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tricks = [line.strip() for line in f if line.strip()]
    return tricks

def scrape_skate_fandom(trick_name):
    """Scrape skateboarding.fandom.com for trick info."""
    base_url = "https://skateboarding.fandom.com/wiki/"
    url = base_url + urllib.parse.quote(trick_name.replace(" ", "_"))
    info = {"description": "Unknown", "invented_by": "Unknown", "year": "Unknown"}

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return info  # page not found

        soup = BeautifulSoup(r.text, "html.parser")

        # Grab the first paragraph for description
        para = soup.select_one("div.mw-parser-output > p")
        if para and para.get_text(strip=True):
            info["description"] = para.get_text(strip=True)

        # Look for "invented by" or "invented in"
        text = soup.get_text(" ", strip=True)
        lower_text = text.lower()

        if "invented" in lower_text:
            idx = lower_text.find("invented")
            snippet = text[idx:idx+200]
            info["invented_by"] = snippet

        # Try to extract a year
        years = re.findall(r"(19\d{2}|20\d{2})", text)
        if years:
            info["year"] = years[0]

    except Exception:
        pass

    return info

def generate_yaml(tricks, scrape=True):
    data = []
    for i, trick in enumerate(tricks, start=1):
        if scrape:
            fandom_info = scrape_skate_fandom(trick)
        else:
            fandom_info = {"description": "Unknown", "invented_by": "Unknown", "year": "Unknown"}

        entry = {
            "name": trick,
            "description": fandom_info["description"],
            "video": f"https://www.youtube.com/results?search_query=how+to+{urllib.parse.quote(trick)}+skateboarding",
            "invented_by": fandom_info["invented_by"],
            "year": fandom_info["year"]
        }
        data.append(entry)

        print(f"[{i}/{len(tricks)}] Processed: {trick}")

        # Pause to avoid hammering fandom too fast
        if scrape:
            time.sleep(1)

    return data

def save_yaml(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":
    tricks = load_tricks_txt()
    data = generate_yaml(tricks, scrape=True)  # set scrape=False for fast placeholder mode
    save_yaml(data)
    print(f"Generated {OUTPUT_FILE} with {len(tricks)} tricks.")
