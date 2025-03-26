from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "scatter")

    # Load data
    csv_path = os.path.join(os.path.dirname(__file__), "coffee_exports.csv")
    df = pd.read_csv(csv_path)
    df.columns = [col.strip() for col in df.columns]

    required = ["Region", "Export_Tons", "Export_Value_USD", "Country"]
    if not all(col in df.columns for col in required):
        return f"Missing required columns. Found: {list(df.columns)}"

    if chart_type == "bar":
        grouped = df.groupby("Region", as_index=False).sum()
        fig = px.bar(grouped, x="Export_Tons", y="Export_Value_USD", color="Region",
                     title="Total Export Value vs Tons by Region")
    elif chart_type == "scatter":
        fig = px.scatter(df, x="Export_Tons", y="Export_Value_USD", color="Region",
                         hover_data=["Country", "Year"],
                         title="Scatter Plot: Export Tons vs Value by Region")
    else:  # box plot fallback
        fig = px.box(df, x="Region", y="Export_Value_USD", color="Region",
                     hover_data=["Country", "Year"],
                     title="Export Value Distribution by Region")

    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)
