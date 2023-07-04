import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
st.title("Sentiment Analysis System")
choice=st.sidebar.selectbox("My Menu",("Home","Analysis","Results"))
if(choice=="Home"):
    st.image("https://i.pinimg.com/originals/52/ad/6a/52ad6a11c1dcb1692ff9e321bd520167.gif")
    st.write("It is a natural language Processing Application which can analyze sentiment on a text data")
    st.write("This application predicts the sentiment into three categories- Positive, Negative, Neutral")
    st.write("This application can get data from google forms through a google sheet.")
elif(choice=="Analysis"):
    sid=st.text_input("Enter your google sheet ID")
    r=st.text_input("Enter Range between first and last columns")
    c=st.text_input("Enter column name to be analysed")
    btn=st.button("Analyse")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file("key.json",["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        service=build("Sheets","v4",credentials=st.session_state['cred']).spreadsheets().values()
        k=service.get(spreadsheetId=sid,range=r).execute()
        d=k['values']
        df=pd.DataFrame(data=d[1:],columns=d[0]) 
        l=[]
        for i in range(0,len(df)):
            t=df._get_value(i,c)
            pred=mymodel.polarity_scores(t)
            if (pred['compound']>0.5):
                l.append("positive")
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        df.to_csv("results.csv",index=False)
        st.subheader("The analysis is saved in results.csv file")
elif(choice=="Results"):
    df=pd.read_csv("results.csv")
    choice2=st.selectbox("Choose visualization",("None","Pie chart","Histogram","Scatterplot"))
    st.dataframe(df)
    if(choice2=="Pie chart"):
        posper=(len(df[df['Sentiment']=='positive'])/len(df))*100
        neuper=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        fig=px.pie(values=[posper,neuper,negper],names=['positive','Neutral','Negative'])
        st.plotly_chart(fig)
    elif(choice2=="Histogram"):
        k=st.selectbox("Choose column",df.columns)
        if k:
            fig=px.histogram(x=df[k],color=df['Sentiment'])
            st.plotly_chart(fig)
    elif(choice2=="Scatterplot"):
        k=st.text_input("Enter the column name")
        if k:
            fig=px.scatter(x=df[k],y=df['Sentiment'])
            st.plotly_chart(fig)