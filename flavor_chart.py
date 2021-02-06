import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as io

import apiget

def get_flavor_chart(flavor):
    flavor_chart = [flavor]
    df = pd.DataFrame(flavor_chart)
    df = df.drop( ['brandId', 'brandName', 'flavor'], axis=1)
    df = df.rename(columns={'f1':'華やか', 'f2':'芳醇', 'f3':'重厚', 'f4':'穏やか', 'f5':'ドライ', 'f6':'軽快'}).T

    fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1])
    fig.update_layout(width=600)
    fig_div = io.to_html(fig, full_html=False)

    return fig_div
