import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="안산시 노인 인구 및 복지시설 시각화", layout="wide")
st.title("🏙️ 안산시 노인 인구수 & 복지시설 비교 시각화 (병합 없이)")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설 CSV 업로드", type=["csv"])

def read_csv_safe(file):
    try:
        return pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="cp949")
    except Exception:
        return pd.read_csv(file, sep=";", encoding="cp949")

if pop_file:
    pop_df = read_csv_safe(pop_file)
    pop_df.columns = pop_df.columns.str.strip()
    st.subheader("👵 노인 인구 데이터 미리보기")
    st.dataframe(pop_df.head())

    # --- 시각화 ---
    pop_x = st.sidebar.selectbox("노인 인구 데이터의 지역 컬럼", pop_df.columns)
    pop_y = st.sidebar.selectbox("노인 인구수 컬럼", pop_df.columns)

    st.subheader("📊 지역별 노인 인구수")
    fig1 = px.bar(pop_df, x=pop_x, y=pop_y, color=pop_y, text=pop_y)
    fig1.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="노인 인구수")
    st.plotly_chart(fig1, use_container_width=True)

if facility_file:
    fac_df = read_csv_safe(facility_file)
    fac_df.columns = fac_df.columns.str.strip()
    st.subheader("🏢 복지시설 현황 데이터 미리보기")
    st.dataframe(fac_df.head())

    # --- 시각화 ---
    fac_x = st.sidebar.selectbox("복지시설 데이터의 지역 컬럼", fac_df.columns)
    fac_y = st.sidebar.selectbox("복지시설 수 컬럼", fac_df.columns)

    st.subheader("📊 지역별 복지시설 수")
    fig2 = px.bar(fac_df, x=fac_x, y=fac_y, color=fac_y, text=fac_y)
    fig2.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="복지시설 수")
    st.plotly_chart(fig2, use_container_width=True)
