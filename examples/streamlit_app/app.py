import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Free API DS Edu", layout="wide")
st.title("무료 API 데이터 과학 수업 예제")

api = st.selectbox("API 선택", ["Open-Meteo 현재 서울 날씨", "World Bank 한국 인구", "서울 따릉이 샘플"])

if api.startswith("Open-Meteo"):
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=Asia%2FSeoul"
    data = requests.get(url, timeout=10).json()
    st.json(data["current"])
    st.metric("기온", f"{data['current']['temperature_2m']} °C")

elif api.startswith("World Bank"):
    url = "https://api.worldbank.org/v2/country/KOR/indicator/SP.POP.TOTL?format=json&per_page=20"
    data = requests.get(url, timeout=10).json()[1]
    df = pd.DataFrame(data)[["date", "value"]].dropna()
    df["date"] = pd.to_numeric(df["date"])
    df = df.sort_values("date")
    st.line_chart(df, x="date", y="value")
    st.dataframe(df)

else:
    url = "http://openapi.seoul.go.kr:8088/sample/json/bikeList/1/20/"
    rows = requests.get(url, timeout=10).json()["rentBikeStatus"]["row"]
    df = pd.DataFrame(rows)
    for col in ["parkingBikeTotCnt", "stationLatitude", "stationLongitude"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    st.dataframe(df[["stationName", "parkingBikeTotCnt", "stationLatitude", "stationLongitude"]])
    st.map(df.rename(columns={"stationLatitude": "lat", "stationLongitude": "lon"}))
