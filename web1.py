#web1.py

from bs4 import BeautifulSoup

page = open("Chap09_test.html", "rt", encoding="utf-8").read()

soup = BeautifulSoup(page, "html.parser")

# print(soup.prettify())

# #<p>태그의 텍스트만 추출하기
# print(soup.p.string)
# print(soup.find_all("p"))
# print(soup.find("p"))
# print(soup.find_all("p", class_="outer-text"))
# print(soup.find_all("p", attrs={"class": "outer-text"}))
# print(soup.find_all(id="first"))
for tag in soup.find_all("p"):
    title = tag.text.strip()
    title = title.replace("\n", "")
    print(title)


#문자열처리 메서드와 정규표현식
strA = "<<< python >>>"
result = strA.strip("<> ")
print(result)
strB = result.replace("python", "python javascript")
print(strB)
result = "spam egg spam egg".split()
print(result)
print(":".join(result))

#정규표현식: 특정한 패턴(규칙)문자열
import re

result = re.search(r"\d{4}", "올해는 2026년입니다.")
print(result.group())

result = re.search("apple", "this is apple")
print(result.group())


