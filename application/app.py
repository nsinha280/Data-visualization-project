import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
#import plotly.plotly as py
import plotly.graph_objs as go
#from plotly.offline import init_notebook_mode, iplot

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

## Data Setup

data_full= pd.read_csv('cc_institution_details.csv',
                  encoding = 'latin1')

state = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

data_full['state'] = ['Virginia' if x == 'District of Columbia'
                 else x for x in data_full['state']]
data_full['code'] = [state[x] for x in data_full['state']]

data_full['state_100_avg'] = data_full.groupby(['code','level'])['grad_100_value']\
    .transform('mean')
data_full['state_150_avg'] = data_full.groupby(['code','level'])['grad_150_value']\
    .transform('mean')
data_full['state_pell_avg'] = data_full.groupby(['code','level'])['pell_value']\
    .transform('mean')
data_full['state_ft_fac_avg'] = data_full.groupby(['code','level'])['ft_fac_value']\
    .transform('mean')
data_full['state_student_count_avg'] = data_full\
.groupby(['code','level'])['student_count'].transform('mean')


for col in data_full.columns:
    data_full[col] = data_full[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'],
       [0.4, 'rgb(188,189,220)'], \
       [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'],
       [1.0, 'rgb(84,39,143)']]

data_full['text_grad'] = data_full['state'] + '<br>' + 'Graduation Rate ' \
                         + ['%.1f' % round(float(x), 1)
                              for x in data_full['state_100_avg']] + '%'
data_full['text_grad_late'] = data_full['state'] + '<br>' + \
                              'Late Graduation Rate ' \
                         + ['%.1f' % round(float(x), 1)
                              for x in data_full['state_150_avg']] + '%'
data_full['text_pell'] = data_full['state'] + '<br>' \
                         + 'Average Pell Grant Value ' \
                         + ['%.1f' % round(float(x), 1)
                               for x in data_full['state_pell_avg']] + '%'
data_full['text_ft_fac'] = data_full['state'] + '<br>' \
                           + 'Average Full-time Faculty Value ' \
                         + ['%.1f' % round(float(x), 1)
                            for x in data_full['state_ft_fac_avg']] + '%'
data_full['text_student_count'] = data_full['state'] + '<br>' \
                                  + 'Average Student Count ' \
                         + ['%.1f' % round(float(x), 1)
                                   for x in
                                        data_full['state_student_count_avg']]

data_viz = data_full[['unitid',
                      'chronname',
                      'city',
                      'state',
                      'level',
                      'control',
                      'basic',
                      'hbcu',
                      'flagship',
                      'long_x',
                      'lat_y',
                      'site',
                      'student_count',
                      'grad_100_value',
                      'grad_150_value',
                      'pell_value',
                      'ft_fac_value',
                      'code',
                      'state_100_avg',
                      'state_150_avg',
                      'state_pell_avg',
                      'state_ft_fac_avg',
                      'state_student_count_avg',
                      'text_grad',
                      'text_grad_late',
                      'text_pell',
                      'text_ft_fac',
                      'text_student_count'
                      ]]


app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

all_options = {
    'Graduation Rate': ['state_100_avg', 'text_grad',
                        'Graduation Rates by State<br>(Hover for breakdown)',
                        'Average Graduation Rate', 'Percentage',
                        'grad_100_value',
                        'Graduation Rates for Colleges at ',
                        'Graduation Rate'],
    'Late Graduation Rate': ['state_150_avg', 'text_grad_late',
                        'Late Graduation Rates by State<br>(Hover for breakdown)',
                        'Average Late Graduation Rate', 'Percentage',
                        'grad_150_value',
                        'Late Graduation Rates for Colleges at ',
                        'Late Graduation Rate'],
    'Pell Grant Value': ['state_pell_avg', 'text_pell',
                         'Average Pell Grant Student Percentage by State'
                         '<br>(Hover for breakdown)',
                         'Average Pell Grant Rate','Percentage',
                         'pell_value',
                         'Pell Grant Rate for Colleges at ',
                         'Pell Grant Rate'],
    'Full-Time Faculty': ['state_ft_fac_avg', 'text_ft_fac',
                          'Average Full-Time Faculty Members Percentage'
                          ' by State<br>(Hover for breakdown)',
                          'Average Full-Time Faculty Percentage','Percentage',
                          'ft_fac_value',
                          'Full-Time Faculty Percentage for Colleges at ',
                          'Full-Time Faculty Percentage'],
    'Student Count': ['state_student_count_avg', 'text_student_count',
                      'Average Student Count by State<br>(Hover for breakdown)',
                      'Average Student Count', 'Count', 'student_count',
                      'Student Counts for Colleges at ',
                      'Student Count']
}

level_options = {
    '2 Year Schools' : '2-year',
    '4 Year Schools' : '4-year'
}
app.layout = html.Div([
    dcc.RadioItems(
        id='information',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Graduation Rate'
    ),

    html.Hr(),

    dcc.RadioItems(
        id='level-information',
        options=[{'label': k, 'value': k} for k in level_options.keys()],
        value='4 Year Schools'
    ),

    html.Hr(),

    html.Div([dcc.Graph(id='choropleth',
                        clickData={'points': [{'location': 'CA'}]})],
             style={'height': '80%'}),

    html.Div([dcc.Graph(id='hovergraph')],
             style={'width': '49%', 'float': 'left',
                    'display': 'inline-block'}),

    html.Div([dcc.Graph(id='bargraph')],
             style={'width': '49%', 'float': 'right',
                    'display': 'inline-block'}),

    ])


@app.callback(
    dash.dependencies.Output('choropleth', 'figure'),
    [dash.dependencies.Input('information', 'value'),
     dash.dependencies.Input('level-information', 'value')])
def update_figure(filter_choice, level_choice):
    average = all_options[filter_choice][0]
    text = all_options[filter_choice][1]
    title_text = all_options[filter_choice][2]
    dff = data_viz[data_viz['level']==level_options[level_choice]]
    bar_title = all_options[filter_choice][4]


    return {
        'data': [go.Choropleth(
            colorscale=scl,
            autocolorscale=False,
            locations=dff['code'].unique(),
            z=['%.1f' % round(x, 1) for x in
               dff[average].astype(float).unique()],
            locationmode='USA-states',
            text=dff[text].unique(),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title=bar_title)
        )],
        'layout': go.Layout(
            title=title_text,
            geo=dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
        )
    }


