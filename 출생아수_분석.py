# -*- coding: utf-8 -*-
"""
대한민국 출생아수 및 합계출산율 데이터 분석
원본 Excel 파일을 pandas로 분석하고 matplotlib으로 시각화
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (Windows 환경)
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


# ==========================================
# 1. Excel 파일 로드 및 데이터 구조 확인
# ==========================================

# Excel 파일 로드
file_name = '출생아수__합계출산율__자연증가_등_20260327151751.xlsx'
df_raw = pd.read_excel(file_name)

print("=" * 80)
print("원본 데이터 형태")
print("=" * 80)
print(f"Shape: {df_raw.shape}")
print(f"\n처음 5행:")
print(df_raw.head())
print(f"\n데이터 타입:")
print(df_raw.dtypes)

# 상세 정보 확인
print("\n" + "=" * 80)
print("컬럼 정보")
print("=" * 80)
print(df_raw.info())

print("\n" + "=" * 80)
print("결측치 확인")
print("=" * 80)
missing = df_raw.isnull().sum()
print(f"결측치 건수: {missing.sum()}")
if missing.sum() > 0:
    print(missing[missing > 0])


# ==========================================
# 2. 데이터 클랜징
# ==========================================

# 1단계: 데이터 구조 조정
df = df_raw.copy()

# 첫 번째 열의 이름을 '지표'로 바꾸기
df = df.rename(columns={df.columns[0]: '지표'})

print("\nStep 1: 데이터 구조 조정")
print(f"현재 shape: {df.shape}")
print(df.head(2))

# 2단계: 행과 열 전치
df_t = df.set_index('지표').T
df_t.index.name = '연도'
df_t.index = df_t.index.astype(str)

# 2025 p) 를 2025로 정리
df_t.index = df_t.index.str.replace(' p)', '')
df_t.index = df_t.index.astype(int)

print("\nStep 2: 행과 열 전치 후")
print(f"Shape: {df_t.shape}")
print(df_t.head())

# 3단계: 데이터 타입 및 결측치 처리
print("\nStep 3: 데이터 타입 and 결측치 처리")

# 모든 컬럼을 float로 변환
for col in df_t.columns:
    df_t[col] = pd.to_numeric(df_t[col], errors='coerce')

# 결측치 확인
print(f"결측치 건수:\n{df_t.isnull().sum()}")

# 이상치 확인 (음수 데이터 확인)
print(f"\n음수 데이터 확인:")
for col in ['출생아수(명)', '자연증가건수(명)', '합계출산율(명)']:
    if col in df_t.columns:
        negative_count = (df_t[col] < 0).sum()
        if negative_count > 0:
            print(f"  {col}: {negative_count}개의 음수 값")

print("\n클랜징된 데이터:")
print(df_t.tail())


# ==========================================
# 3. 기초 통계 분석
# ==========================================

# 전체 데이터 통계
print("\n" + "=" * 80)
print("전체 데이터 기초 통계")
print("=" * 80)
print(df_t.describe().T)

# 출생아수(명) 상세 분석
print("\n" + "=" * 80)
print("출생아수(명) 상세 분석")
print("=" * 80)
birth_data = df_t['출생아수(명)'].dropna()
print(f"평균: {birth_data.mean():,.0f}명")
print(f"중앙값: {birth_data.median():,.0f}명")
print(f"표준편차: {birth_data.std():,.0f}명")
print(f"최솟값: {birth_data.min():,.0f}명 (년도: {birth_data.idxmin()})")
print(f"최댓값: {birth_data.max():,.0f}명 (년도: {birth_data.idxmax()})")
print(f"범위: {birth_data.max() - birth_data.min():,.0f}명")

# 합계출산율(명) 상세 분석
print("\n" + "=" * 80)
print("합계출산율(명) 상세 분석")
print("=" * 80)
tfr_data = df_t['합계출산율(명)'].dropna()
print(f"평균: {tfr_data.mean():.3f}명")
print(f"중앙값: {tfr_data.median():.3f}명")
print(f"표준편차: {tfr_data.std():.3f}명")
print(f"최솟값: {tfr_data.min():.3f}명 (년도: {tfr_data.idxmin()})")
print(f"최댓값: {tfr_data.max():.3f}명 (년도: {tfr_data.idxmax()})")


# ==========================================
# 4. 다각도 데이터 분석
# ==========================================

# 1. 분석1: 임계기간별 출생아수 변화
print("\n" + "=" * 80)
print("분석 1: 임계기간별 출생아수 변화")
print("=" * 80)
periods = {
    '1970-1979년': df_t.loc[1970:1979, '출생아수(명)'].mean(),
    '1980-1989년': df_t.loc[1980:1989, '출생아수(명)'].mean(),
    '1990-1999년': df_t.loc[1990:1999, '출생아수(명)'].mean(),
    '2000-2009년': df_t.loc[2000:2009, '출생아수(명)'].mean(),
    '2010-2019년': df_t.loc[2010:2019, '출생아수(명)'].mean(),
    '2020-2025년': df_t.loc[2020:2025, '출생아수(명)'].mean(),
}
for period, avg in periods.items():
    print(f"{period}: {avg:,.0f}명")

# 2. 분석2: 연도별 변동률 (Y-o-Y)
print("\n" + "=" * 80)
print("분석 2: 연도별 변동률 (Year-over-Year)")
print("=" * 80)
birth_yoy = df_t['출생아수(명)'].pct_change() * 100
print(f"최대 증가율: {birth_yoy.max():.2f}% (년도: {birth_yoy.idxmax()})")
print(f"최대 감소율: {birth_yoy.min():.2f}% (년도: {birth_yoy.idxmin()})")
print(f"평균 변동률: {birth_yoy.mean():.2f}%")

# 2020년 이후의 변동률
print(f"\n2020년 이후 연도별 변동률:")
print(birth_yoy[2020:].to_string())

# 3. 분석3: 출생아수와 합계출산율의 상관관계
print("\n" + "=" * 80)
print("분석 3: 출생아수와 합계출산율의 상관관계")
print("=" * 80)
correlation = df_t['출생아수(명)'].corr(df_t['합계출산율(명)'])
print(f"Pearson 상관계수: {correlation:.4f}")
print("→ 매우 강한 양의 상관관계 (1에 가까울수록 강함)")

# 4. 분석4: 시간 추세 분석
print("\n" + "=" * 80)
print("분석 4: 시간 추세 분석")
print("=" * 80)
# 1970년 vs 2025년 비교
birth_1970 = df_t.loc[1970, '출생아수(명)']
birth_2025 = df_t.loc[2025, '출생아수(명)']
decrease_pct = ((birth_2025 - birth_1970) / birth_1970) * 100

print(f"1970년 출생아수: {birth_1970:,.0f}명")
print(f"2025년 출생아수: {birth_2025:,.0f}명")
print(f"변화: {decrease_pct:+.2f}%")
print(f"감소량: {birth_1970 - birth_2025:,.0f}명")

# 5. 분석5: 최근 10년 추세
print("\n" + "=" * 80)
print("분석 5: 최근 10년(2015-2025) 추세")
print("=" * 80)
recent = df_t.loc[2015:2025, '출생아수(명)']
print(recent.to_string())
print(f"\n2015-2025 감소율: {((recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0] * 100):.2f}%")


# ==========================================
# 5. 시각화 - 연도별 출생아수 라인그래프
# ==========================================

# 기본 라인 그래프
fig, ax = plt.subplots(figsize=(14, 7))

# 출생아수 라인 그래프
ax.plot(df_t.index, df_t['출생아수(명)'], 
        marker='o', linewidth=2.5, markersize=4, 
        color='#2E86AB', label='출생아수', alpha=0.8)

# 스타일 설정
ax.set_title('연도별 대한민국 출생아수 추이 (1970-2025)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('연도', fontsize=12, fontweight='bold')
ax.set_ylabel('출생아수 (명)', fontsize=12, fontweight='bold')

# 그리드 추가
ax.grid(True, alpha=0.3, linestyle='--')

# y축 포맷 (천 단위 구분)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# x축 눈금 설정 (5년 단위)
ax.set_xticks(range(1970, 2030, 5))
ax.set_xticklabels(range(1970, 2030, 5), rotation=45)

# 범례
ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)

plt.tight_layout()
plt.show()

print("✓ 라인 그래프 생성 완료")


# ==========================================
# 6. 시각화 - 다중 지표
# ==========================================

# 다중 지표 시각화 (출생아수 + 합계출산율)
fig, ax1 = plt.subplots(figsize=(14, 7))

# 첫 번째 y축 (출생아수)
color = '#2E86AB'
ax1.set_xlabel('연도', fontsize=12, fontweight='bold')
ax1.set_ylabel('출생아수 (명)', color=color, fontsize=12, fontweight='bold')
line1 = ax1.plot(df_t.index, df_t['출생아수(명)'], 
                 marker='o', linewidth=2, markersize=4,
                 color=color, label='출생아수', alpha=0.8)
ax1.tick_params(axis='y', labelcolor=color)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# 두 번째 y축 (합계출산율)
ax2 = ax1.twinx()
color = '#A23B72'
ax2.set_ylabel('합계출산율 (명)', color=color, fontsize=12, fontweight='bold')
line2 = ax2.plot(df_t.index, df_t['합계출산율(명)'], 
                 marker='s', linewidth=2, markersize=4,
                 color=color, label='합계출산율', alpha=0.8)
ax2.tick_params(axis='y', labelcolor=color)

# 제목 및 그리드
ax1.set_title('출생아수 vs 합계출산율 추이 (1970-2025)', 
              fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')

# x축 눈금 설정 (5년 단위)
ax1.set_xticks(range(1970, 2030, 5))
ax1.set_xticklabels(range(1970, 2030, 5), rotation=45)

# 범례
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', fontsize=11, frameon=True, shadow=True)

plt.tight_layout()
plt.show()

print("✓ 다중 지표 그래프 생성 완료")


# ==========================================
# 7. 시각화 - 최근 15년 상세 분석
# ==========================================

# 최근 15년 상세 분석 (2010-2025)
recent_data = df_t.loc[2010:2025, '출생아수(명)']

fig, ax = plt.subplots(figsize=(14, 7))

# 막대 그래프로 표현
bars = ax.bar(recent_data.index, recent_data.values, 
              color=['#2E86AB' if x > recent_data.mean() else '#F18F01' 
                     for x in recent_data.values],
              alpha=0.8, edgecolor='black', linewidth=1.2)

# 평균선 추가
ax.axhline(y=recent_data.mean(), color='red', linestyle='--', 
           linewidth=2, label=f'평균: {recent_data.mean():,.0f}명', alpha=0.7)

# 스타일 설정
ax.set_title('최근 15년 연도별 출생아수 (2010-2025)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('연도', fontsize=12, fontweight='bold')
ax.set_ylabel('출생아수 (명)', fontsize=12, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

# x축 설정
ax.set_xticks(range(2010, 2026))
ax.set_xticklabels(range(2010, 2026), rotation=45)

# 값 레이블 추가
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

# 범례
ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)

plt.tight_layout()
plt.show()

print("✓ 최근 15년 상세 분석 그래프 생성 완료")


# ==========================================
# 8. 시각화 - 기간별 분포 비교
# ==========================================

# 기간별 분포 비교 (박스플롯)
# 기간 분류
def classify_period(year):
    if year <= 1979:
        return '1970s'
    elif year <= 1989:
        return '1980s'
    elif year <= 1999:
        return '1990s'
    elif year <= 2009:
        return '2000s'
    elif year <= 2019:
        return '2010s'
    else:
        return '2020s'

df_t['기간'] = [classify_period(year) for year in df_t.index]

# 데이터 분류
data_by_period = [df_t[df_t['기간'] == period]['출생아수(명)'].values 
                  for period in ['1970s', '1980s', '1990s', '2000s', '2010s', '2020s']]

fig, ax = plt.subplots(figsize=(12, 7))

# 박스플롯
bp = ax.boxplot(data_by_period, 
                labels=['1970s', '1980s', '1990s', '2000s', '2010s', '2020s'],
                patch_artist=True, widths=0.6,
                medianprops=dict(color='red', linewidth=2),
                boxprops=dict(facecolor='#2E86AB', alpha=0.7),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5))

ax.set_title('기간별 출생아수 분포 비교', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('기간', fontsize=12, fontweight='bold')
ax.set_ylabel('출생아수 (명)', fontsize=12, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.show()

print("✓ 기간별 분포 비교 그래프 생성 완료")

print("\n" + "=" * 80)
print("모든 분석 및 시각화 완료!")
print("=" * 80)
