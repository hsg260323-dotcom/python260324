import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

BASE_ENTRY_URL = "https://finance.naver.com/sise/entryJongmok.naver?type=KPI200"


def fetch_html(url: str, timeout: int = 10) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def find_entry_table(soup: BeautifulSoup):
    # '편입종목상위' 제목을 가진 박스 내부의 table.type_1 선택
    box = soup.find('div', class_='box_type_m')
    if not box:
        return None
    title = box.find('h4', class_='top_tlt')
    if not title or '편입종목' not in title.get_text():
        return None
    table = box.find('table', class_='type_1')
    return table


def parse_table(table) -> tuple:
    rows = []
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    tbody = table.find('tbody') or table
    for tr in tbody.find_all('tr'):
        # skip separator or empty rows
        if 'blank_' in (tr.get('class') or [''] ) or tr.find('td', class_='blank_07'):
            continue
        cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        if not cols:
            continue
        rows.append(cols)
    return headers, rows


def get_max_page(soup: BeautifulSoup) -> int:
    nav = soup.find('table', class_='Nnavi')
    if not nav:
        return 1
    pages = []
    for a in nav.find_all('a'):
        href = a.get('href', '')
        if 'page=' in href:
            try:
                p = int(href.split('page=')[-1])
                pages.append(p)
            except ValueError:
                continue
    return max(pages) if pages else 1


def save_csv(headers, rows, filename: str):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)


def main():
    all_rows = []
    headers = None

    # 1) 첫 페이지로 최대 페이지 수 파악
    html1 = fetch_html(BASE_ENTRY_URL + '&page=1')
    soup1 = BeautifulSoup(html1, 'lxml')
    max_page = get_max_page(soup1)

    # 2) 각 페이지에서 테이블 추출
    for page in range(1, max_page + 1):
        url = f"{BASE_ENTRY_URL}&page={page}"
        html = fetch_html(url)
        soup = BeautifulSoup(html, 'lxml')
        table = find_entry_table(soup)
        if table is None:
            print(f'페이지 {page}에서 테이블을 찾지 못했습니다.')
            continue
        h, rows = parse_table(table)
        if headers is None:
            headers = h
        all_rows.extend(rows)

    if not all_rows:
        print('추출된 데이터가 없습니다.')
        return

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_file = f'kpi200_pyeonip_all_{now}.csv'
    save_csv(headers, all_rows, out_file)
    print(f'저장 완료: {out_file} (총 행: {len(all_rows)})')


if __name__ == '__main__':
    main()
