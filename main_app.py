import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
import matplotlib.animation as animation
import streamlit.components.v1 as components
import datetime as dt

# Title
st.markdown("<h1 style=\"text-align:center;\">Real Time Prediction Monitoring</h1>", unsafe_allow_html=True)
st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<b>Hello, Mr.Johson</b>", unsafe_allow_html=True)
well = st.sidebar.selectbox("Where the well do you want to monitor?", ["L26E",
                                                                       "L26F",
                                                                       "L26G",
                                                                       "L26H"])

st.sidebar.markdown('What kind moving time do you want?')

if st.sidebar.button('Days'):
    spacing = st.sidebar.slider("How the spacing time in day do you want?", 1, 30, 1)
elif st.sidebar.button('Hours'):
    spacing = st.sidebar.slider("How the spacing time in hours do you want?", 1, 24, 1)
    spacing = spacing / 24
else:
    spacing = 1

file_name = "data/data_source" + "_" + well + ".csv"
data = pd.read_csv(file_name, sep=",")
column_data = data.columns.values
data.ewm(span=spacing).mean()

data.dropna(inplace=True)

data_monitor = data.loc[:, ["L26E1 - GG Temp 1",
                            "L26E2 - GG Temp 2",
                            "L26E3 - GG Temp 3",
                            "L26E4 - GG Temp 4",
                            "L26E5 - GG Temp 5",
                            "L26E6 - GG Temp 6",
                            "L26E7 - GG Temp 7",
                            "L26E8 - GG Temp 8"]]
column_monitor = data_monitor.columns.values

# Monitoring Plot
st.markdown("Monitoring Plot Well " + well)

placeholder = st.empty()

fig, ax = plt.subplots()
j = 1

while j <= 10000:
    with placeholder.container():
        for k in range(len(column_monitor)):
            ax.plot(range(0, j), data_monitor[column_monitor[k]].iloc[0:j])

        ax.set_xlim(0, 10000)
        ax.set_ylim(min(data_monitor[column_monitor[1]]), max(data_monitor[column_monitor[1]]))
        ax.set_title("GG Compressor on " + str(data["TimeStamp"].iloc[j]))
        ax.grid()
        ax.legend(column_monitor, loc=4, fontsize='xx-small')

        st.pyplot(fig)

        j += spacing
