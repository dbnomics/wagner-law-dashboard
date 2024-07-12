import pandas as pd
from dbnomics import fetch_series


def download_data():
    df_gdp = fetch_series(
        [
            "WB/WDI/A-NY.GDP.PCAP.KD-USA",
            "WB/WDI/A-NY.GDP.PCAP.KD-IND",
            "WB/WDI/A-NY.GDP.PCAP.KD-FRA",
            "WB/WDI/A-NY.GDP.PCAP.KD-NOR",
            "WB/WDI/A-NY.GDP.PCAP.KD-KOR",
        ]
    )

    df_exp = fetch_series(
        [
            "WB/WDI/A-NE.CON.GOVT.KD-USA",
            "WB/WDI/A-NE.CON.GOVT.KD-IND",
            "WB/WDI/A-NE.CON.GOVT.KD-FRA",
            "WB/WDI/A-NE.CON.GOVT.KD-NOR",
            "WB/WDI/A-NE.CON.GOVT.KD-KOR",
        ]
    )

    col_gdp = ["original_period", "value", "country (label)"]
    col_exp = ["original_period", "value", "country (label)"]

    countries = {
        "France": "FRA",
        "United States": "USA",
        "India": "IND",
        "Norway": "NOR",
        "Korea, Rep.": "KOR",
    }

    data_wag = {}
    for country, code in countries.items():
        df_gdp_country = df_gdp[df_gdp["country (label)"] == country][col_gdp].rename(
            columns={"value": "GDP per Capita"}
        )
        df_exp_country = df_exp[df_exp["country (label)"] == country][col_exp].rename(
            columns={"value": "General Government Expenditure"}
        )

        df_country = pd.merge(df_gdp_country, df_exp_country, on="original_period")
        data_wag[code] = df_country

    return data_wag
