#demoIndex.py

strA="파이썬은 강력해"
strB="python"

print(strA[0])
print(strA[0:3])
print(strA[:3])
print(strA[-2:])


#리스트형식 연습
lst=[10,20,30]
print(len(lst))
lst.append(40)
print(lst)
lst.insert(1,100)
print(lst)
lst.remove(10)
print(lst)

#세트형식 연습
a={1,2,3,3}
b={3,4,4,5}


print(a)
print(len(b))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#튜플형식 연습
tp=(100,200,300)
print(tp)
print(len(tp))

#함수 정의
def calc(a,b):
    return a+b, a*b

#호출
print(calc(3,4))

#한방에 입력
print("id: %s, name: %s" % ("kim","김유신"))






