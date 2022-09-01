import streamlit as st
from streamlit_multipage import MultiPage
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import time
import numpy as np
from tools import anomaly_detection as dt
from tools import processing_data as pdt
from tools import building_model as bd


def login(st, **state):
    # Create an empty container
    placeholder = st.empty()

    actual_email = "rtm-p.agora@gmail.com"
    actual_password = "rtm-p"

    # Insert a form in the container
    with placeholder.form("login"):
        image = Image.open("images/logo_rtm-p.png")
        st1, st2, st3 = st.columns(3)

        with st2:
            st.image(image)

        st.markdown("#### Login App RTM-P")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit and email == actual_email and password == actual_password:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
        MultiPage.save({"login": "True"})

    elif submit and email != actual_email and password != actual_password:
        st.error("Login failed")
        MultiPage.save({"login": "False"})

    else:
        MultiPage.save({"login": "False"})
        pass


def dashboard(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Dashboard</h3>", unsafe_allow_html=True)

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
    st.markdown("<h3 style=\"text-align:center;\">Monitoring Well " + well + " Part " + column + "</h3>",
                unsafe_allow_html=True)

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
            ax.set_xlabel("Index")
            ax.set_ylabel(pdt.unit(column))
            ax.legend(column_monitor[1:], loc=4, fontsize='xx-small')

            st.pyplot(fig)

            if len(value) > 0:
                st.write("Anomaly Detection Log Information")
                st.table(dataset.iloc[value])

            j += spacing

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


def insight(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Data Insight</h3>", unsafe_allow_html=True)

    st.write("Where the well do you want to get more information?")
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
    st.markdown("<h3 style=\"text-align:center;\">Graph Insight Well " + well + " Part " + column + "</h3>",
                unsafe_allow_html=True)

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
    plt.xlabel("Year")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Year'))
    st.pyplot(fig)

    fig = plt.figure(figsize=(15, 5))
    data_quarter[column].agg('mean').plot()
    plt.xlabel("Quarter")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Quarter'))
    st.pyplot(fig)

    fig = plt.figure(figsize=(15, 5))
    data_month[column].agg('mean').plot()
    plt.xlabel("Month")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Month'))
    st.pyplot(fig)

    fig = plt.figure(figsize=(15, 5))
    data_day[column].agg('mean').plot()
    plt.xlabel("Days")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Day'))
    st.pyplot(fig)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


def deployment(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Deployment Model</h3>", unsafe_allow_html=True)

    well = st.selectbox("Please choice the well!", ["L26E",
                                                    "L26F",
                                                    "L26G",
                                                    "L26H"])
    file_name = "data/dataset" + "_" + well + ".csv"
    data = pd.read_csv(file_name, sep=",")
    data = pdt.create_data(data)
    # data.ewm(span=spacing).mean()
    
    data.dropna(inplace=True)

    # st.dataframe(data)

    column_feature = data.columns.values[1:]

    feature = st.selectbox("Please choice one column as feature anomaly detection!", column_feature)

    col5, col6 = st.columns(2)

    with col5:
        high = float(st.number_input('Insert a highest limit for safety'))

    with col6:
        low = float(st.number_input('Insert a lowest limit for safety'))

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Building Model</h3>", unsafe_allow_html=True)

    with st.spinner('Wait for it...'):
        time.sleep(5)

    data_ml = dt.anomaly_detection(data, high, low, feature)

    model_ml = st.radio("Please select model deep learning do you want!", ('LSTM',
                                                                           'CNN',
                                                                           'DeepAR',
                                                                           'ANN'))

    train_size = float(st.number_input('Please input train size do you want! (value: 0 - 1)'))

    if model_ml == "LSTM":
        model, history = bd.model_lstm(data, data_ml, train_size)
    else:
        pass

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Accuracy Model</h3>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(history.history['acc'], label='Train Accuracy')
    ax.plot(history.history['val_acc'], label='Test Accuracy')
    ax.set_ylim(0, 1)
    ax.set_itle('Model Accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epochs')
    ax.legend(loc='upper right')

    st.pyplot(fig)


def messages(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Messages</h3>", unsafe_allow_html=True)


def account(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Account Setting</h3>", unsafe_allow_html=True)


def logout(st, **state):
    st.write("Your account has been log out from this app")
    MultiPage.save({"login": "False"})


app = MultiPage()
app.st = st

app.navbar_name = "Menu"
app.navbar_style = "VerticalButton"

app.hide_menu = False
app.hide_navigation = True

app.add_app("Login", login)
app.add_app("Dashboard", dashboard)
app.add_app("Data Insight", insight)
app.add_app("Deployment Model", deployment)
app.add_app("Messages", messages)
app.add_app("Account Setting", account)
app.add_app("Logout", logout)

app.run()
