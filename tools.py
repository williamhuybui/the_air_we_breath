import plotly.graph_objects as go
import datetime
import numpy as np
import pandas as pd

color_dict = {'CO2' : {'mean':'#636EFA',
                       'median' : '#EF553B',
                       'std': '#FECB52',
                       'max': '#AB63FA',
                       'min': '#00CC96'},
            'NO2' : {'mean':'#1F77B4',
                       'median' : '#FF7F0E',
                       'std': '#19D3F3',
                       'max': '#D62728',
                       'min': '#8C564B'}
             }
marker_mode_dict = {'CO2': {'mean':'lines+markers'},
                    'NO2': {'mean':'lines+markers'}}

def data_generator(n_hours):
    """
    n_hours
    """
    np.random.seed(10)
    
    #Create datetime column. Unit = hours, counting backward from today
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(hours = x) for x in range(n_hours)]

    #Create no2 column. Normal distribution with specified mean and std
    no2 = np.abs(np.random.normal(loc = 50, scale = 15, size = n_hours))

    #Create co2 column. Normal distribution with specified mean and std
    co2 = np.abs(np.random.normal(loc = 80, scale = 20, size = n_hours))

    #Create dataframe with new engineer features
    df = pd.DataFrame({})
    df['datetime'] = date_list
    df['date'] = [i.date() for i in df['datetime']]
    df['NO2'] = no2
    df['CO2'] = co2

    #Groupby and data engineer
    df_group = df.groupby('date').agg(['mean', 'median', 'max', 'min', 'std'])
    return df_group

def gas_plot(df_group, gas, x_range=[], y_range = [], color_dict = color_dict, marker_mode_dict = marker_mode_dict):
    """
    gas: either 'NO2' or 'CO2'
    y_range: (tupple), the lower and upper limit of y axis
    """
    #Initialization
    fig = go.Figure()
    stats = [ 'median', 'max', 'min', 'std', 'mean']

    #Slice date
    # start_date = datetime.datetime.strptime(x_range[0], '%Y-%m-%d').date()
    # end_date = datetime.datetime.strptime(x_range[1], '%Y-%m-%d').date()
    # df=df_group[start_date : end_date].copy()
    df=df_group.copy()

    for stat in stats:
        if stat == 'mean':
            fig.add_trace(go.Scatter(x=df.index, y=df[gas][stat], 
                                    name = f'{gas} {stat}',
                                    mode=marker_mode_dict[gas][stat],
                                    marker_color = color_dict[gas][stat]
                                    )
                         )
        # elif stat == 'median':
        #     fig.add_trace(go.Scatter(x=df.index, 
        #                             y=df[gas][stat], 
        #                             name = f'{gas} {stat}',
        #                             marker_color = color_dict[gas][stat]
        #                             )
        #                  )
        # elif stat == 'max':
        #     fig.add_trace(go.Scatter(x=df.index, 
        #                             y=df[gas][stat], 
        #                             name = f'{gas} {stat}',
        #                             marker_color = color_dict[gas][stat]
        #                             )
        #                  )
        # elif stat == 'min':
        #     fig.add_trace(go.Scatter(x=df.index, 
        #                             y=df[gas][stat], 
        #                             name = f'{gas} {stat}',
        #                             marker_color = color_dict[gas][stat]
        #                             )
        #                  )
        elif stat == 'std':
            if gas == 'CO2':
                color = 'gray'
            else:
                color = '#f8e6bd'
            
            upper = list(df[gas]['mean'] + df[gas][stat]) #Upper bound
            lower = list(df[gas]['mean'] - df[gas][stat]) #Lower bound
            
            fig.add_trace(go.Scatter(x=list(df.index), 
                                y=lower,
                                opacity = 0.4,
                                showlegend=False,
                                mode='lines',
                                marker_color = color_dict[gas][stat]
                        )
             )
            
            fig.add_trace(go.Scatter(x=list(df.index), 
                                            y=upper,
                                            fill='tonexty',
                                            opacity = 0.4,
                                     showlegend=False,
                                     mode='lines',
                                     marker_color = color_dict[gas][stat]
                                    )
                         )

    #Background update
    fig.update_layout(plot_bgcolor= 'white',
                      title = ''
                     )
    fig.update_xaxes(showgrid=True,
                     title = 'Date',
                     gridcolor='gray', 
                     zerolinecolor='black'
                    )
    fig.update_yaxes(showgrid=True,  
                     title = f'Concentration (μ mol/m2)',
                     gridcolor='gray', 
                     zerolinecolor='black',
                    )
    
    # The ability to modify the plot axis minimum and maximum values 
    # (for both the X [time] axis and Y [CO2 or NO2] axis).
    if len(x_range) != 0:
        x_range = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in x_range]
        fig.update_xaxes(range = x_range, 
                         rangeslider = dict(visible=True, range = x_range))
    if len(y_range) != 0:
         fig.update_yaxes(range = y_range)
            
    return fig


def gases_plot(df_group, gases, x_range=[], y_range = [], color_dict = color_dict, marker_mode_dict=marker_mode_dict):
    fig = go.Figure()
    for gas in gases:
        fig_temp = gas_plot(df_group, gas, x_range = x_range, y_range = y_range, color_dict = color_dict)
        for trace in fig_temp.data:
            fig.add_trace(trace)
        fig.layout = fig_temp.layout
    return fig