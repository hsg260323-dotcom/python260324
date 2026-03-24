#분기구문.py
#블럭으로 주석처리 : ctrl+/

# score = int(input("점수를 입력하세요: "))

# if score >= 90:
#     print("A학점입니다.")
# elif score >= 80:
#     print("B학점입니다.")
# elif score >= 70:
#     print("C학점입니다.")
# elif score >= 60:
#     print("D학점입니다.")
# else:
#     print("F학점입니다.")

#print("등급은 ", grade)

value=5
while value > 0:
    print("현재 값:", value)
    value -= 1

lst=[100, 3.14, "apple"]
for item in lst:
    print("항목:", item)

colors ={"apple":"red", "banana":"yellow", "grape":"purple"}
for key, value in colors.items():
    print("과일:", key, "색상:", value)


print("----range()----")
print(list(range(10)))
print(list(range(2000,2027)))
print(list(range(1,32)))
print(list(range(10,0,-1)))

print("----리스트 컴프리헨션----")
lst=[1,2,3,4,5,6,7,8,9,10]
print([i**2 for i in lst if i>5])
tp=("apple", "banana")
print([len(i) for i in tp])


print("----필터링함수----")
lst=[10,25,30]
itemL=filter(None,lst)
for item in itemL:
    print(item)

print("----필터링함수 사용----")
def getBiggerThan20(x):
    return x>20

itemL=filter(getBiggerThan20,lst)
for item in itemL:
    print(item)

print("----람다함수 사용----")
itemL=filter(lambda x: x>20,lst)
for item in itemL:
    print(item)





