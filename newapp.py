from ORI_BZK_new import ORIDC
import divlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input, State

# load data and filter for recent data
datamodel = ORIDC('total.json', 'xtra_data.json')
rowrange = 10


def getvaluecounts(df, field):
    """function to count al occurences of values in field of df."""
    df = df[field].value_counts()
    return(df.sort_index())


app = dash.Dash(__name__)
app.title = 'Inzicht in beleid'

# print(divlib.create_tab3())

app.layout = html.Div(
    children=[
        divlib.create_header(),
        divlib.create_navbar(),
        divlib.create_tabs(rowrange)
    ],
    style={
        "font-size": "15px"
    }
)


def callback_closedquestion(i):
    def update_piegram(n_clicks, data):
        if len(datamodel.closedquestion) > i:
            values = []
            labels = []
            for key, value in datamodel.closedquestion[i]['data'].items():
                values.append(value)
                labels.append(key)
            figure = {
                'data': [{
                    'values': values,
                    'labels': labels,
                    'type': 'pie'
                }],
                'layout': {
                    'title': ''
                }
            }
            return divlib.create_piecol(
                    tabnum=3,
                    rownum=i,
                    colnum=1,
                    buttext=datamodel.closedquestion[i]['title'],
                    figdata=figure
                )
        else:
            return divlib.create_piecol(
                    tabnum=3,
                    rownum=i,
                    colnum=1,
                    display='None'
                )
    return update_piegram


def callback_openquestion(i):
    def update_wordcloud(n_clicks, data):
        if len(datamodel.openquestion) > i:
            image = datamodel.create_wcimage(datamodel.openquestion[i]['data'])
            return divlib.create_cloudcol(
                    tabnum=3,
                    rownum=i,
                    colnum=2,
                    buttext=datamodel.openquestion[i]['title'],
                    imgdata=image
                )
        else:
            return divlib.create_cloudcol(
                tabnum=3,
                rownum=i,
                colnum=2,
                display='None'
            )
    return update_wordcloud


def callback_openanswerquestion(i):
    def update_question(n_clicks, data):
        if len(datamodel.openanswer) > i:
            return divlib.create_butcol(
                tabnum=4,
                rownum=i,
                colnum=1,
                buttext=datamodel.openanswer[i]['title']
            )
        else:
            return divlib.create_butcol(
                tabnum=4,
                rownum=i,
                colnum=1,
                display='None')
    return update_question


def callback_openanswercount(i):
    def update_count(n_clicks, data):
        if len(datamodel.openanswer) > i:
            return divlib.create_labcol(
                tabnum=4,
                rownum=i,
                colnum=2,
                labtext=str(int(datamodel.openanswer[i]['count']))+' hits'
            )
        else:
            return divlib.create_labcol(
                tabnum=4,
                rownum=i,
                colnum=2,
                display='None')
    return update_count


def callback_openanswercloud(i):
    def update_cloud(n_clicks, data):
        if len(datamodel.openanswer) > i:
            image = datamodel.create_wcimage(datamodel.openanswer[i]['data'])
            return divlib.create_cloudcol(
                tabnum=4,
                rownum=i,
                colnum=3,
                imgdata=image,
                buttext=False
            )
        else:
            return divlib.create_cloudcol(
                tabnum=4,
                rownum=i,
                colnum=3,
                display='None',
                buttext=False)
    return update_cloud


def callback_getdetails():
    def get_detailtable(*args):
        answer = False
        if max(args) > 0:
            maxpos = args.index(max(args))
            if maxpos >= len(args)/2:
                maxpos = int(maxpos - len(args)/2)
                answer = True
            if answer is False:
                df = pd.DataFrame({'Answers': datamodel.openquestion[maxpos]['source']})
                return df.to_dict("rows")
            df = pd.DataFrame({'Answers': datamodel.openanswer[maxpos]['source']})
            return df.to_dict("rows")
    return get_detailtable


