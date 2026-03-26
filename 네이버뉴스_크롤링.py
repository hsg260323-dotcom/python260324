import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.5845.188 Safari/537.36"
}

def get_titles(url, selector=".sds-comps-text-type-headline1", headers=None, timeout=10):
    if headers is None:
        headers = DEFAULT_HEADERS
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    titles = []
    for el in soup.select(selector):
        text = el.get_text(strip=True)
        if text:
            titles.append(text)
    return titles


def save_titles_to_excel(titles, filename="naver_result.xlsx", url=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "titles"
    ws.append(["crawl_time", "source_url", "title"])
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    for t in titles:
        ws.append([now, url or "", t])
    wb.save(filename)
    return filename

if __name__ == "__main__":
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%95%84%EC%9D%B4%ED%8F%B017&ackey=j7mkbobm"
    titles = get_titles(url)
    for t in titles:
        print(t)
    saved = save_titles_to_excel(titles, filename="naver_result.xlsx", url=url)
    print(f"Saved {len(titles)} titles -> {saved}")