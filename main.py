import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="안산시 노인 인구 및 복지시설 시각화", layout="wide")
st.title("🏙️ 경기도 안산시 노인 인구수 & 복지시설 비교 시각화")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 및 독거노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설현황 CSV 업로드", type=["csv"])

# --- 안전하게 CSV 읽기 ---
def read_csv_safe(file):
    try:
        return pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="cp949")
    except Exception:
        return pd.read_csv(file, sep=";", encoding="cp949")

if pop_file and facility_file:
    pop_df = read_csv_safe(pop_file)
    fac_df = read_csv_safe(facility_file)

    st.success("✅ 두 파일이 성공적으로 업로드되었습니다!")

    # --- 미리보기 ---
    st.subheader("👵 노인 인구 데이터 미리보기")
    st.dataframe(pop_df.head())

    st.subheader("🏢 복지시설 현황 데이터 미리보기")
    st.dataframe(fac_df.head())

    # --- 컬럼 선택 ---
    st.sidebar.header("⚙️ 시각화 설정")
    pop_x = st.sidebar.selectbox("노인 인구 데이터의 지역 컬럼", pop_df.columns)
    pop_y = st.sidebar.selectbox("노인 인구수 컬럼", pop_df.columns)
    fac_x = st.sidebar.selectbox("복지시설 데이터의 지역 컬럼", fac_df.columns)
    fac_y = st.sidebar.selectbox("복지시설 수 컬럼", fac_df.columns)

    # --- 그래프 1: 노인 인구 막대그래프 ---
    st.subheader("📊 1️⃣ 지역별 노인 인구수")
    fig1 = px.bar(
        pop_df,
        x=pop_x,
        y=pop_y,
        color=pop_y,
        title="지역별 노인 인구수",
        text=pop_y
    )
    fig1.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="노인 인구수")
    st.plotly_chart(fig1, use_container_width=True)

    # --- 그래프 2: 복지시설 막대그래프 ---
    st.subheader("🏢 2️⃣ 지역별 복지시설 개수")
    fig2 = px.bar(
        fac_df,
        x=fac_x,
        y=fac_y,
        color=fac_y,
        title="지역별 복지시설 개수",
        text=fac_y
    )
    fig2.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="복지시설 수")
    st.plotly_chart(fig2, use_container_width=True)

    # --- 그래프 3: 두 데이터를 겹쳐서 비교 (Group Bar Chart) ---
    st.subheader("⚖️ 3️⃣ 지역별 노인 인구수 & 복지시설 비교")

    # 병합을 위한 전처리
    merged = pd.merge(
        pop_df[[pop_x, pop_y]],
        fac_df[[fac_x, fac_y]],
        left_on=pop_x,
        right_on=fac_x,
        how="inner",
        suffixes=("_인구", "_시설")
    )

    # 겹친 막대그래프 (grouped bar)
    fig3 = go.Figure(data=[
        go.Bar(name="노인 인구수", x=merged[pop_x], y=merged[pop_y]),
        go.Bar(name="복지시설 수", x=merged[fac_x], y=merged[fac_y])
    ])
    fig3.update_layout(
        barmode="group",
        template="plotly_white",
        title="지역별 노인 인구수 vs 복지시설 수 비교",
        xaxis_title="지역",
        yaxis_title="수량",
        legend_title="구분"
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("👆 사이드바에서 두 개의 CSV 파일을 업로드해주세요.")
