import pandas as pd
import datetime
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_extensions import Download

#Local
from tools import data_generator, gas_plot, gases_plot, color_dict, marker_mode_dict

#I) Congig
df_group = data_generator(n_hours=4000)
gas = 'CO2'
start_date = df_group.index.min()
end_date = df_group.index.max()
# y_range = [int(df_group[gas]['min'].min() - 0.2*df_group[gas]['min'].min()),
#            int(df_group[gas]['max'].max() + 0.2*df_group[gas]['max'].max())]
y_range = (0,160)

fig = gas_plot(
    df_group, 
    gas = gas, 
    x_range=['2021-06-03', '2021-06-26']
)

# II) COMPONENT

# 1) Time interval
date_picker = dcc.DatePickerRange(
    start_date=start_date, end_date=end_date, id="date_picker"
)

# 2) Concentration range (y axis)
y_range_slider = (
    dcc.RangeSlider(
        id="y_range_slider", min=y_range[0], max=y_range[1], step=1, value=y_range
    ),
)

# 3) CO2 and NO2 check boxes
gas_check_list = dcc.Checklist(
    id="gas_check_list",
    options=[
        {"label": "CO2", "value": "CO2"},
        {"label": "NO2", "value": "NO2"},
    ],
    value=["CO2"],
    labelStyle = {'margin-right': '20px'}
)

# 4) Graph
graph = dcc.Graph(figure=fig, id="graph")

# 5) Four color input for CO2 mean/std, NO2 mean/std
CO2_mean_color = dbc.Input(
    type="color",
    id="CO2_mean_color",
    name="CO2 mean",
    value=color_dict["CO2"]["mean"],
)
CO2_std_color = dbc.Input(
    type="color",
    id="CO2_std_color",
    name="CO2 std",
    value=color_dict["CO2"]["std"],
)
NO2_mean_color = dbc.Input(
    type="color",
    id="NO2_mean_color",
    name="NO2 mean",
    value=color_dict["NO2"]["mean"],
)
NO2_std_color = dbc.Input(
    type="color",
    id="NO2_std_color",
    name="NO2 std",
    value=color_dict["NO2"]["std"],
)

# 6) Marker mode dropdown
CO2_marker = dcc.Dropdown(
    id='CO2_marker',
    options=[
        {'label': 'Lines and markers', 'value': 'lines+markers'},
        {'label': 'Lines', 'value': 'lines'},
        {'label': 'Markers', 'value': 'markers'}
    ],
    value='lines+markers'
)
NO2_marker = dcc.Dropdown(
    id='NO2_marker',
    options=[
        {'label': 'Lines and markers', 'value': 'lines+markers'},
        {'label': 'Lines', 'value': 'lines'},
        {'label': 'Markers', 'value': 'markers'}
    ],
    value='lines+markers'
)

# 7) Download button
csv_button = html.Div(
    [
        html.Button("Download CSV", id="download_csv_button", n_clicks=0),
    ]
)

