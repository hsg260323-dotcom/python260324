import requests
from bs4 import BeautifulSoup
import csv
import datetime

# 오늘 날짜로 파일명 생성
today = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'kpi200_pyeonip_all_{today}.csv'

# 데이터 저장 리스트
all_data = []

# 1부터 20페이지까지 크롤링
for page in range(1, 21):
    url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"
    
    # 페이지 요청
    response = requests.get(url)
    response.raise_for_status()  # 오류 발생 시 예외
    
    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 편입종목상위 섹션 찾기
    header = soup.find('h4', class_='top_tlt')
    if not header or '편입종목상위' not in header.text:
        print(f"페이지 {page}: 편입종목상위 섹션을 찾을 수 없습니다.")
        continue
    
    # 다음 테이블 찾기 (class="type_1")
    table = header.find_next('table', class_='type_1')
    if not table:
        print(f"페이지 {page}: 테이블을 찾을 수 없습니다.")
        continue
    
    # 테이블 데이터 추출
    rows = table.find_all('tr')
    for row in rows[1:]:  # 첫 번째 행은 헤더
        cols = row.find_all('td')
        if len(cols) >= 7:
            종목명 = cols[0].find('a').text.strip() if cols[0].find('a') else cols[0].text.strip()
            현재가 = cols[1].text.strip()
            전일비_span = cols[2].find('span', class_='tah')
            전일비_direction = cols[2].find('em').find('span', class_='blind').text.strip() if cols[2].find('em') else ''
            전일비 = f"{전일비_direction} {전일비_span.text.strip()}" if 전일비_span else cols[2].text.strip()
            등락률_span = cols[3].find('span', class_='tah')
            등락률 = 등락률_span.text.strip() if 등락률_span else cols[3].text.strip()
            거래량 = cols[4].text.strip()
            거래대금 = cols[5].text.strip()
            시가총액 = cols[6].text.strip()
            all_data.append({
                '종목명': 종목명,
                '현재가': 현재가,
                '전일비': 전일비,
                '등락률': 등락률,
                '거래량': 거래량,
                '거래대금': 거래대금,
                '시가총액': 시가총액
            })
    
    print(f"페이지 {page} 크롤링 완료")

# CSV 파일로 저장
with open(filename, 'w', newline='', encoding='utf-8') as f:
    if all_data:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)

print(f"모든 데이터가 {filename} 파일로 저장되었습니다.")
