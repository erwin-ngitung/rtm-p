import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tools import processing_data as pdt
from PIL import Image
import time

# Title

image = Image.open("images/logo_rtm-p.png")
st1, st2, st3 = st.columns(3)

with st2:
    st.image(image)

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
st.markdown("<h3 style=\"text-align:center;\">Data Preparation</h3>", unsafe_allow_html=True)

st.write("Where the well do you want to monitor?")
well = st.selectbox("Please choice one!", ["L26E",
                                            "L26F",
                                            "L26G",
                                            "L26H"])

# Monitoring Plot

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

file_name = "data/dataset" + "_" + well + ".csv"
data = pd.read_csv(file_name, sep=",")
column_data = data.columns.values
data = pdt.create_data(data)
# data.ewm(span=spacing).mean()

data.dropna(inplace=True)

data["TimeStamp"] = pd.to_datetime(data['TimeStamp'])
data["Year"] = data['TimeStamp'].dt.year
data["Quarter"] = data['TimeStamp'].dt.quarter
data["Month"] = data['TimeStamp'].dt.month
data["Day"] = data['TimeStamp'].dt.day
data["Hours"] = data['TimeStamp'].dt.hour
data["Minutes"] = data['TimeStamp'].dt.minute

data_year = data.groupby('Year')
data_quarter = data.groupby('Quarter')
data_month = data.groupby('Month')
data_day = data.groupby('Day')

with st.spinner('Wait for it...'):
    time.sleep(5)

fig = plt.figure(figsize=(15, 5))
data_year["GG Temp Avg"].agg('mean').plot()
plt.xlabel('')
plt.title('Temperature Average GG Combust by Year')
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_quarter["GG Temp Avg"].agg('mean').plot()
plt.xlabel('')
plt.title('Temperature Average GG Combust by Quarter')
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_month["GG Temp Avg"].agg('mean').plot()
plt.xlabel('')
plt.title('Temperature Average GG Combust by Month')
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_day["GG Temp Avg"].agg('mean').plot()
plt.xlabel('')
plt.title('Temperature Average GG Combust by Day')
st.pyplot(fig)

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