def callback_getdetailtitle():
    def get_detailtitle(*args):
        answer = False
        if max(args) > 0:
            maxpos = args.index(max(args))
            if maxpos >= len(args)/2:
                maxpos = int(maxpos - len(args)/2)
                answer = True
            if answer is False:
                return str(datamodel.openquestion[maxpos]['title'])
            return str(datamodel.openanswer[maxpos]['title'])
    return get_detailtitle


def callback_switchtab():
    def switchtab(*args):
        if max(args) > 0:
            print('switch')
            return 'tab-5'
    return switchtab


for i in range(0, rowrange):
    app.callback(
        Output('piecontainer3'+str(i), 'children'),
        [Input('button', 'n_clicks'),
         Input('table', 'data')]
    )(callback_closedquestion(i))
    app.callback(
        Output('wordcontainer3'+str(i), 'children'),
        [Input('button', 'n_clicks'),
         Input('table', 'data')]
    )(callback_openquestion(i))
    app.callback(
        Output('question-4'+str(i), 'children'),
        [Input('button', 'n_clicks'),
         Input('table', 'data')]
    )(callback_openanswerquestion(i))
    app.callback(
        Output('count-4'+str(i), 'children'),
        [Input('button', 'n_clicks'),
         Input('table', 'data')]
    )(callback_openanswercount(i))
    app.callback(
        Output('wordcloud-4'+str(i), 'children'),
        [Input('button', 'n_clicks'),
         Input('table', 'data')]
    )(callback_openanswercloud(i))

input = []
input2 = []
for i in range(0, rowrange):
    input.append(Input('button-3'+str(i)+'2', 'n_clicks_timestamp'))
    input2.append(Input('button-4'+str(i)+'1', 'n_clicks_timestamp'))
input.extend(input2)

app.callback(
    Output('detailtile', 'children'),
    input
)(callback_getdetailtitle())

app.callback(
    Output('detailtable', 'data'),
    input
)(callback_getdetails())

app.callback(
    Output('tabs', 'value'),
    input
)(callback_switchtab())

if True is False:
    for j in range(3, 5):
        for i in range(0, rowrange):
            app.callback(
                Output('detailtable', 'data'),
                [Input('button-'+str(j)+str(i)+'2', 'n_clicks'),
                 Input('table', 'data')]
            )(callback_getdetails(i))

            app.callback(
                Output('detailtile', 'children'),
                [Input('button-'+str(j)+str(i)+'2', 'n_clicks'),
                 Input('table', 'data')]
            )(callback_getdetailtitle(i))
        app.callback(
            Output('button-3'+str(i)+'2', 'n_clicks'),
            [Input('detailtile', 'children')]
        )(())
        app.callback(
            Output('button-4'+str(i)+'1', 'n_clicks'),
            [Input('detailtile', 'children')]
        )(())


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


@app.callback(
    Output('textbox', 'children'),
    [Input('table', 'selected_rows'),
     Input('table', 'data')])
def show_clicked_doc(selected_row_indices, rows):
    """Callback to retrieve the selected document and output to the textbox."""
    if selected_row_indices is None:
        value = 'Klik een document aan om hem door te lezen'
    elif len(selected_row_indices) == 1:
        row_idx = selected_row_indices[0]
        text = rows[row_idx]['document']
        for word in datamodel.searchword:
            text = text.replace(word, '**'+word+'**')
        text = text.replace('\n', '\n\n')
        value = text
    else:
        value = 'Klik een document aan om hem door te lezen'
    value = '''''' + value + ''''''
    return dcc.Markdown(children=value)


@app.callback(
    Output('table', 'selected_rows'),
    [Input('button', 'n_clicks')])
def unclick(n_clicks):
    """" Callback to unclick items with new searchclick"""
    if n_clicks is not None:
        return []


if __name__ == '__main__':
    app.run_server(debug=True)
