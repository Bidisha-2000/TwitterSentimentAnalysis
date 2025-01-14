import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , redirect, url_for, request

import emoji
import pandas as pd

def clean_tweet( tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment( tweet): 
        
        # analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer()) 

        # if analysis.sentiment.classification == "pos": 
        #     return 'positive'
        # elif analysis.sentiment.classification == "neg": 
        #     return 'negative'

        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"


def get_tweets(api, query, c):
    
    
    count = int(c)
    tweets = [] 
    tweets = api.user_timeline(screen_name=query, count=count,
                           tweet_mode='extended')

    # create DataFrame
    m=[]
    columns = ['User', 'Tweet']
    data = []
    x=[]
    for tweet in tweets:
        j = emoji.demojize(tweet.full_text)

        data.append([tweet.user.screen_name, j])
        x.append(j)

    df = pd.DataFrame(data, columns=columns)
    
    po=ne=n=0
    for text in x:
        blob = TextBlob(text)
        key=text
        if blob.sentiment.polarity > 0:
            text_sentiment = "positive"
            po+=1
            
        elif blob.sentiment.polarity == 0:
            text_sentiment = "neutral"
            ne+=1
        else:
            text_sentiment = "negative"
            n+=1
        sentiment=text_sentiment
        m.append({"text":key,"sentiment":sentiment})
    return m #returning nested dictionary

        

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

# ******Phrase level sentiment analysis
@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            fetched_tweets = get_tweets(api,query, count) 
            return render_template('result.html', result=fetched_tweets)

# fetched_tweets


# *******Sentence level sentiment analysis
@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0:
                text_sentiment = "positive"
            elif blob.sentiment.polarity == 0:
                text_sentiment = "neutral"
            else:
                text_sentiment = "negative"
            return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':
    
    consumerKey = "kyRQF7cFHe4qgecZG0knT26xM"
    consumerSecret = "ksQcnURKquWNOeiq1NBUmRvF1Q3mntwK5GS1Z8idP55s9R5F9j"
    accessToken = "1574783882091642880-xDPEEHEYJp1I7PVuoVdYSJjqdlh2Ct"
    accessTokenSecret = "sKCjx2Q3iGlIg1FctYGbLdpy5jgDGkpIbIyNwgruhuMQo"

    try: 
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
    except: 
        print("Error: Authentication Failed") 

    app.debug=True
    app.run(host='localhost')

