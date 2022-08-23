import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
import matplotlib.animation as animation
import streamlit.components.v1 as components
import datetime as dt
from PIL import Image

# Sidebar
image = Image.open("images/logo_rtm-p.png")
st.sidebar.image(image)
st.sidebar.markdown("<svg width=\"300\" height=\"2\"><line x1=\"0\" y1=\"2.5\" x2=\"300\" y2=\"2.5\" stroke=\"black\" "
                    "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

if st.sidebar.checkbox("About RTM-P 1.0"):
    st.sidebar.write("")
elif st.sidebar.checkbox("Recent"):
    st.sidebar.write("")
elif st.sidebar.checkbox("Account Settings"):
    st.sidebar.write("")
elif st.sidebar.checkbox("Contact Support"):
    st.sidebar.write("")
elif st.sidebar.checkbox("Log Out"):
    st.sidebar.write("")

st.sidebar.markdown("<svg width=\"300\" height=\"2\"><line x1=\"0\" y1=\"2.5\" x2=\"300\" y2=\"2.5\" stroke=\"black\" "
                    "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

st.sidebar.text_input("Address Account")
st.sidebar.text_area("Write Your Message")

st.sidebar.markdown("<svg width=\"300\" height=\"2\"><line x1=\"0\" y1=\"2.5\" x2=\"300\" y2=\"2.5\" stroke=\"black\" "
                    "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)

# Title
st.markdown("<h5>Hello, Mr.Johson</h5>", unsafe_allow_html=True)

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
st.markdown("<h3 style=\"text-align:center;\">Data Preparation</h3>", unsafe_allow_html=True)
st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.write('What kind moving time do you want?')

    if st.checkbox('Days'):
        spacing = st.slider("How the spacing time in day do you want?", 1, 30, 1)
    elif st.checkbox('Hours'):
        spacing = st.slider("How the spacing time in hours do you want?", 1, 24, 1)
        spacing = spacing / 24
    else:
        spacing = 1

with col2:
    st.write("Where the well do you want to monitor?")
    well = st.selectbox("Please choice one!", ["L26E",
                                               "L26F",
                                               "L26G",
                                               "L26H"])

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
colour = ["red", "black", "yellow", "blue", "grey", "brown", "purple", "pink"]
# Monitoring Plot

st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
st.markdown("<h3 style=\"text-align:center;\">Monitoring Well " + well + "</h3>", unsafe_allow_html=True)
st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
            "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


placeholder = st.empty()

fig, ax = plt.subplots()
j = 1
maxim = 10000

while j <= 10000:
    with placeholder.container():
        for k in range(len(column_monitor)):
            ax.plot(range(0, j), data_monitor[column_monitor[k]].iloc[0:j], co)

        ax.set_xlim(0, maxim)
        ax.set_ylim(min(data_monitor[column_monitor[1]]), max(data_monitor[column_monitor[1]]))
        ax.set_title(str(data["TimeStamp"].iloc[j]))
        ax.legend(column_monitor, loc=4, fontsize='xx-small')

        st.pyplot(fig)

        j += spacing
