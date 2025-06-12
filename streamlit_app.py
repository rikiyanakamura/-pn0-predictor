import streamlit as st
import pandas as pd
import joblib

# モデル読み込み
model = joblib.load("pn0_model.pkl")

# アプリタイトル
st.title("乳がんリンパ節転移陰性（pN0）予測ツール")

# 入力項目
age = st.number_input("年齢", min_value=20, max_value=100, value=50)
height = st.number_input("身長 (cm)", min_value=120, max_value=200, value=160)
weight = st.number_input("体重 (kg)", min_value=30, max_value=150, value=55)
us_diameter = st.number_input("US径 (mm)", min_value=0, max_value=100, value=15)
cER = st.slider("cER (%)", 0, 100, 90)
cPgR = st.slider("cPgR (%)", 0, 100, 70)

axilla_diag = st.selectbox("腋窩診断", ["画像上転移なし", "FNA陰性", "CNB陰性"])
menopause = st.selectbox("閉経", ["前", "後"])
ct = st.selectbox("cT", ["T1", "T1c", "T2", "T3", "その他"])
biopsy_type = st.selectbox("CNB組織型", ["浸潤性乳管癌", "浸潤性小葉癌", "その他"])
chg = st.selectbox("cHG", ["1", "2", "3"])
cher2 = st.selectbox("cHER2", ["陰性", "陽性"])
her2_protein = st.selectbox("HER2蛋白", ["陰性", "1+", "2+", "3+"])

# 入力データをDataFrame形式に
input_data = pd.DataFrame([{
    "年齢": age,
    "身長": height,
    "体重": weight,
    "US径": us_diameter,
    "cER(%)": cER,
    "cPgR(%)": cPgR,
    "腋窩診断": axilla_diag,
    "閉経": menopause,
    "cT": ct,
    "CNB組織型": biopsy_type,
    "cHG": chg,
    "cHER2": cher2,
    "HER2蛋白": her2_protein
}])

# 予測
if st.button("予測する"):
    prob = model.predict_proba(input_data)[0][1]
    st.write(f"転移陰性（pN0）の予測確率：**{prob:.2%}**")
    if prob >= 0.9:
        st.success("転移陰性の可能性が高いです。観察や縮小治療の候補になり得ます。")
    elif prob >= 0.7:
        st.info("やや転移陰性の可能性が高いですが、慎重な判断が必要です。")
    else:
        st.warning("転移の可能性があり、標準的な評価・治療が推奨されます。")