import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

## Data Setup

data_full= pd.read_csv('../college_completion/cc_institution_details.csv',
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

data_full['state_100_avg'] = data_full.groupby(['code'])['grad_100_value']\
    .transform('mean')
data_full['state_pell_avg'] = data_full.groupby(['code'])['pell_value']\
    .transform('mean')
data_full['state_ft_fac_avg'] = data_full.groupby(['code'])['ft_fac_value']\
    .transform('mean')
data_full['state_student_count_avg'] = data_full\
.groupby(['code'])['pell_value'].transform('mean')


for col in data_full.columns:
    data_full[col] = data_full[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'],
       [0.4, 'rgb(188,189,220)'], \
       [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'],
       [1.0, 'rgb(84,39,143)']]
data_full['text_grad'] = data_full['state'] + '<br>' + 'Graduation Rate ' \
                         + ['%.1f' % round(float(x), 1)
                              for x in data_full['state_100_avg']] + '%'
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
                      'pell_value',
                      'ft_fac_value',
                      'code',
                      'state_100_avg',
                      'state_pell_avg',
                      'state_ft_fac_avg',
                      'state_student_count_avg',
                      'text_grad',
                      'text_pell',
                      'text_ft_fac',
                      'text_student_count'
                      ]]


app = dash.Dash(__name__)

all_options = {
    'Graduation Rate': ['state_100_avg', 'text_grad',
                        'Graduation Rates by State<br>(Hover for breakdown)'],
    'Pell Grant Value': ['state_pell_avg', 'text_pell',
                         'Average Pell Grant Student Percentage by State'
                         '<br>(Hover for breakdown)'],
    'Full-Time Faculty': ['state_ft_fac_avg', 'text_ft_fac',
                          'Average Full-Time Faculty Members Percentage'
                          ' by State<br>(Hover for breakdown)'],
    'Student Count': ['state_student_count_avg', 'text_student_count',
                      'Average Student Count by State<br>(Hover for breakdown)']
}
app.layout = html.Div([
    dcc.RadioItems(
        id='information',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Graduation Rate'
    ),

    html.Hr(),

    html.Div([dcc.Graph(id='choropleth')],
             style={'width': '49%', 'float': 'left', 'display': 'inline-block'}),

html.Div([dcc.Graph(id='bargraph')],
             style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ])


@app.callback(
    dash.dependencies.Output('choropleth', 'figure'),
    [dash.dependencies.Input('information', 'value')])
def update_figure(filter_choice):
    average = all_options[filter_choice][0]
    text = all_options[filter_choice][1]
    title_text = all_options[filter_choice][2]


    return {
        'data': [go.Choropleth(
            colorscale=scl,
            autocolorscale=False,
            locations=data_viz['code'].unique(),
            z=['%.1f' % round(x, 1) for x in
               data_viz[average].astype(float).unique()],
            locationmode='USA-states',
            text=data_viz[text].unique(),
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Percentage")
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
    [dash.dependencies.Input('information', 'value')])
def update_bargraph(filter_choice):
    average = all_options[filter_choice][0]
    title_text = all_options[filter_choice][2]


    return {
        'data': [go.Bar(
            x= data_viz['state'].unique(),
            y= data_viz[average].astype(float).unique()
    )],
        'layout': go.Layout(
            title=title_text,
            yaxis=dict(
                title='Average graduation rate',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#54278f'
                )
            )
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)