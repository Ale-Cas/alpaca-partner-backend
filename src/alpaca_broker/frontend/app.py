"""Streamlit app."""

from datetime import date, datetime

import streamlit as st
from alpaca.broker import (
    Agreement,
    AgreementType,
    Contact,
    CreateAccountRequest,
    Disclosures,
    Identity,
)

from alpaca_broker.api.routes.accounts import create_account
from alpaca_broker.enums.accounts import CountryCode

st.title("Alpaca Example Trading App")


form_tabs = st.tabs(["Contact & Identity", "Disclosures & Agreements"])

with st.form("Create an account"):
    with form_tabs[0]:
        name_cols = st.columns(2)
        with name_cols[0]:
            given_name = st.text_input("Enter your first name")
        with name_cols[1]:
            family_name = st.text_input("Enter your last name")
        contact_cols = st.columns(2)
        with contact_cols[0]:
            email_address = st.text_input("Enter your email")
        with contact_cols[1]:
            phone_number = st.text_input("Enter your phone number")
        date_of_birth = st.date_input("When's your birthday", date(year=1997, month=12, day=14)).strftime("%Y-%m-%d")  # type: ignore
        contact_cols = st.columns(3)
        with contact_cols[0]:
            street_address = [st.text_input("Enter your street address")]
        with contact_cols[1]:
            city = st.text_input("City")
        with contact_cols[2]:
            state = st.text_input("State")
        country_of_tax_residence = CountryCode(
            st.selectbox("Country of tax residence", options=[c.value for c in list(CountryCode)])
        )
        contact = Contact(
            email_address=email_address,
            phone_number=phone_number,
            street_address=street_address,
            city=city,
            state=state,
        )
        identity = Identity(
            given_name=given_name,
            family_name=family_name,
            country_of_tax_residence=country_of_tax_residence,
            date_of_birth=date_of_birth,
        )
        disclosures = Disclosures(
            immediate_family_exposed=False,
            is_affiliated_exchange_or_finra=False,
            is_control_person=False,
            is_politically_exposed=False,
        )
        agreements = [
            Agreement(
                agreement=AgreementType.CUSTOMER,
                signed_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                ip_address="185.13.21.99",
                revision="19.2022.02",
            )
        ]

    submitted = st.form_submit_button("Submit account creation request.")
    if submitted:
        account = create_account(
            account_request=CreateAccountRequest(
                contact=contact,
                identity=identity,
                disclosures=disclosures,
                agreements=agreements,
            )
        )
