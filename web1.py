#web1.py

from bs4 import BeautifulSoup

page = open("Chap09_test.html", "rt", encoding="utf-8").read()

soup = BeautifulSoup(page, "html.parser")

# print(soup.prettify())

# #<p>태그의 텍스트만 추출하기
# print(soup.p.string)
print(soup.find_all("p"))