@app.callback(
    dash.dependencies.Output('bargraph', 'figure'),
    [dash.dependencies.Input('information', 'value'),
     dash.dependencies.Input('level-information', 'value')])
def update_bargraph(filter_choice, level_choice):
    average = all_options[filter_choice][0]
    title_text = all_options[filter_choice][2]
    y_axis_title = all_options[filter_choice][3]
    dff = data_viz[data_viz['level'] == level_options[level_choice]]
    dff = dff.sort_values(by=['state'], ascending=False)


    return {
        'data': [go.Bar(
            x= dff[average].astype(float).unique(),
            y= dff['state'].unique(),
            marker=dict(
                color='rgb(84,39,143)'
            ),
            orientation = 'h'
    )],
        'layout': go.Layout(
            title=title_text,
            xaxis=dict(
                title=y_axis_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            margin=go.Margin(
                l=120
            )
        )
    }

def create_hovergraph(dff, graph_type, title, axis_title):


    return {
        'data': [go.Bar(
            x=dff[graph_type].astype(float).unique(),
            y=dff['chronname'].unique(),
            marker=dict(
                color='rgb(84,39,143)'
            ),
            orientation='h'
        )],
        'layout': go.Layout(
            title=title,
            xaxis=dict(
                title=axis_title,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
            ),
            margin=go.Margin(
                l=400
            )
        )
    }

@app.callback(
    dash.dependencies.Output('hovergraph', 'figure'),
    [dash.dependencies.Input('choropleth', 'clickData'),
     dash.dependencies.Input('information', 'value'),
     dash.dependencies.Input('level-information', 'value')])
def update_hovergraph(clickData, filter_choice, level_choice):
    location = clickData['points'][0]['location']
    graph_type = all_options[filter_choice][5]
    dff = data_viz[data_viz['code'] == location]
    dff = dff[dff['level'] == level_options[level_choice]]
    dff = dff.sort_values(by=['chronname'], ascending=False)
    title = all_options[filter_choice][6] + location + \
            '<br>(Click on a State to Change)'
    axis_title = all_options[filter_choice][7]
    return create_hovergraph(dff, graph_type, title, axis_title)

if __name__ == '__main__':
    app.run_server(debug=True)