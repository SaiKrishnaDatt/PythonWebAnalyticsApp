#Credits to Charming Data Youtube tutor.
#Modified By : KrishnaDutt
import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("casesData.csv")

df = df.groupby(["State", "ANSI", "Affected by", "Year", "state_code"])[
    ["Pct of Colonies Impacted"]
].mean()
df.reset_index(inplace=True)
print(df[:5])

colors = {
    'background': '#a9a9a9',
    'text': '#7FDBFF'
}
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1("Cases: State and year wise data ", style={"text-align": "center"}),
        dcc.Slider(
            id="slct_year",
            min=2015,
            max=2018,
            step=None,
            marks={2015: "2015", 2016: "2016", 2017: "2017", 2018: "2018"},
            value=2015,
        ),
        dcc.Dropdown(
            id="slct_state",
            options=[
                {"label": "Delaware", "value": "Delaware"},
                {"label": "Pennsylvania", "value": "Pennsylvania"},
                {"label": "New Jersey", "value": "New Jersey"},
                {"label": "Georgia", "value": "Georgia"},
                {"label": "Connecticut", "value": "Connecticut"},
                {"label": "Massachusetts", "value": "Massachusetts"},
                {"label": "Maryland", "value": "Maryland"},
                {"label": "South Carolina", "value": "South Carolina"},
                {"label": "New Hampshire", "value": "New Hampshire"},
                {"label": "Virginia", "value": "Virginia"},
                {"label": "New York", "value": "New York"},
                {"label": "North Carolina", "value": "North Carolina"},
                {"label": "Rhode Island", "value": "Rhode Island"},
                {"label": "Vermont", "value": "Vermont"},
                {"label": "Kentucky", "value": "Kentucky"},
                {"label": "Tennessee", "value": "Tennessee"},
                {"label": "Ohio", "value": "Ohio"},
                {"label": "Louisiana", "value": "Louisiana"},
                {"label": "Indiana", "value": "Indiana"},
                {"label": "Mississippi", "value": "Mississippi"},
                {"label": "Illinois", "value": "Illinois"},
                {"label": "Alabama", "value": "Alabama"},
                {"label": "Maine", "value": "Maine"},
                {"label": "Missouri", "value": "Missouri"},
                {"label": "Arkansas", "value": "Arkansas"},
                {"label": "Michigan", "value": "Michigan"},
                {"label": "Florida", "value": "Florida"},
                {"label": "Texas", "value": "Texas"},
                {"label": "Iowa", "value": "Iowa"},
                {"label": "Wisconsin", "value": "Wisconsin"},
                {"label": "California", "value": "California"},
                {"label": "Minnesota", "value": "Minnesota"},
                {"label": "Oregon", "value": "Oregon"},
                {"label": "Kansas", "value": "Kansas"},
                {"label": "West Virginia", "value": "West Virginia"},
                {"label": "Nevada", "value": "Nevada"},
                {"label": "Nebraska", "value": "Nebraska"},
                {"label": "Colorado", "value": "Colorado"},
                {"label": "North Dakota", "value": "North Dakota"},
                {"label": "South Dakota", "value": "South Dakota"},
                {"label": "Montana", "value": "Montana"},
                {"label": "Washington", "value": "Washington"},
                {"label": "Idaho", "value": "Idaho"},
                {"label": "Wyoming", "value": "Wyoming"},
                {"label": "Utah", "value": "Utah"},
                {"label": "Oklahoma", "value": "Oklahoma"},
                {"label": "New Mexico", "value": "New Mexico"},
                {"label": "Arizona", "value": "Arizona"},
                {"label": "Alaska", "value": "Alaska"},
                {"label": "Hawaii", "value": "Hawaii"},
            ],
            multi=True,
            value="Alabama",
            style={"width": "40%"},
        ),
        html.Div(id="output_container", children=[],),
        html.Br(),
        dcc.Graph(id="my_bee_map", figure={}),
        dcc.Graph(id="my_bee_map2", figure={}),
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="my_bee_map", component_property="figure"),
        Output(component_id="my_bee_map2", component_property="figure"),
    ],
    [
        Input(component_id="slct_year", component_property="value"),
        Input(component_id="slct_state", component_property="value"),
    ],
)
def update_graph(option_slctd, option_slct_state):


    container = "Year Range: 2015 - {}".format(option_slctd)
    
    dff = df.copy()
    print(dff)
    print(type(dff))
    yearSelected = [];
    for i in range(2015, option_slctd + 1):
        #yearSelected.append(str(i));
        yearSelected.append(i);
    dff = dff[dff["Year"].isin(yearSelected)]

    if isinstance(option_slct_state, str):
        values= [option_slct_state];
    else :
        values = option_slct_state;
    dff = dff[dff["State"].isin(values)]

    # if option_slct_state == []:
    #     values = dff[dff["State"].values[0];
    # else
    # dff = dff[dff["State"] == option_slct_state]

    # if type(option_slct_state) == 'str':
    #     dff = dff[dff["State"] == option_slct_state];
    # else:
    #     dff = dff[dff["State"] ==  [for currstate in option_slct_state]


    # Plotly Graph Objects(GO)
    fig1 = px.bar(
        data_frame=dff,
        x="Year",
        y="Pct of Colonies Impacted",
        hover_data=["State", "Pct of Colonies Impacted"],
        labels={"Pct of Colonies Impacted": "% of Cases"},
        template="plotly_dark",
        title="Year-wise representation",
        color = "State",
        barmode="group"
    )

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="Pct of Colonies Impacted",
        hover_data=["State", "Pct of Colonies Impacted"],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={"Pct of Colonies Impacted": "% of Cases"},
        template="plotly_dark",
    )

    return container, fig1, fig


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(host="localhost", port=8900, debug=True)
