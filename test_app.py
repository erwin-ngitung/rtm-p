import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
import matplotlib.animation as animation
import streamlit.components.v1 as components

file_name = "data/data_source" + "_" + "L26E" + ".csv"
data = pd.read_csv(file_name, sep=",")
data = pd.read_csv(file_name, sep=",")
data_monitor = data.loc[:, ["TimeStamp",
                            "L26E1 - GG Temp 1",
                            "L26E2 - GG Temp 2",
                            "L26E3 - GG Temp 3",
                            "L26E4 - GG Temp 4",
                            "L26E5 - GG Temp 5",
                            "L26E6 - GG Temp 6",
                            "L26E7 - GG Temp 7",
                            "L26E8 - GG Temp 8"]]
column = data_monitor.columns.values

# # Create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# x = []
# y = []
#
#
# # This function is called periodically from FuncAnimation
# def animate(i, x, y):
#     # Read temperature (Celsius) from TMP102
#
#     # Add x and y to lists
#     x.append(data_monitor["TimeStamp"].iloc[i])
#     y.append(data_monitor["L26E1 - GG Temp 1"].iloc[i])
#
#     # Draw x and y lists
#     ax.clear()
#     ax.plot(x, y)
#
#     # Format plot
#     plt.xticks(rotation=90, ha='right')
#     plt.subplots_adjust(bottom=0.30)
#     plt.title('GG Temperature')
#     plt.ylabel('Temperature (deg C)')
#
#
# # Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(x, y), interval=1000)
#
# components.html(ani.to_html5_video(), height=900, width=900)

data.ewm(span=30).mean()

data.dropna(inplace=True)

print(data)