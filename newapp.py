from ORI_BZK import ORIDC
import divlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input, State

# load data and filter for recent data
datamodel = ORIDC('total.json', 'xtra_data.json')


def getvaluecounts(df, field):
    """function to count al occurences of values in field of df."""
    df = df[field].value_counts()
    return(df.sort_index())


app = dash.Dash(__name__)
app.title = 'Inzicht in beleid'

print(divlib.create_tabs())

app.layout = html.Div(
    children=[
        divlib.create_header(),
        divlib.create_navbar(),
        divlib.create_tabs()
    ],
    style={
        "font-size": "15px"
    }
)




if __name__ == '__main__':
    app.run_server(debug=True)
