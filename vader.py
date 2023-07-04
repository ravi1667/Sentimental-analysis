from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
mymodel=SentimentIntensityAnalyzer()
k=input("enter the text")
pred=mymodel.polarity_scores(k)
if (pred['compound']>0.5):
    print("Sentiment is positive")
elif(pred['compound']<-0.5):
    print("Sentiment is negative")
else:
    print("sentiment is neutral")