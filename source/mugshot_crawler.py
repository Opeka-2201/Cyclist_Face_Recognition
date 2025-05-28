import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import os
import time
from tqdm import tqdm  # type: ignore

BASE_URL = "https://www.procyclingstats.com"
TEAMS_URL = f"{BASE_URL}/teams"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_team_links():
    resp = requests.get(TEAMS_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.select("a[href^='team/']"):
        href = a.get("href")
        if href and "team/" in href and href not in links:
            links.append(href)

    return [BASE_URL + "/" + link for link in links]


def get_rider_links(team_url):
    resp = requests.get(team_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.select("a[href^='rider/']"):
        href = a.get("href")
        if href and "rider/" in href and href not in links:
            links.append(href)

    print(f"Found {len(links)} riders in team: {team_url}")
    return [BASE_URL + "/" + link for link in links]


def get_mugshot_url(rider_url):
    resp = requests.get(rider_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    img = soup.select_one("img[src*='jpeg'], img[src*='jpg'], img[src*='png']")
    if img and img.get("src"):
        return "https://procyclingstats.com/" + img["src"]
    return None


def download_image(url, save_path):
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(resp.content)


def main():
    os.makedirs("data/mugshots", exist_ok=True)
    team_links = get_team_links()
    print(str(len(team_links)) + " teams found\n")
    print("Starting to process teams and riders...")

    for team_url in team_links:
        print(f"\nProcessing team: {team_url}")
        rider_links = get_rider_links(team_url)
        for rider_url in tqdm(rider_links):
            mugshot_url = get_mugshot_url(rider_url)

            if mugshot_url:
                if mugshot_url.endswith("rider/"):
                    continue

                filename = mugshot_url.split("/")[-1]
                filename = filename.replace("-2025", "")
                filename = filename.replace("-2024", "")
                filename = filename.replace("-2023", "")
                save_path = os.path.join("data/mugshots", filename)
                if not os.path.exists(save_path):
                    download_image(mugshot_url, save_path)
                    time.sleep(0.1)  # Be polite to the server
            else:
                print("    No mugshot found for rider:", rider_url)
        time.sleep(0.1)  # Be polite to the server


if __name__ == "__main__":
    main()
