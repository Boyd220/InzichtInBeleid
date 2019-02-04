from ORI_BZK import ORIDC, have_internet
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input, State

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]

external_js = ["http://code.jquery.com/jquery-3.3.1.min.js",
               "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"]


# load data and filter for recent data
datamodel = ORIDC('total.json', 'xtra_data.json')


def getvaluecounts(df, field):
    """function to count al occurences of values in field of df."""
    df = df[field].value_counts()
    return(df.sort_index())


app = dash.Dash(external_scripts = external_js, external_stylesheets = external_css)

if have_internet() is False:
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
else:
    app.css.config.serve_locally = False
    app.scripts.config.serve_locally = False

app.layout = html.Div(
    children=[
        html.Nav(
            className='navbar navbar-expand-lg navbar-light',
            style={'background-color': 'white'},
            children=[
                html.Img(
                    src='https://helix.nl/wp-content/uploads/2017/02/Rijkslogo-Bouwbesluit-s2.png',
                    width='125',
                    height='75',
                    style={
                        'margin': 'auto'
                    }
                ),
                html.Div(
                    className='navbar navbar-expand-lg navbar-light bg-light',
                    children=[
                        html.A(
                            className='navbar-brand',
                            children='Inzicht in beleid'
                        )
                    ]
                )
            ]),
        html.Div(
            style={
                'width': '100%',
                'background-color': '#00689B',
                "height": "70px"
            },
            children=[
                html.A(
                    children='Inzicht in beleid',
                    style={
                        "color": "white",
                        "float": "right",
                        "margin-right": "1em",
                        "padding-top": "12px",
                        "font-size": "30px"
                    }
                ),
                dcc.Input(
                    placeholder='Typ een zoekterm...',
                    id='input-box',
                    type='text',
                    style={
                        "margin-right": "1em",
                        "margin-top": "1.3em",
                        "margin-left": "1em"
                    }
                ),
                html.Button(
                    'Zoek',
                    id='button',
                    style={
                        "margin-top": "1.3em"
                    }
                )
            ]
        ),
        dcc.Tabs(
            id="tabs",
            value='tab-1',
            children=[
                dcc.Tab(
                    label='Tab one',
                    value='tab-1',
                    children=[
                        html.Div(children=[
                            html.Div(
                                id='textbox',
                                children=
                                    dcc.Markdown(
                                        children='''Select a **single** row to see the details'''
                                    ),
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
                                    columns=[{"name": i, "id": i} for i in ['author', 'date', 'place', 'summary']],
                                    data=[],
                                    # data=df.to_dict("rows"),
                                    row_selectable='single',
                                    n_fixed_rows=1,
                                    selected_rows=[],
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
                                style={
                                    'width': '60%',
                                    'display': 'inline-block',
                                    'vertical-align': 'top'}
                            )
                        ])
                    ]
                ),
                dcc.Tab(
                    label='Tab two',
                    value='tab-2',
                    children=[
                        html.Div(
                            children=[
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
                    ]
                ),
                dcc.Tab(
                    label='Tab three',
                    value='tab-3',
                    children=[
                        html.Div(
                            id='tab3container',
                            children=[
                                html.Div(
                                    id='piecontainer',
                                    style={
                                        'display': 'inline-block'
                                    }
                                ),
                                html.Div(
                                    id='wordcontainer',
                                    style={
                                        'display': 'inline-block'
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output('table', 'data'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def update_dataoutput(n_clicks, searchvalue):
    """ Callback to fill table with searchresults. """
    datamodel.searchword = searchvalue
    datamodel.filter()
    table_data = datamodel.mainresult
    return table_data.to_dict("rows")


@app.callback(
    Output('tabgraph', 'figure'),
    [Input('table', 'data')])
def update_scatter(data):
    """ Callback to fill graph with data from table. """
    df = pd.DataFrame(data)
    if not df.empty:
        dfTK = getvaluecounts(df=df.loc[df['place'] == 'TK'], field='date')
        dfOt = getvaluecounts(df=df.loc[df['place'] != 'TK'], field='date')
        print('create graph')
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
            }]
        }


@app.callback(Output('textbox', 'children'),
              [Input('table', 'selected_rows'),
               Input('table', 'data')])
def show_clicked_doc(selected_row_indices, rows):
    """Callback to retrieve the selected document and output to the textbox."""
    if selected_row_indices is None:
        value = 'Select a single row to see the details'
    elif len(selected_row_indices) == 1:
        row_idx = selected_row_indices[0]
        text = rows[row_idx]['document']
        for word in datamodel.searchword:
            text = text.replace(word, '**'+word+'**')
        text = text.replace('\n', '\n\n')
        value = text
    else:
        value = 'Select a single row to see the details'
    value = '''''' + value + ''''''
    return dcc.Markdown(children=value)


@app.callback(
    Output('table', 'selected_rows'),
    [Input('button', 'n_clicks')])
def unclick(n_clicks):
    """" Callback to unclick items with new searchclick"""
    if n_clicks is not None:
        return []


@app.callback(
    Output('wordcontainer', 'children'),
    [Input('button', 'n_clicks'),
     Input('table', 'data')])
def update_openquestions(n_clicks, tabledata):
    print(datamodel.searchword)
    question = []
    answers = []
    for index, row in datamodel.mcresult.iterrows():
        if row['questype'] == 'open':
            question.append(html.Div(row['summary']))
    return html.Div(question)


@app.callback(
    Output('piecontainer', 'children'),
    [Input('button', 'n_clicks'),
     Input('table', 'data')])
def update_piegraphs(n_clicks, tabledata):
    graphs = []
    graphdata = []
    for index, row in datamodel.mcresult.iterrows():
        if row['questype'] == 'meerkeuze':
            graphdata.append({'title': row['summary'], 'data': row['document']})
    if len(graphdata) > 0:
        for i in range(len(graphdata)):
            values = []
            labels = []
            for key, value in graphdata[i]['data'].items():
                values.append(value)
                labels.append(key)
            graphs.append(dcc.Graph(
                id='piegram-{}'.format(i),
                figure={
                    'data': [{
                        'values': values,
                        'labels': labels,
                        'type': 'pie'
                    }],
                    'layout': {
                        'title': graphdata[i]['title']
                    }
                }
            ))
    else:
        for i in range(3):
            graphs.append(dcc.Graph(
                id='piegram-{}'.format(i),
                figure={
                    'data': [{
                        'values': [10, 20, 70],
                        'labels': ['een', 'twee', 'drie'],
                        'type':'pie'
                    }],
                    'layout': {
                        'title': 'Graph {}'.format(i)
                    }
                }
            ))
    return html.Div(graphs)


if __name__ == '__main__':
    app.run_server(debug=True)
