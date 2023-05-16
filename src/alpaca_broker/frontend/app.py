"""Streamlit app."""


import streamlit as st

from alpaca_broker.frontend.sign_up import load_sign_up_screen

st.set_page_config(
    page_title="Alpaca Example",
    page_icon="🦙",
)


st.title("Alpaca Example Trading App")
with st.sidebar, st.form("Login"):
    email_address = st.text_input("Email")
    password = st.text_input("Password")
    submitted = st.form_submit_button("Log in", use_container_width=True)
    if submitted:
        submitted
sign_up_clicked = st.sidebar.button("Sign up", use_container_width=True)
load_sign_up_screen(sign_up_clicked)
