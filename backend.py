from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
mymodel=SentimentIntensityAnalyzer()
#Permission
f=InstalledAppFlow.from_client_secrets_file("key.json",["https://www.googleapis.com/auth/spreadsheets"])
cred=f.run_local_server(port=0)
service=build("Sheets","v4",credentials=cred).spreadsheets().values()
k=service.get(spreadsheetId="15R5fxxr4nilNTEsvaIHQB5l_OOrFIm1AIfO6RvNh2mU",range="B:F").execute()
d=k['values']
df=pd.DataFrame(data=d[1:],columns=d[0]) 
l=[]
for i in range(0,len(df)):
    t=df._get_value(i,"Opinion")
    pred=mymodel.polarity_scores(t)
    if (pred['compound']>0.5):
        d[i+1].append("positive")
    elif(pred['compound']<-0.5):
        d[i+1].append("Negative")
    else:
        d[i+1].append("Neutral")
h={'values':d}
service.update(spreadsheetId="15R5fxxr4nilNTEsvaIHQB5l_OOrFIm1AIfO6RvNh2mU",
range="B:G",valueInputOption="USER_ENTERED",body=h).execute()