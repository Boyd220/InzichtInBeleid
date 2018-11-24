import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from ORI_BZK import get_selection

df = pd.read_json('C:/Users/Kraan/Git/ORI/total.json', orient='records')

app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Test-app',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(id='textfield',children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Input(placeholder='Enter a value...',id='input-box', type='text'),
    html.Button('Zoek', id='button'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in ['author','date','place','summary']],
        data=df.to_dict("rows"),
    )
])

@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks,value):
    if value!=None:
        table_data=get_selection(value)
        return table_data.to_dict("rows")

if __name__ == '__main__':
    app.run_server(debug=True)
