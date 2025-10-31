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

    # 컬럼 공백 제거
    pop_df.columns = pop_df.columns.str.strip()
    fac_df.columns = fac_df.columns.str.strip()

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

    # --- 문자열 기반 안전 매칭 ---
    pop_df[pop_x] = pop_df[pop_x].astype(str).str.strip().str.lower()
    fac_df[fac_x] = fac_df[fac_x].astype(str).str.strip().str.lower()

    # 단순히 일치하는 경우만 매칭, 안 맞으면 빈칸
    pop_df["매칭지역"] = pop_df[pop_x].apply(lambda x: x if x in fac_df[fac_x].values else "")

    # 숫자형 변환
    pop_df[pop_y] = pd.to_numeric(pop_df[pop_y], errors="coerce")
    fac_df[fac_y] = pd.to_numeric(fac_df[fac_y], errors="coerce")

    # 매칭 성공한 데이터만 병합
    pop_matched = pop_df[pop_df["매칭지역"] != ""].copy()
    fac_df_nonnull = fac_df[[fac_x, fac_y]].copy()
    merged = pd.merge(
        pop_matched[[pop_y, "매칭지역"]],
        fac_df_nonnull,
        left_on="매칭지역",
        right_on=fac_x,
        how="inner"
    )

    # --- 그래프 1 ---
    st.subheader("📊 1️⃣ 지역별 노인 인구수")
    fig1 = px.bar(pop_df, x=pop_x, y=pop_y, color=pop_y, text=pop_y)
    fig1.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="노인 인구수")
    st.plotly_chart(fig1, use_container_width=True)

    # --- 그래프 2 ---
    st.subheader("🏢 2️⃣ 지역별 복지시설 개수")
    fig2 = px.bar(fac_df, x=fac_x, y=fac_y, color=fac_y, text=fac_y)
    fig2.update_layout(template="plotly_white", xaxis_title="지역", yaxis_title="복지시설 수")
    st.plotly_chart(fig2, use_container_width=True)

    # --- 그래프 3 ---
    st.subheader("⚖️ 3️⃣ 지역별 노인 인구수 & 복지시설 비교")
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
        legend_title="구분"
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("👆 사이드바에서 두 개의 CSV 파일을 업로드해주세요.")
