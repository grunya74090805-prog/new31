import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from thefuzz import process

st.set_page_config(page_title="안산시 노인 인구 및 복지시설 시각화", layout="wide")
st.title("🏙️ 경기도 안산시 노인 인구수 & 복지시설 비교 시각화")

# --- 파일 업로드 ---
st.sidebar.header("📂 CSV 파일 업로드")
pop_file = st.sidebar.file_uploader("노인 및 독거노인 인구수 CSV 업로드", type=["csv"])
facility_file = st.sidebar.file_uploader("노인복지시설현황 CSV 업로드", type=["csv"])

# --- 안전한 CSV 읽기 ---
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

    pop_df.columns = pop_df.columns.str.strip()
    fac_df.columns = fac_df.columns.str.strip()

    st.subheader("👵 노인 인구 데이터 미리보기")
    st.dataframe(pop_df.head())

    st.subheader("🏢 복지시설 현황 데이터 미리보기")
    st.dataframe(fac_df.head())

    st.sidebar.header("⚙️ 시각화 설정")
    pop_x = st.sidebar.selectbox("노인 인구 데이터의 지역 컬럼", pop_df.columns)
    pop_y = st.sidebar.selectbox("노인 인구수 컬럼", pop_df.columns)
    fac_x = st.sidebar.selectbox("복지시설 데이터의 지역 컬럼", fac_df.columns)
    fac_y = st.sidebar.selectbox("복지시설 수 컬럼", fac_df.columns)

    # --- 지역명 유사도 기반 병합 ---
    pop_df[pop_x] = pop_df[pop_x].astype(str).str.strip()
    fac_df[fac_x] = fac_df[fac_x].astype(str).str.strip()

    # 가장 유사한 이름 찾기
    def match_region(region, candidates):
        match, score = process.extractOne(region, candidates)
        return match

    fac_regions = fac_df[fac_x].tolist()
    pop_df["매칭지역"] = pop_df[pop_x].apply(lambda x: match_region(x, fac_regions))

    # 병합
    merged = pd.merge(
        pop_df[[pop_y, "매칭지역"]],
        fac_df[[fac_y, fac_x]],
        left_on="매칭지역",
        right_on=fac_x,
        how="inner"
    )

    # --- 그래프 3: 겹친 막대그래프 ---
    st.subheader("⚖️ 지역별 노인 인구수 & 복지시설 비교")
    fig3 = go.Figure(data=[
        go.Bar(name="노인 인구수", x=merged["매칭지역"], y=merged[pop_y]),
        go.Bar(name="복지시설 수", x=merged[fac_x], y=merged[fac_y])
    ])
    fig3.update_layout(
        barmode="group",
        template="plotly_white",
        title="지역별 노인 인구수 vs 복지시설 수 비교",
        xaxis_title="지역",
        yaxis_title="수량",
