import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, State, Input, Output, no_update, set_props
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

df = pd.read_csv('statue_map/csv/updated_coordinates6.csv', encoding='unicode_escape')


#test commit
title = 'Sports Statues in US'
hover_title = df['Athlete']
hover_details = ['Description']
sort = df.sort_values('Athlete')
options = sort['Athlete']
options_2 = [dict(zip(df['Athlete'], df['Athlete']))]

#Plot map and layout
fig = px.scatter_mapbox(df, lat=df['LATITUDE'], lon=df['LONGITUDE'], #title=title,
                        color_discrete_sequence=["fuchsia"], zoom=4, height=1000, size=df['size'])
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":10,"l":0,"b":0})
fig.update_traces(hoverinfo="none", hovertemplate=None)

#Run Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dcc.Dropdown(options, id="searchbar", multi=False), dbc.Container([
    graph := dcc.Graph(id="graph-interactive", figure=fig, clear_on_unhover=True),
    hover_tt := dcc.Tooltip(id="graph-tooltip"),
    modal := dbc.Modal(id="modal", centered=True, is_open=False),
], id="container", fluid=True)

#callback for hover tooltip
@app.callback(
   Output(hover_tt, "show"),
   Output(hover_tt, "bbox"),
   Output(hover_tt, "children"),
   Input(graph, 'hoverData'))

def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df.iloc[num]
    img_src = df_row['image']
    name = df_row['Athlete']
    desc = df_row['Description']
    time = df_row['time']

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H5(f"{name} - {time}", style={"color": "darkblue", "overflowWrap": "break-word"}),
            #html.H3(f'{time}')
            #html.P(f"{desc}"),
        ], style={'width': '200px', 'whiteSpace': 'normal'})
    ]

    return True, bbox, children

#callback for modal window on click
@app.callback(
   [Output(modal, "is_open", allow_duplicate=True), Output(modal, "children", allow_duplicate=True)],
   Input(graph, 'clickData'),
   [State(modal, "is_open")],
   prevent_initial_call='initial_duplicate'
)

def display_click(clickData, is_open):
    if clickData is None:
        return is_open, no_update

    # clear hover tooltip
    set_props("graph-tooltip", { "show": False, "children": list() })

    pt = clickData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df.iloc[num]
    img_src = df_row['image']
    name = df_row['Athlete']
    desc = df_row['Description']
    time = df_row['time']
    location = df_row['Location']
    citystate = df_row['CityState']
    sculptor = df_row['Sculptor']
    citation = df_row['Citation']

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            dbc.ModalHeader(dbc.ModalTitle(f"{name}"), close_button=True, style={"color": "darkblue", "overflowWrap": "break-word"}),
            #html.H6(f'{location_1} - {citystate_1}'),
            dbc.ModalBody(f'{location} - {citystate}\nSculptor: {sculptor}, {time}', style={'white-space': 'pre-line'}),
            #dbc.ModalBody(f"Sculptor: {sculptor_1}, {time_1}"),
            dbc.ModalBody(f'{desc}'),
            dbc.ModalFooter(f'Citation: {citation}', style={'justifyContent': 'flex-start'})
        ],
                  )
    ]

    return True, children

#callback for searchbar typing
@app.callback(
    Output('searchbar', 'options'),
    Input('searchbar', 'search_value'),
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate

    return [o for o in options if search_value.title() in o]

#callback for searching and displaying modal with result
@app.callback(
    [Output(modal, "is_open"), Output(modal, "children")],
    [Input('searchbar', 'value')],
    [State(modal, "is_open")]
)
def search_result(search_result, is_open):
    if search_result is None:
        return is_open, no_update
    
    df_row = df.loc[search_result == df['Athlete'], :]
    img_src = df_row['image']
    img_src_1 = img_src.iloc[0]
    name = df_row['Athlete']
    name_1 = name.iloc[0]
    desc = df_row['Description']
    desc_1 = desc.iloc[0]
    time = df_row['time']
    time_1 = time.iloc[0]
    citystate = df_row['CityState']
    citystate_1 = citystate.iloc[0]
    location = df_row['Location']
    location_1 = location.iloc[0]
    sculptor = df_row['Sculptor']
    sculptor_1 = sculptor.iloc[0]
    citation = df_row['Citation']
    citation_1 = citation.iloc[0]

    children = [
        html.Div([
            html.Img(src=img_src_1, style={"width": "100%"}),
            dbc.ModalHeader(dbc.ModalTitle(f"{name_1}"), close_button=True, style={"color": "darkblue", "overflowWrap": "break-word"}),
            #html.H6(f'{location_1} - {citystate_1}'),
            dbc.ModalBody(f'{location_1} - {citystate_1}\nSculptor: {sculptor_1}, {time_1}', style={'white-space': 'pre-line'}),
            #dbc.ModalBody(f"Sculptor: {sculptor_1}, {time_1}"),
            dbc.ModalBody(f'{desc_1}'),
            dbc.ModalFooter(f'Citation: {citation_1}', style={'justifyContent': 'flex-start'})
        ],
                  )
    ]
    return True, children

#print(options)

#run app
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)