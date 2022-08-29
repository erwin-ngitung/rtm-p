import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tools import processing_data as pdt
from PIL import Image
import time
import numpy as np

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
file_name = "data/dataset" + "_" + well + ".csv"
data = pd.read_csv(file_name, sep=",")
column_data = np.asarray(data.columns.values[1:])
column_data = np.insert(column_data, 8, "GG Temp Avg")

column = st.selectbox("Please choice one part simulator!", column_data)

# Monitoring Plot

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

data = pdt.create_data(data)
# data.ewm(span=spacing).mean()

data.dropna(inplace=True)

dataset = data.loc[:, ["TimeStamp",
                       column]]
dataset["TimeStamp"] = pd.to_datetime(dataset['TimeStamp'])
dataset["Year"] = dataset['TimeStamp'].dt.year
dataset["Quarter"] = dataset['TimeStamp'].dt.quarter
dataset["Month"] = dataset['TimeStamp'].dt.month
dataset["Day"] = dataset['TimeStamp'].dt.day
dataset["Hours"] = dataset['TimeStamp'].dt.hour
dataset["Minutes"] = dataset['TimeStamp'].dt.minute

data_year = dataset.groupby('Year')
data_quarter = dataset.groupby('Quarter')
data_month = dataset.groupby('Month')
data_day = dataset.groupby('Day')

with st.spinner('Wait for it...'):
    time.sleep(5)

fig = plt.figure(figsize=(15, 5))
data_year[column].agg('mean').plot()
plt.xlabel('')
plt.title(str('Data Insight ' + column + ' by Year'))
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_quarter[column].agg('mean').plot()
plt.xlabel('')
plt.title(str('Data Insight ' + column + ' by Quarter'))
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_month[column].agg('mean').plot()
plt.xlabel('')
plt.title(str('Data Insight ' + column + ' by Month'))
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
data_day[column].agg('mean').plot()
plt.xlabel('')
plt.title(str('Data Insight ' + column + ' by Day'))
st.pyplot(fig)

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
