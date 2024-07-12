import importlib.resources

import streamlit as st
from charts import plot_gov_expenditure, plot_wagner_law
from data_loader import download_data
from streamlit_option_menu import option_menu


def main() -> None:
    package_dir = importlib.resources.files("wagner_law")
    st.set_page_config(
        page_title="DBnomics Wagner's Law",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(":blue[Wagner Law]")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(package_dir / "assets/styles.css")

    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=[
                "Explanations",
                "Charts Wagner Law",
                "Charts Government Expenditure",
                "Sources",
                "DBnomics",
            ],
            icons=["book", "bar-chart", "bar-chart", "paperclip", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.header(":blue[What is Wagner's Law?]")
        st.write(
            "\n"
            "Wagner's Law is named after its creator, the German economist Adolph Wagner (1835-1917)."
            'He was a specialist in financial institutions and was part of a group of economists known as the "socialists of the chair".'
            "\n"
        )
        st.image(str(package_dir / "images/wagnerphoto.png"), width=200)
        st.write(
            "\n"
            "Wagner placed the state at the center of his economic theories: the state must ensure social cohesion by improving the conditions of the most disadvantaged.\n"
            "He advocated for the necessity of a welfare state.\n"
            "\n"
            'Thus, in 1872, he explained that "the more civilized society becomes, the more the state spends".\n'
            "In other words, state expenditures increase with the growth of income and wealth.\n"
            "Therefore, as GDP increases, state expenditures also increase. This assertion aligns with his conception of a highly interventionist state: the increase in expenditures is inevitable.\n"
            "It is even suggested that public expenditures tend to grow faster than economic activity.\n"
            "\n"
            "This is explained by the strong demand for non-market services created by economic development: health, education, culture, etc.\n"
            "At the same time, economic growth accompanied by industrialization requires investments that only states can undertake.\n"
            "\n"
            "The question is whether this relationship is still visible today in developed countries and emerging countries experiencing rapid economic growth.\n"
            "For both developed and emerging countries, there is a positive relationship between the increase in General Government Expenditure and the evolution of GDP per Capita.\n"
            "However, this relationship is not strictly linear.\n"
        )

    if selected == "Charts Wagner Law":
        countries = {
            "France": "FRA",
            "United States": "USA",
            "India": "IND",
            "Norway": "NOR",
            "Korea, Rep.": "KOR",
        }

        country_name = st.selectbox("Select a country", list(countries.keys()))
        country_code = countries[country_name]
        data = download_data()
        df = data[country_code]

        fig_wagner = plot_wagner_law(df, country_name)
        st.plotly_chart(fig_wagner)

    if selected == "Charts Government Expenditure":
        countries = {
            "France": "FRA",
            "United States": "USA",
            "India": "IND",
            "Norway": "NOR",
            "Korea, Rep.": "KOR",
        }

        country_name = st.selectbox("Select a country", list(countries.keys()))
        country_code = countries[country_name]
        data = download_data()
        df = data[country_code]

        fig_gov_exp = plot_gov_expenditure(df, country_name)
        st.plotly_chart(fig_gov_exp)

    if selected == "Sources":
        st.write(
            'GDP per Capita: [link](https://db.nomics.world/WB/WDI?dimensions=%7B"indicator"%3A%5B"NY.GDP.PCAP.KD"%5D%7D&tab=list)\n'
            "\n"
            'General Government Expenditure: [link](https://db.nomics.world/WB/WDI?dimensions=%7B"indicator"%3A%5B"NE.CON.GOVT.KD"%5D%7D&tab=list)\n'
        )

    if selected == "DBnomics":
        st.write("Visit DBnomics by clicking [here](https://db.nomics.world)")


if __name__ == "__main__":
    main()
