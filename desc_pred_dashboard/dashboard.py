import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------------
# Load and Prepare the Dataset
# -------------------------------
df = pd.read_csv("superstore_sales.csv", encoding="latin-1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

# -------------------------------
#  Predictive Analysis
# -------------------------------
sales_trend = df.groupby("YearMonth")["Sales"].sum().reset_index()
sales_trend["t"] = np.arange(len(sales_trend))
model = LinearRegression()
model.fit(sales_trend[["t"]], sales_trend["Sales"])
sales_trend["Predicted"] = model.predict(sales_trend[["t"]])

# -------------------------------
#  Create Dash App
# -------------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Sales Dashboard with Descriptive & Predictive Insights"),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            options=[{"label": r, "value": r} for r in df["Region"].unique()],
            value=df["Region"].unique()[0],
            id="region-filter",
            multi=False
        ),
    ], style={"width": "25%", "display": "inline-block"}),

    # Graphs
    dcc.Graph(id="sales-by-category"),
    dcc.Graph(id="sales-trend"),
    dcc.Graph(id="category-share")
])

# -------------------------------
#  Callbacks for Interactivity
# -------------------------------
@app.callback(
    [Output("sales-by-category", "figure"),
     Output("sales-trend", "figure"),
     Output("category-share", "figure")],
    Input("region-filter", "value")
)
def update_dashboard(selected_region):
    filtered_df = df[df["Region"] == selected_region]

    # 1. Bar Chart – Sales by Category
    bar_fig = px.bar(filtered_df.groupby("Category")["Sales"].sum().reset_index(),
                     x="Category", y="Sales", title=f"Sales by Category ({selected_region})",
                     color="Category")

    # 2. Line Chart – Sales Trend (with Prediction)
    trend = sales_trend.copy()
    line_fig = px.line(trend, x="YearMonth", y=["Sales", "Predicted"],
                       title="Sales Trend & Prediction")

    # 3. Pie Chart – Category Sales Share
    pie_fig = px.pie(filtered_df, names="Category", values="Sales",
                     title=f"Category Share ({selected_region})")

    return bar_fig, line_fig, pie_fig


# -------------------------------
# Run the Dashboard
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)