import pandas as pd
import plotly.express as px
df=pd.read_csv("results.csv")
fig=px.histogram(x=df['Gender'],color=df['Sentiment'])
fig.show()