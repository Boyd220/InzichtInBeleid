import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from ORI_BZK import get_selection, get_searchmatrix
from dash.dependencies import Output, Input, State

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

external_js = ["http://code.jquery.com/jquery-3.3.1.min.js",
               "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"]

#load data and filter for recent data
df = pd.read_json('total.json', orient='records')
df = df.loc[df['date']>='2016-01-01']

def getvaluecounts(df, field):
    """function to count al occurences of values in field of df."""
    df = df[field].value_counts()
    return(df.sort_index())


app = dash.Dash(external_scripts = external_js,
external_stylesheets = external_css)
markdown_text = '''
Select a **single** row to see the details
'''
app.layout = html.Div(
    children=[
        html.Nav(
        className='navbar navbar-expand-lg navbar-light bg-light', 
        children =[html.A(className='navbar-brand', children='Inzicht in beleid')
        ]),

        dcc.Input(placeholder='Enter a value...', id='input-box', type='text'),
        html.Button('Zoek', id='button'),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Tab one', value='tab-1', children=[
                html.Div(children=[
                    html.Div(id='textbox', children=dcc.Markdown(children=markdown_text),
                        style={
                            'textAlign': 'left',
                            'backgroundColor': 'white',
                            'width': '40%',
                            'display': 'inline-block'
                        }
                    ),
                    html.Div(
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in ['author','date','place','summary']],
                            # data=df.to_dict("rows"),
                            row_selectable=True,
                            n_fixed_rows=1,
                            style_table={
                                'maxHeight': '300',
                                'overflowY': 'scroll'
                            },
                            style_cell={
                                'minWidth': '30px', 'maxWidth': '500px',
                                'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                            },
                            css=[{
                                'selector': '.dash-cell div.dash-cell-value',
                                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                            }],
                            style_cell_conditional=[
                                {'if': {'column_id': 'author'},
                                 'width': '100px'},
                                {'if': {'column_id': 'summary'},
                                 'width': '400px'},
                            ]
                        ),
                    style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'} )
                ])
            ]),
            dcc.Tab(label='Tab two', value='tab-2', children=[
                html.Div(children=[
                    dcc.Graph(
                        id='tabgraph',
                        figure={
                            'data': [{
                                    'x': [1, 2, 3, 4],
                                    'y': [4, 1, 3, 5],
                                    'name': 'TK',
                                    'mode': 'markers',
                                }, {
                                    'x': [1, 2, 3, 4],
                                    'y': [9, 4, 1, 4],
                                    'name': 'Gemeente',
                                    'mode': 'markers',
                                }
                            ]
                        }
                    )
                ],
                )
            ])
        ])
])


@app.callback(
    Output('table', 'data'),
    [Input('button', 'n_clicks'),
     Input('tabs', 'value')],
    [State('input-box', 'value')])
def update_output(n_clicks, abvalue, searchvalue):
    """ Callback to fill table with searchresults. """
    if searchvalue is not None:
        table_data = get_selection(df, searchvalue)
        return table_data.to_dict("rows")


@app.callback(
    Output('tabgraph', 'figure'),
    [Input('table', 'data')])
def update_graph(data):
    """ Callback to fill graph with data from table. """
    df = pd.DataFrame(data)
    dfTK = getvaluecounts(df=df.loc[df['place'] == 'TK'], field='date')
    dfOt = getvaluecounts(df=df.loc[df['place'] != 'TK'], field='date')
    print('test')
    print(dfTK.index.tolist())
    return{'data': [{
            'x': dfTK.index.tolist(),
            'y': dfTK.tolist(),
            'name': 'TK',
            'mode': 'markers',
        }, {
                'x': dfOt.index.tolist(),
                'y': dfOt.tolist(),
                'name': 'Gemeente',
                'mode': 'markers',
        }]}


@app.callback(Output('textbox', 'children'),
              [Input('table', 'selected_rows'),
               Input('table', 'data')],
               [State('input-box', 'value')])
def query_button_clicked(selected_row_indices, rows, value):
    """ Callback to retrieve the selected document and output to the textbox. """
    if selected_row_indices is None:
        value = 'Select a single row to see the details'
    elif len(selected_row_indices) == 1:
        row_idx = selected_row_indices[0]
        text = rows[row_idx]['document']
        for word in get_searchmatrix(value):
            text = text.replace(word, '**'+word+'**')
        text = text.replace('\n', '\n\n')
        value = text
    else:
        value = 'Select a **single** row to see the details'
    value = '''''' + value + ''''''
    return dcc.Markdown(children=value)

if __name__ == '__main__':
    app.run_server(debug=True)
