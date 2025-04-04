import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(font='Malgun Gothic', 
        rc={'axes.unicode_minus' : False}, 
        style='darkgrid')

# 한글폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic' 
plt.rcParams['axes.unicode_minus'] = False 

# 페이지 설정
# st.set_page_config(page_title="Matplotlib & Seaborn 튜토리얼", layout="wide") 
st.title("Matplotlib & Seaborn 튜토리얼") 

# 데이터셋 불러오기 
tips = sns.load_dataset('tips') 

# 데이터 미리보기 
st.subheader('데이터 미리보기')
st.dataframe(tips.head())

# 기본 막대 그래프, matplotlit + seaborn 
st.subheader("1. 기본 막대 그래프")
# 객체지향방식으로 차트 작성 하는 이유
# 그래프를 그리는 목적 : (예쁘게) 잘 나오라고
fig, ax = plt.subplots(figsize=(10, 6)) # matplotlib
sns.barplot(data=tips, x='day', y='total_bill', ax=ax) # seaborn

ax.set_title('요일별 평균 지불 금액') # matplotlib
ax.set_xlabel('요일')               # matplotlib
ax.set_ylabel('평균 지불 금액($)')   # matplotlib

# plt.show() ==> 이 문법은 jupyter notebook, google colab에서 활용할 때 사용
st.pyplot(fig) # streamlit 문법

# 산점도
# x축, y축이 연속형 변수여야 합니다. 
st.subheader("2. 산점도")
fig1, ax1 = plt.subplots(figsize=(10, 6)) # matplotlib
sns.barplot(data=tips, x='day', y='total_bill', ax=ax) # seaborn
sns.scatterplot(data=tips, x = 'total_bill', y = 'tip', hue='day', size='size', ax=ax1)
ax1.set_title("한글")
st.pyplot(fig1)

# 히트맵
st.subheader("3. 히트맵") 

# 요일과 시간별 평균 팁 계산 
pivot_df = tips.pivot_table(values='tip', index='day', columns='time', aggfunc='mean')
fig2, ax2 = plt.subplots(figsize=(10, 6)) 
sns.heatmap(pivot_df, annot=True, fmt='.2f', ax=ax2)
ax2.set_xlabel("한글")
st.pyplot(fig2)

# 회귀선이 있는 산점도
st.subheader('4. 회귀선이 있는 산점도')
fig3, ax3 = plt.subplots(figsize=(10, 6)) 
sns.regplot(data=tips, x='total_bill', y='tip', scatter_kws={'alpha':0.5}, ax=ax3)
st.pyplot(fig3)

# ChatGPT 질문던지기 팁 : fig, ax = plt.subplots() 형태로 만들어줘!

st.subheader('4. 회귀선이 있는 산점도')

# Seaborn 스타일 설정
sns.set_style("whitegrid")  # 배경 스타일 지정
sns.set_palette("pastel")   # 색상 팔레트

# 그래프 생성
fig3, ax3 = plt.subplots(figsize=(10, 6))

# 산점도 + 회귀선
sns.regplot(
    data=tips,
    x='total_bill',
    y='tip',
    scatter_kws={'alpha': 0.5, 's': 60},  # 투명도와 점 크기
    line_kws={'color': 'red', 'linewidth': 2},  # 회귀선 스타일
    ax=ax3
)

# 제목 및 라벨 꾸미기
ax3.set_title("총 지불 금액 vs 팁 (회귀선 포함)", fontsize=16, fontweight='bold')
ax3.set_xlabel("총 지불 금액($)", fontsize=12)
ax3.set_ylabel("팁($)", fontsize=12)

# 축 눈금 크기 조절
ax3.tick_params(axis='both', labelsize=10)

# 격자 추가 (선택)
ax3.grid(True, linestyle='--', alpha=0.5)

# Streamlit에 출력
st.pyplot(fig3)
########################################################
# 📈 1. 라인 그래프 (Line Plot) - 요일별 평균 지불 금액
st.subheader("📈 요일별 평균 지불 금액 (라인 그래프)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x=tips["day"], y=tips["total_bill"], marker="o", ax=ax, estimator="mean")
ax.set_title("요일별 평균 지불 금액")
ax.set_xlabel("요일")
ax.set_ylabel("평균 지불 금액 ($)")
st.pyplot(fig)

# 📊 2. 박스 플롯 (Box Plot) - 요일별 지불 금액 분포
st.subheader("📊 요일별 지불 금액 분포 (박스 플롯)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="day", y="total_bill", data=tips, ax=ax)
ax.set_title("요일별 총 지불 금액 분포")
ax.set_xlabel("요일")
ax.set_ylabel("총 지불 금액 ($)")
st.pyplot(fig)

# 🎻 3. 바이올린 플롯 (Violin Plot) - 요일별 지불 금액 분포
st.subheader("🎻 요일별 지불 금액 분포 (바이올린 플롯)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(x="day", y="total_bill", data=tips, ax=ax, inner="quartile")
ax.set_title("요일별 총 지불 금액 분포")
ax.set_xlabel("요일")
ax.set_ylabel("총 지불 금액 ($)")
st.pyplot(fig)

# 🥧 4. 파이 차트 (Pie Chart) - 성별 비율
st.subheader("🥧 성별 비율 (파이 차트)")
fig, ax = plt.subplots(figsize=(6, 6))
gender_counts = tips["sex"].value_counts()
ax.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
ax.set_title("성별 비율")
st.pyplot(fig)

# 🍩 5. 도넛 차트 (Donut Chart) - 성별 비율
st.subheader("🍩 성별 비율 (도넛 차트)")
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%",
                                  startangle=90, colors=sns.color_palette("pastel"), wedgeprops={"edgecolor": "w"})
center_circle = plt.Circle((0,0), 0.5, fc='white')  # 도넛 효과 추가
fig.gca().add_artist(center_circle)
ax.set_title("성별 비율 (도넛 차트)")
st.pyplot(fig)

# 🐝 6. 스와름 플롯 (Swarm Plot) - 요일별 지불 금액
st.subheader("🐝 요일별 지불 금액 (스와름 플롯)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.swarmplot(x="day", y="total_bill", data=tips, ax=ax)
ax.set_title("요일별 총 지불 금액")
ax.set_xlabel("요일")
ax.set_ylabel("총 지불 금액 ($)")
st.pyplot(fig)

# 📉 7. ECDF 그래프 (누적 분포 함수) - 지불 금액 분포
st.subheader("📉 총 지불 금액의 ECDF 그래프")
fig, ax = plt.subplots(figsize=(8, 5))
sns.ecdfplot(x=tips["total_bill"], ax=ax)
ax.set_title("총 지불 금액의 ECDF 그래프")
ax.set_xlabel("총 지불 금액 ($)")
ax.set_ylabel("누적 확률")
st.pyplot(fig)