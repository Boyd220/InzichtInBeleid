import dash_core_components as dcc
import dash_html_components as html
import dash_table

tableheader = ['author', 'date', 'place', 'summary']
def create_header():
    return html.Nav(
        className='navbar navbar-expand-lg navbar-light',
        style={'background-color': 'white'},
        children=[
            html.Img(
                src='assets/newlogo.png',
                width='175',
                height='52',
                style={
                    'margin': 'auto'
                }
            )
        ])

def create_navbar():
    barlabel = 'Inzicht in beleid'
    butlabel = 'Zoek'
    startinput = 'Typ een zoekterm...'
    return html.Div(
        style={
            'width': '100%',
            'background-color': '#00689B',
            "height": "70px"
        },
        children=[
            html.A(
                children=barlabel,
                style={
                    "color": "white",
                    "float": "right",
                    "margin-right": "1em",
                    "padding-top": "12px",
                    "font-size": "30px"
                }
            ),
            dcc.Input(
                placeholder=startinput,
                id='input-box',
                type='text',
                style={
                    "margin-right": "1em",
                    "margin-top": "1.3em",
                    "margin-left": "1em"
                }
            ),
            html.Button(
                butlabel,
                id='button',
                style={
                    "color": "white",
                    "margin-top": "1.3em"
                }
            )
        ]
    )

def create_tabs():
    return dcc.Tabs(
        id="tabs",
        value='tab-1',
        children=[
        create_tab('Tekst','tab-1',create_tabletab()),
        create_tab('Grafiek','tab-2',create_graphtab()),
        create_tab('Vraagselectie','tab-3',''),
        create_tab('Antwoordselectie','tab-4',''),
        create_tab('Details','tab-5','')
        ]
    )

def create_tab(label,value,children):
    return dcc.Tab(label=label,value=value,children=[children])

def tab5():
    dcc.Tab(
        id='tab5',
        label='Details',
        value='tab-5',
        children=[
                html.Div('Nothing to show yet..')
        ]
        # style={'display': 'none'}
    )

def tab4():
    dcc.Tab(
        id='tab4',
        label='Antwoordselectie',
        value='tab-4',
        children=[
            html.Div(
                className='row',
                children=[
                    html.Div(
                        className='six columns',
                        children=[
                            html.Div(
                                id='newcontainer',
                                style={
                                    'display': 'inline-block'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        children=[
                            html.Div(
                                id='newcontainer2',
                                style={
                                    'display': 'inline-block'
                                },
                                children='testing'
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className='row',
                children=[
                    html.Div(
                        className='six columns',
                        children=[
                            html.Div(
                                id='newcontainer3',
                                style={
                                    'display': 'inline-block'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        className='six columns',
                        children=[
                            html.Div(
                                id='newcontainer4',
                                style={
                                    'display': 'inline-block'
                                },
                                children='testing'
                            )
                        ]
                    )
                ]
            )
        ]
    )

def tab3():
    dcc.Tab(
        label='Vraagselectie',
        value='tab-3',
        children=html.Div(
            html.Div([
                html.Div([
                    html.Div(
                        id='piecontainer',
                        style={
                            'display': 'inline-block'
                        }
                    )],
                    className='six columns'
                ),
                html.Div([
                    html.Div(
                        id='wordcontainer',
                        style={
                            'display': 'inline-block'
                        }
                    )],
                    className='six columns'
                )],
                className='row'
            )
        )
    )

def create_graphtab():
    return html.Div(
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

def create_tabletab():
    return html.Div(children=[create_textbox(),create_datatable()])

def create_textbox(text=''):
    return html.Div(id='textbox',
        children=dcc.Markdown(children=text),
        style={
            'textAlign': 'left',
            'backgroundColor': 'white',
            'width': '40%',
            'display': 'inline-block'
        }
    )

def create_datatable():
    divinput = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in tableheader],
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
    )
    return html.Div(divinput,
        style={
            'width': '60%',
            'display': 'inline-block',
            'vertical-align': 'top'
        })
