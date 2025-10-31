import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="안산시 노인 관련 데이터 시각화", layout="wide")

st.title("📊 경기도 안산시 노인 인구 및 복지시설 시각화")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 및 독거노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설현황 CSV 업로드", type=["csv"])

if pop_file and facility_file:
    # CSV 파일 읽기
    pop_df = pd.read_csv(pop_file)
    fac_df = pd.read_csv(facility_file)

    st.success("✅ 두 파일이 성공적으로 업로드되었습니다!")

    # --- 데이터 미리보기 ---
    st.subheader("👵 노인 및 독거노인 인구 데이터")
    st.dataframe(pop_df.head())

    st.subheader("🏢 노인복지시설현황 데이터")
    st.dataframe(fac_df.head())

    # --- 기본적인 컬럼 확인 ---
    st.sidebar.subheader("📈 시각화 설정")
    pop_x = st.sidebar.selectbox("노인 인구 데이터의 x축 선택", options=pop_df.columns)
    pop_y = st.sidebar.selectbox("노인 인구 데이터의 y축 선택", options=pop_df.columns)

    fac_x = st.sidebar.selectbox("복지시설 데이터의 x축 선택", options=fac_df.columns)
    fac_y = st.sidebar.selectbox("복지시설 데이터의 y축 선택", options=fac_df.columns)

    # --- 시각화 ---
    st.subheader("1️⃣ 노인 인구수 시각화")
    fig1 = px.bar(pop_df, x=pop_x, y=pop_y, color=pop_y, title="노인 및 독거노인 인구 현황")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("2️⃣ 노인복지시설 현황 시각화")
    fig2 = px.bar(fac_df, x=fac_x, y=fac_y, color=fac_y, title="노인복지시설 현황")
    st.plotly_chart(fig2, use_container_width=True)

    # --- 비교 시각화 (예시: 시설 수 대비 인구수 비율 등) ---
    st.subheader("3️⃣ 데이터 비교 시각화 (예시)")

    # 비교용 그래프 예시 (합계 비교)
    pop_sum = pop_df[pop_y].sum()
    fac_sum = fac_df[fac_y].sum()
    compare_df = pd.DataFrame({
        "구분": ["노인 인구수", "복지시설 수"],
        "값": [pop_sum, fac_sum]
    })
    fig3 = px.pie(compare_df, names="구분", values="값", title="노인 인구수 vs 복지시설 수 비율")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("👆 사이드바에서 두 개의 CSV 파일을 업로드해주세요.")

