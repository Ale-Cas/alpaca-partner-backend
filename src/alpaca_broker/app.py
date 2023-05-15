"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"alpaca-broker v{version('alpaca-broker')}")  # type: ignore[no-untyped-call]