#Layout
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div(
    [
        html.H3("Daily Astrospheric NO2 and CO2 Concentration", style = {'text-align':'center', 'margin' : 'auto'}),
        
        html.Div(
            date_picker, 
            style = {'text-align':'center', 'margin' : 'auto', 'padding-top' : '1em'}
            ),

        html.Div(
            f'Concentration range: {y_range}', 
            id = 'y_range_putput',
            style = {'text-align':'center', 'margin' : 'auto', 'padding-top' : '1em'}
            ),

        html.Div(
            y_range_slider, 
            style = {'text-align':'center', 'margin' : 'auto', 'width' : '40%'},
            ),

        html.Div(
            gas_check_list, 
            style = {'text-align':'center', 'margin' : 'auto'}
            ),

        html.Div(
            graph, 
            style = {'text-align':'center', 'margin' : 'auto'}
            ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(CO2_mean_color, style = {'display': 'inline-block', 'width' : '72px'}),
                        html.Div('CO2 mean', style = {'display': 'inline-block', 'padding-left' : '0.5em' }),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),

                html.Div(
                    [
                        html.Div(CO2_std_color, style = {'display': 'inline-block', 'width' : '72px'}),
                        html.Div('CO2 std', style = {'display': 'inline-block', 'padding-left' : '0.5em' }),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),

                html.Div(
                    [
                        html.Div(NO2_mean_color, style = {'display': 'inline-block', 'width' : '72px'}),
                        html.Div('NO2 mean', style = {'display': 'inline-block', 'padding-left' : '0.5em' }),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),

                html.Div(
                    [
                        html.Div(NO2_std_color, style = {'display': 'inline-block', 'width' : '72px'}),
                        html.Div('NO2 std', style = {'display': 'inline-block', 'padding-left' : '0.5em' }),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),
            ],
            style = {'text-align':'center', 'margin' : 'auto'}
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(CO2_marker, style = {'display': 'inline-block', 'width' : '14em'}),
                        html.Label('CO2 marker', style = {'display': 'inline-block', 'padding-left' : '0.5em' }),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),

                html.Div(
                    [
                        html.Div(NO2_marker, style = {'display': 'inline-block', 'width' : '14em'}),
                        html.Label('NO2 marker', style = {'display': 'inline-block', 'padding-left' : '0.5em'}),
                    ],
                    style = {'display': 'inline-block', 'padding-left' : '1em'}
                    ),
            ],
            style = {'text-align':'center', 'margin' : 'auto', 'padding-top': '1em'}
        ),

        html.Div(
            [
                csv_button, 
                dcc.Download(id="download_csv")
            ],
            style = {'text-align':'center', 'margin' : 'auto', 'padding-top': '1em'}
            ),
    ]
)

@app.callback(
    Output('y_range_putput', 'children'),
    [Input('y_range_slider', 'value')],
    prevent_initial_call=True)
def update_range_output(y_range):
    return f'Concentration range: {y_range}'

@app.callback(
    Output('graph', 'figure'),
    [
        Input('date_picker', 'start_date'), 
        Input('date_picker', 'end_date'),
        Input('y_range_slider', 'value'),
        Input('gas_check_list', 'value'),
        Input('CO2_mean_color', 'value'),
        Input('CO2_std_color', 'value'),
        Input('NO2_mean_color', 'value'),
        Input('NO2_std_color', 'value'),
        Input('CO2_marker', 'value'),
        Input('NO2_marker', 'value'),
    ],
)
def update_graph(start_date, end_date, y_range, gas_list, CO2_mean_color, CO2_std_color, NO2_mean_color, NO2_std_color, CO2_marker, NO2_marker):

    #Change color
    color_dict_temp = color_dict
    color_dict_temp['CO2']['mean'] = CO2_mean_color
    color_dict_temp['CO2']['std'] = CO2_std_color
    color_dict_temp['NO2']['mean'] = NO2_mean_color
    color_dict_temp['NO2']['std'] = NO2_std_color

    #Change marker mode
    marker_mode_dict_temp = marker_mode_dict
    marker_mode_dict_temp['CO2']['mean'] = CO2_marker
    marker_mode_dict_temp['NO2']['mean'] = NO2_marker

    #Get figure
    fig = gases_plot(
        df_group, 
        gases = gas_list, 
        x_range=[start_date, end_date], 
        y_range = y_range, 
        color_dict = color_dict_temp, 
        marker_mode_dict = marker_mode_dict_temp
    )
    return fig

@app.callback(
    Output('download_csv', 'data'),
    [   
        Input('download_csv_button', 'n_clicks'),
    ],
    prevent_initial_call=True,
)
def update_graph(n_clicks):
    return dcc.send_data_frame(df_group.to_csv, "data.csv")

app.run_server(port=8000, host='127.0.0.1')