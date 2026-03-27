import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Windows용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 타이타닉 데이터셋 로드
df = sns.load_dataset('titanic')

# 데이터 클린징
# 결측치 확인
print("결측치 확인:")
print(df.isnull().sum())

# Age 결측치를 평균으로 채우기
df['age'] = df['age'].fillna(df['age'].mean())

# Embarked 결측치를 최빈값으로 채우기
df['embarked'] = df['embarked'].fillna(df['embarked'].mode()[0])

# Cabin 열은 결측치가 많아 삭제 (실제로는 deck)
# 불필요한 열 제거 (deck, alive 등)
df.drop(['deck', 'alive', 'adult_male', 'alone'], axis=1, inplace=True)

# 성별별 생존율 계산
survival_rate = df.groupby('sex')['survived'].mean()
print("\n성별별 생존율:")
print(survival_rate)

# 그래프 그리기
plt.figure(figsize=(8, 6))
survival_rate.plot(kind='bar', color=['blue', 'pink'])
plt.title('타이타닉호 성별별 생존율')
plt.xlabel('성별')
plt.ylabel('생존율')
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.show()