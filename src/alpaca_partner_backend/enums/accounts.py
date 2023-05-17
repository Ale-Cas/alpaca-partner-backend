"""Enumerations for the accounts router."""


from enum import Enum


class CountryCode(str, Enum):
    """
    Country codes for country_of_citizenship, country_of_citizenship and country_of_tax_residence.

    see: https://alpaca.markets/docs/api-references/broker-api/accounts/accounts/#the-account-model
    """

    USA = "USA"
    ITA = "Italy"
    FRA = "France"
