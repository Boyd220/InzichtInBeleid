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


def create_tabs(rowrange=10):
    return dcc.Tabs(
        id="tabs",
        value='tab-1',
        children=[
            create_tab('Tekst', 'tab-1', create_tabletab()),
            create_tab('Grafiek', 'tab-2', create_graphtab()),
            # tab3(),
            create_tab('Vraagselectie', 'tab-3', create_questionstab(rows=rowrange)),
            create_tab('Antwoordselectie', 'tab-4', create_answersstab(rows=rowrange)),
            create_tab('Details', 'tab-5',
                       html.Div([
                            html.Div(
                                id='detailtile',
                                children=[],
                                style={
                                    'font-weight': 'bold'
                                }
                            ),
                            create_datatable(
                                tableid='detailtable',
                                columnnames=['Answers'],
                                datastyle={
                                    'whiteSpace': 'normal'
                                },
                                style={
                                    'minWidth': '30px', 'maxWidth': '500px'
                                },
                                tablecss=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }]),
                            html.Div()]
                        )
            )
        ]
    )


def create_tab(label, value, children):
    if type(children) == list:
        return dcc.Tab(label=label, value=value, children=children)
    else:
        return dcc.Tab(label=label, value=value, children=[children])


def create_answersstab(rows):
    divrows = []
    tabnumber = 4
    for rownumber in range(0, rows):
        divrows.append(
            html.Div(
                [
                    create_col(
                        colid='question-'+str(tabnumber)+str(rownumber),
                        children=create_butcol(
                            tabnum=tabnumber,
                            rownum=rownumber,
                            colnum=1,
                            display='None'),
                        width='four columns'
                    ),
                    create_col(
                        colid='count-'+str(tabnumber)+str(rownumber),
                        children=create_labcol(
                            tabnum=tabnumber,
                            rownum=rownumber,
                            colnum=1,
                            display='None'),
                        width='two columns'
                    ),
                    create_col(
                        colid='wordcloud-'+str(tabnumber)+str(rownumber),
                        children=create_cloudcol(
                            tabnum=tabnumber,
                            rownum=rownumber,
                            colnum=3,
                            display='None',
                            buttext=False)
                    )
                ],
                className='row'
            )
        )
    divrows.append(html.Button(
        'Zie volgende resultaten',
        id='next' + str(tabnumber),
        style={'display': 'None'}
    ))
    divrows.append(html.Div(
        id='div-' + str(tabnumber)
    ))
    return divrows


def create_col(colid, children, width='six columns'):
    return html.Div(
        className=width,
        children=[
            html.Div(
                id=colid,
                style={
                    'display': 'inline-block'
                },
                children=children
            )
        ]
    )


def create_labcol(tabnum, rownum, colnum, display='inline-block', labtext='count'):
    return html.Div(
                        labtext,
                        id='label-'+str(tabnum)+str(rownum)+str(colnum),
                        style={
                            'margin-top': '1.3em',
                            'display': display
                        }
                    )


def create_butcol(tabnum, rownum, colnum, display='inline-block', buttext='question'):
    return html.Button(
                        buttext,
                        id='button-'+str(tabnum)+str(rownum)+str(colnum),
                        style={
                            'height': '50',
                            'margin-top': '1.3em',
                            'white-space': 'normal',
                            'display': display
                        },
                        n_clicks_timestamp=0
                    )


def create_piecol(tabnum, rownum, colnum, display='inline-block', figdata=[], buttext='Button'):
    return [html.Button(
                        buttext,
                        id='button-'+str(tabnum)+str(rownum)+str(colnum),
                        style={
                            'height': '50',
                            'margin-top': '1.3em',
                            'white-space': 'normal',
                            'display': display
                        }
                    ),
            dcc.Graph(
                        id='piegram-'+str(tabnum)+str(rownum)+str(colnum),
                        figure={
                            'data': figdata
                        },
                        style={
                            'display': display
                        }
                    )
            ]


def create_cloudcol(tabnum, rownum, colnum, display='inline-block', imgdata='', buttext='Button'):
    resultdiv = []
    if buttext is not False:
        resultdiv.append(
            html.Button(
                buttext,
                id='button-'+str(tabnum)+str(rownum)+str(colnum),
                style={
                    'height': '50',
                    'margin-top': '1.3em',
                    'white-space': 'normal',
                    'display': display
                },
                n_clicks_timestamp=0
            )
        )
    resultdiv.append(
        html.Img(
                    id='Img-'+str(tabnum)+str(rownum)+str(colnum),
                    src=imgdata,
                    style={
                        'vertical-align': 'top',
                        'display': display
                    }
                )
    )
    return resultdiv


def create_questionstab(rows):
    divrows = []
    tabnumber = 3
    for rownumber in range(0, rows):
        divrows.append(
            html.Div(
                [
                    create_col(
                        colid='piecontainer'+str(tabnumber)+str(rownumber),
                        children=create_piecol(
                            tabnum=tabnumber,
                            rownum=rownumber,
                            colnum=1,
                            display='None'
                        )
                    ),
                    create_col(
                        colid='wordcontainer'+str(tabnumber)+str(rownumber),
                        children=create_cloudcol(
                            tabnum=tabnumber,
                            rownum=rownumber,
                            colnum=2,
                            display='None'
                        )
                    )
                ],
                className='row',
                style={
                    'font-weight': 'bold',
                    'font-size': '15px'
                }
            )
        )
    divrows.append(html.Button(
        'Zie volgende resultaten',
        id='next' + str(tabnumber),
        style={'display': 'None'}
    ))
    divrows.append(html.Div(
        id='div-' + str(tabnumber)
    ))
    return divrows


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
    return html.Div(
        children=[
            create_textbox(),
            html.Div(
                create_datatable(
                    tableid='table',
                    columnnames=tableheader,
                    row_selectable='single',
                    style_table={
                        'maxHeight': '300',
                        'overflowY': 'scroll'
                    },
                    tablecss=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                    condstyle=[
                        {'if': {'column_id': 'author'},
                         'width': '100px'},
                        {'if': {'column_id': 'summary'},
                         'width': '400px'},
                    ],
                    style={
                        'minWidth': '30px', 'maxWidth': '500px',
                        'whiteSpace': 'no-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
                style={
                    'width': '60%',
                    'display': 'inline-block',
                    'vertical-align': 'top'
                })
        ]
    )


def create_textbox(text=''):
    return html.Div(
        id='textbox',
        children=dcc.Markdown(
            children=text
        ),
        style={
            'textAlign': 'left',
            'backgroundColor': 'white',
            'width': '40%',
            'display': 'inline-block'
        }
    )


def create_datatable(tableid, columnnames, row_selectable=None, style_table={}, datastyle={}, tablecss=[], condstyle=[], style={}):
    divinput = dash_table.DataTable(
        id=tableid,
        columns=[{"name": i, "id": i} for i in columnnames],
        data=[],
        row_selectable=row_selectable,
        n_fixed_rows=1,
        selected_rows=[],
        style_table=style_table,
        style_cell=style,
        style_data=datastyle,
        css=tablecss,
        style_cell_conditional=condstyle
    )
    return divinput
