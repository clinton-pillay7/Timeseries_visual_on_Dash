import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pymongo import MongoClient
from pandas import *
import datetime
import pytz


# establish connection parameters
client = MongoClient('127.0.0.1', 27017)
db_name = 'alpha'
weeklytable = "weeklycol"



# connect to the database
db = client[db_name]
weekcol = db[weeklytable]

df = pd.DataFrame(list(weekcol.find({
    "$and" : [{
                 "date" : { "$gt" :datetime.datetime(2020, 1, 1, 0, 0, tzinfo=pytz.utc)}
              },
              {
                   "date" : { "$lt" :datetime.datetime(2020, 12, 30, 0, 0, tzinfo=pytz.utc)}
              }]
})))


df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

df.sort_values("date", inplace=True)

df.to_csv('dataset.csv', index = False)

app = dash.Dash(__name__)




app.layout = html.Div(
    children=[
        html.H1(
            children="Closing prices",
        ),
        html.P(
            children="Visual analysis of the closing price weekly",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["date"],
                        "y": df["4_close"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Date vs Closing price"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["date"],
                        "y": df["5_volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Date vs Volume"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)