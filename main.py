import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="안산시 노인 데이터 비교 시각화", layout="wide")

st.title("📈 경기도 안산시 노인 인구수 vs 복지시설 현황 비교 시각화")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 및 독거노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설현황 CSV 업로드", type=["csv"])

# --- 안전하게 CSV 읽는 함수 ---
def read_csv_safe(file):
    try:
        return pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="cp949")
    except Exception:
        return pd.read_csv(file, sep=";", encoding="cp949")

# --- 파일 업로드 후 처리 ---
if pop_file and facility_file:
    pop_df = read_csv_safe(pop_file)
    fac_df = read_csv_safe(facility_file)

    st.success("✅ 두 파일이 성공적으로 업로드되었습니다!")

    st.subheader("👵 노인 인구 데이터 미리보기")
    st.dataframe(pop_df.head())

    st.subheader("🏢 노인복지시설 현황 데이터 미리보기")
    st.dataframe(fac_df.head())

    # --- 시각화 컬럼 선택 ---
    st.sidebar.header("⚙️ 시각화 설정")
    time_col_pop = st.sidebar.selectbox("노인 인구 데이터의 기준(연도/지역) 컬럼", pop_df.columns)
    value_col_pop = st.sidebar.selectbox("노인 인구수 컬럼", pop_df.columns)

    time_col_fac = st.sidebar.selectbox("복지시설 데이터의 기준(연도/지역) 컬럼", fac_df.columns)
    value_col_fac = st.sidebar.selectbox("복지시설 개수 컬럼", fac_df.columns)

    # --- 데이터 병합을 위한 전처리 ---
    # 기준 축(예: 연도, 지역명)을 공통 키로 사용
    merged_df = pd.merge(
        pop_df[[time_col_pop, value_col_pop]],
        fac_df[[time_col_fac, value_col_fac]],
        left_on=time_col_pop,
        right_on=time_col_fac,
        how="inner",
        suffixes=("_인구", "_시설")
    )

    st.subheader("📋 병합된 비교 데이터")
    st.dataframe(merged_df)

    # --- Plotly 꺾은선 그래프 ---
    st.subheader("📊 노인 인구수 vs 복지시설 수 비교 그래프")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=merged_df[time_col_pop],
        y=merged_df[value_col_pop],
        name="노인 인구수",
        mode="lines+markers",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=merged_df[time_col_fac],
        y=merged_df[value_col_fac],
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
