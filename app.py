from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")

    # Load coffee export data
    csv_path = os.path.join(os.path.dirname(__file__), "coffee_exports.csv")
    df = pd.read_csv(csv_path)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Confirm required columns
    required_cols = ["Country", "Export_Tons", "Region"]
    if not all(col in df.columns for col in required_cols):
        return f"Error: Expected columns {required_cols} not found. Found: {list(df.columns)}"

    # Chart generation
    if chart_type == "bar":
        fig = px.bar(df, x="Country", y="Export_Tons", color="Region",
                     title="Coffee Exports (Tons) by Country")
    elif chart_type == "scatter":
        fig = px.scatter(df, x="Country", y="Export_Tons", color="Region",
                         title="Coffee Export Scatter Plot")
    else:
        fig = px.box(df, x="Country", y="Export_Tons", color="Region",
                     title="Coffee Export Distribution")

    # Dark theme
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

    # Convert to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)
