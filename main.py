import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="안산시 노인 인구 vs 복지시설 시각화", layout="wide")
st.title("📈 경기도 안산시 노인 인구수 vs 복지시설 현황 비교 시각화")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 및 독거노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설현황 CSV 업로드", type=["csv"])

def read_csv_safe(file):
    """한글 CSV 파일을 자동으로 읽기"""
    try:
        return pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="cp949")
    except Exception:
        return pd.read_csv(file, sep=";", encoding="cp949")

if pop_file and facility_file:
    pop_df = read_csv_safe(pop_file)
    fac_df = read_csv_safe(facility_file)

    st.success("✅ 두 파일이 업로드되었습니다!")

    st.subheader("👵 노인 인구 데이터 미리보기")
    st.dataframe(pop_df.head())

    st.subheader("🏢 복지시설 현황 데이터 미리보기")
    st.dataframe(fac_df.head())

    # --- 시각화 컬럼 선택 ---
    st.sidebar.header("⚙️ 시각화 설정")
    pop_x = st.sidebar.selectbox("노인 인구 데이터 기준(연도/지역)", pop_df.columns)
    pop_y = st.sidebar.selectbox("노인 인구수 컬럼", pop_df.columns)

    fac_x = st.sidebar.selectbox("복지시설 데이터 기준(연도/지역)", fac_df.columns)
    fac_y = st.sidebar.selectbox("복지시설 수 컬럼", fac_df.columns)

    # --- 그래프 ---
    st.subheader("📊 노인 인구수 vs 복지시설 수 비교 그래프")

    fig = go.Figure()

    # 노인 인구 라인
    fig.add_trace(go.Scatter(
        x=pop_df[pop_x],
        y=pop_df[pop_y],
        name="노인 인구수",
        mode="lines+markers",
        line=dict(width=3)
    ))

    # 복지시설 라인
    fig.add_trace(go.Scatter(
        x=fac_df[fac_x],
        y=fac_df[fac_y],
        name="복지시설 수",
        mode="lines+markers",
        line=dict(width=3, dash="dot")
    ))

    fig.update_layout(
        title="노인 인구수 vs 복지시설 수 비교",
        xaxis_title="연도 또는 지역",
        yaxis_title="수량",
        legend_title="구분",
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 사이드바에서 두 개의 CSV 파일을 업로드해주세요.")
