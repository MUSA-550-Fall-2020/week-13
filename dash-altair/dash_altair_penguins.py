import dash
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import io
import pandas as pd

# load the data
penguins = pd.read_csv(
    "https://raw.githubusercontent.com/MUSA-550-Fall-2020/week-2/master/data/penguins.csv"
)

# initialize the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# set a title
app.title = "Testing Dash and Altair"

# columns to plot
COLUMNS = [
    "flipper_length_mm",
    "bill_length_mm",
    "body_mass_g",
    "bill_depth_mm",
]

# set the layout
app.layout = html.Div(
    [
        html.Div(
            [
                # Dropdown for x axis
                html.Div(
                    [
                        html.Label("x-axis"),
                        dcc.Dropdown(
                            id="x_axis",
                            options=[{"label": i, "value": i} for i in COLUMNS],
                            value="flipper_length_mm",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
                # Dropdown for y axis
                html.Div(
                    [
                        html.Label("y-axis"),
                        dcc.Dropdown(
                            id="y_axis",
                            options=[{"label": i, "value": i} for i in COLUMNS],
                            value="bill_length_mm",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
            ],
        ),
        # This is where the chart goes
        html.Iframe(
            id="plot",
            height="500",
            width="1000",
            sandbox="allow-scripts",
            style={"border-width": "0px"},
        ),
    ],
    style={"display": "flex", "justify-content": "center"},
)


@app.callback(
    dash.dependencies.Output("plot", "srcDoc"),
    [
        dash.dependencies.Input("x_axis", "value"),
        dash.dependencies.Input("y_axis", "value"),
    ],
)
def render(x_axis, y_axis):

    brush = alt.selection_interval()
    base = alt.Chart(penguins)

    # scatter plot of x vs y
    scatter = (
        base.mark_point()
        .encode(
            x=alt.X(x_axis, scale=alt.Scale(zero=False)),
            y=alt.Y(y_axis, scale=alt.Scale(zero=False)),
            color="species:N",
        )
        .properties(width=300, height=400, selection=brush)
    )

    # histogram of body mass
    hist = (
        base.mark_bar()
        .encode(x=alt.X("body_mass_g:Q", bin=True), y="count()", color="species:N")
        .transform_filter(brush.ref())
    ).properties(width=300, height=400)

    # the combined chart
    chart = alt.hconcat(scatter, hist)

    # SAVE TO HTML AND THEN RETURN
    # Save html as a StringIO object in memory
    chart_html = io.StringIO()
    chart.save(chart_html, "html")

    # Return the html from StringIO object
    return chart_html.getvalue()


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5000, debug=True)