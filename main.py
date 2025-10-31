# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="주민등록 인구 및 세대현황 시각화", layout="wide")

@st.cache_data
def load_data():
    """CSV 파일 불러오기"""
    file_path = "202509_202509_주민등록인구및세대현황_월간.csv"
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        if df.shape[1] == 1:
            df = pd.read_csv(file_path, encoding="cp949")
    except Exception as e:
        st.error(f"파일 불러오기 오류: {e}")
        st.stop()
    return df

# 데이터 불러오기
df = load_data()

# 제목
st.title("📈 주민등록 인구 및 세대현황 (월간) 시각화 대시보드")
st.markdown("이 대시보드는 주민등록 인구 및 세대현황 데이터를 기반으로 Plotly 시각화를 제공합니다.")

# 데이터 미리보기
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 컬럼 목록 가져오기
cols = df.columns.tolist()

# 날짜 컬럼 후보 탐지
date_cols = [c for c in cols if any(k in c for k in ["기간", "연월", "기준", "년월", "날짜"])]
group_cols = [c for c in cols if any(k in c for k in ["시도", "시군구", "행정", "구분", "성별", "연령", "지역"])]
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if not numeric_cols:
    for c in cols:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="ignore")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# 사이드바 설정
st.sidebar.header("⚙️ 설정")
date_col = st.sidebar.selectbox("📅 날짜(기간) 컬럼", [None] + date_cols)
group_col = st.sidebar.selectbox("🏙️ 그룹(지역/구분) 컬럼", [None] + group_cols)
metric_col = st.sidebar.selectbox("📊 수치 컬럼", [None] + numeric_cols)

# 날짜 변환
if date_col:
    df[date_col] = pd.to_datetime(df[date_col].astype(str), errors="coerce")

# 메인 시각화
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
    st.info("📌 왼쪽 사이드바에서 수치 컬럼을 선택해주세요.")

# 그룹별 평균 그래프
if group_col and metric_col:
    st.subheader("📦 그룹별 평균 비교")
    grouped = df.groupby(group_col)[metric_col].mean().reset_index()
    fig_bar = px.bar(grouped, x=group_col, y=metric_col, title=f"{metric_col} 평균 ({group_col}별)")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.caption("© 2025. Streamlit + Plotly 인구 데이터 시각화 예제")
