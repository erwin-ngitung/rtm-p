import streamlit as st

# Create an empty container
placeholder = st.empty()

actual_email = "rtm-p.agora@gmail.com"
actual_password = "rtm-p"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Login App RTM-P")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.success("Login successful")


elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")

else:
    pass


