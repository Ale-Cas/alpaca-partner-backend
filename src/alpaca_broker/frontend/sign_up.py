"""Streamlit app."""

import logging
from datetime import date, datetime
from functools import partial

import streamlit as st
from alpaca.broker import (
    Account,
    Agreement,
    AgreementType,
    Contact,
    CreateAccountRequest,
    Disclosures,
    Identity,
)

from alpaca_broker.api.routes.accounts import create_account
from alpaca_broker.enums.accounts import CountryCode

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def _handle_account_submission(account_request: CreateAccountRequest) -> Account | None:
    """
    Helper callback to submit the account creation request.

    Parameters
    ----------
    `account_request`: CreateAccountRequest
        The parameters for the account request.

    Returns
    -------
    `Account | None`:
        The account that has been created or nothing if there was an error.
    """
    log.info(account_request.dict(exclude_none=True))
    account = create_account(account_request=account_request)
    if account:
        st.success(f"Account {account.account_number} created.")
        return account
    st.error("Error in creating the account.")
    return None


def load_sign_up_screen(sign_up_clicked: bool) -> None:
    """
    Get the sign up page in the streamlit app.

    Parameters
    ----------
    `sign_up_clicked`: bool
        Wether the sign up button has been clicked.
    """
    if sign_up_clicked:
        # form_tabs = st.tabs(["Contact & Identity", "Disclosures & Agreements"])

        with st.form("Create an account"):
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
                st.selectbox(
                    "Country of tax residence", options=[c.value for c in list(CountryCode)]
                )
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
            # password_cols = st.columns(2)
            # with password_cols[0]:
            #     password = st.text_input("Choose your password")
            # with password_cols[1]:
            #     password_confirm = st.text_input("Repeat your password")
            account_request = CreateAccountRequest(
                contact=contact,
                identity=identity,
                disclosures=disclosures,
                agreements=agreements,
            )
            st.form_submit_button(
                "Submit account creation request.",
                use_container_width=True,
                on_click=partial(_handle_account_submission, account_request),  # type: ignore
            )
