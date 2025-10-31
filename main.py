# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="주민등록 인구 및 세대현황 시각화", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("202509_202509_주민등록인구및세대현황_월간.csv", encoding="utf-8")
        if df.shape[1] == 1:
            df = pd.read_csv("202509_202509_주민등록인구및세대현황_월간.csv", encoding="cp949")
    except Exception as e:
        st.error(f"파일 불러오기 오류: {e}")
        st.stop()
    return df

# 데이터 불러오기
df = load_data()

st.title("📈 주민등록 인구 및 세대현황 (월간) 시각화 대시보드")
st.markdown("이 대시보드는 주민등록 인구 및 세대현황 데이터를 기반으로 Plotly 시각화를 제공합니다.")

# 데이터 정보 확인
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 컬럼 선택
all_columns = df.columns.tolist()

# 날짜 컬럼 자동 탐지
date_candidates = [c for c in all_columns if any(k in c for k in ["기간", "연월", "기준", "년월", "날짜"])]
date_col = st.sidebar.selectbox("📅 날짜(기간) 컬럼 선택", [None] + date_candidates)

# 그룹(지역, 성별 등) 컬럼
group_candidates = [c for c in all_columns if any(k in c for k in ["시도", "시군구", "행정", "구분", "성별", "연령", "지역"])]
group_col = st.sidebar.selectbox("🏙️ 그룹(지역/구분) 컬럼 선택", [None] + group_candidates)

# 수치 컬럼 자동 선택
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
if not numeric_cols:
    for c in all_columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="ignore")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

metric_col = st.sidebar.selectbox("📊 수치 컬럼 선택", [None] + numeric_cols)

# 날짜 컬럼을 datetime으로 변환
if date_col:
    df[date_col] = pd.to_datetime(df[date_col].astype(str), errors="coerce")

# 시각화
st.subheader("📉 시각화 결과")

if metric_col:
    if date_col and group_col:
        fig = px.line(df, x=date_col, y=metric_col, color=group_col, title=f"{metric_col} 추이 ({group_col}별)")
    elif date_col:
        fig = px.line(df, x=date_col, y=metric_col, title=f"{metric_col} 추이")
    elif group_col:
        fig = px.bar(df, x=group_col, y=metric_col, title=f"{metric_col} ({group_col}별)")
    else:
        fig = px.histogram(df, x=metric_col, nbins=20, title=f"{metric_col} 분포")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽 사이드바에서 '수치 컬럼'을 선택해주세요.")

# 추가 시각화 옵션
if group_col and metric_col:
    st.subheader("📦 그룹별 평균 비교")
    grouped = df.groupby(group_col)[metric_col].mean().reset_index()
    fig_bar = px.bar(grouped, x=group_col, y=metric_col, title=f"{metric_col} 평균 ({group_col}별)")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.caption("© 2025. Streamlit + Plotly 인구 데이터 시각화 예제")

