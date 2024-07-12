import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def plot_wagner_law(df, country):
    df["original_period"] = pd.to_datetime(df["original_period"], errors="coerce")
    df = df.dropna(subset=["original_period"])
    df["date"] = df["original_period"].dt.strftime("%Y")
    df["customdata"] = df.apply(
        lambda row: [row["date"], row["GDP per Capita"], row["General Government Expenditure"]], axis=1
    )

    df = df.dropna(subset=["GDP per Capita", "General Government Expenditure"])

    fig = px.scatter(
        df,
        x="GDP per Capita",
        y="General Government Expenditure",
        title=f"Laffer curve for {country}",
        labels={
            "GDP per Capita": "GDP per Capita (constant 2015 US$)",
            "General Government Expenditure": " General government expenditure (constant 2015 US$) ",
        },
        custom_data=["date", "GDP per Capita", "General Government Expenditure"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "GDP per Capita in USD: %{customdata[1]}",
                "General Government Expenditure in USD : %{customdata[2]}",
            ]
        ),
        marker=dict(size=8, symbol="circle-open-dot"),
        selector=dict(mode="markers"),
    )

    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(df[["GDP per Capita"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, df["General Government Expenditure"])

    x_line = np.linspace(df["GDP per Capita"].min(), df["GDP per Capita"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Line",
            line=dict(color="Deeppink", width=3),
        )
    )

    return fig 

def plot_gov_expenditure(df, country_name):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["original_period"],
            y=df["General Government Expenditure"],
            mode="lines+markers",
            name="General Government Expenditure",
        )
    )

    fig.update_layout(
        title=f"Evolution of Government Expenditure for {country_name}",
        xaxis_title="Year",
        yaxis_title="General Government Expenditure",
        legend=dict(x=0, y=1),
        autosize=True,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig