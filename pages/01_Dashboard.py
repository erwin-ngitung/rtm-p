import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from tools import anomaly_detection as dt
from tools import processing_data as pdt
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

col1, col2 = st.columns(2)

with col1:
    st.write('What kind moving time do you want?')

    if st.checkbox('Days'):
        spacing = st.slider("How the spacing time in day do you want?", 1, 30, 1)
        spacing = spacing * 24
    elif st.checkbox('Hours'):
        spacing = st.slider("How the spacing time in hours do you want?", 1, 24, 1)
    else:
        spacing = 1

with col2:
    st.write("Where the well and simulator do you want to monitor?")
    well = st.selectbox("Please choice one well!", ["L26E",
                                                    "L26F",
                                                    "L26G",
                                                    "L26H"])

    file_name = "data/dataset" + "_" + well + ".csv"
    data = pd.read_csv(file_name, sep=",")
    column_data = np.asarray(data.columns.values[1:])
    column_data = np.insert(column_data, 0, "All GG Temp")
    column_data = np.insert(column_data, 9, "GG Temp Avg")

    column = st.selectbox("Please choice one part simulator!", column_data)

# Monitoring Plot

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
st.markdown("<h3 style=\"text-align:center;\">Monitoring Well " + well + " Part " + column + "</h3>", unsafe_allow_html=True)

data = pdt.create_data(data)
# data.ewm(span=spacing).mean()

data.dropna(inplace=True)

if column == "All GG Temp":
    data_monitor = data.loc[:, ["TimeStamp",
                                "GG Temp 1",
                                "GG Temp 2",
                                "GG Temp 3",
                                "GG Temp 4",
                                "GG Temp 5",
                                "GG Temp 6",
                                "GG Temp 7",
                                "GG Temp 8"]]
    column = "GG Temp Avg"

else:
    data_monitor = data.loc[:, ["TimeStamp",
                                column]]

column_monitor = data_monitor.columns

colour = ["red", "black", "yellow", "blue", "grey", "brown", "purple", "pink"]

col3, col4 = st.columns(2)

with col3:
    high = float(st.number_input('Insert a highest limit for safety'))

with col4:
    low = float(st.number_input('Insert a lowest limit for safety'))

placeholder = st.empty()

with st.spinner('Wait for it...'):
    time.sleep(5)

colors = ["black",
          "blue",
          "yellow",
          "green",
          "brown",
          "grey",
          "red",
          "purple"]

fig, ax = plt.subplots()
j = 1
maxim = len(data)

while j <= maxim:
    with placeholder.container():
        for k in range(1, len(column_monitor)):
            ax.plot(range(0, j), data_monitor[column_monitor[k]].iloc[0:j], color=colors[k - 1])
            dataset = data.loc[0:j, ["TimeStamp",
                                     column]]

            value = dt.anomaly_detection_manual(dataset, column, high, low)

            for m in range(len(value)):
                ax.axvspan(value[m] - 5, value[m] + 5, facecolor='0.5')

        ax.set_xlim(0, maxim)
        ax.set_ylim(min(data_monitor[column_monitor[1]]), max(data_monitor[column_monitor[1]]))
        ax.set_title(str(data["TimeStamp"].iloc[j]))
        ax.legend(column_monitor[1:], loc=4, fontsize='xx-small')

        st.pyplot(fig)

        if len(value) > 0:
            st.write("Anomaly Detection Log Information")
            st.table(dataset.iloc[value])

        j += spacing

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)