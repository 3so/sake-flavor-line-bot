import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as io

import get_sakenowa_api

def get_flavor_chart(flavor):
    flavor_chart = [flavor]
    df = pd.DataFrame(flavor_chart)
    df = df.drop( ['brandId', 'brandName', 'flavor'], axis=1)
    df = df.rename(columns={'f1':'華やか', 'f2':'芳醇', 'f3':'重厚', 'f4':'穏やか', 'f5':'ドライ', 'f6':'軽快'}).T

    fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1])
    fig.update_layout(width=600)
    fig.write_image('templates/flavor_chart.png')

flavor = {
    "brandId": 2,
    "f1": 0.5,
    "f2": 0.424835098066976,
    "f3": 0.353698484182939,
    "f4": 0.480473334729331,
    "f5": 0.47061712325654,
    "f6": 0.419411247406479,
    "flavor" : "true",
    "brandName" : "test"
    }

get_flavor_chart(flavor)