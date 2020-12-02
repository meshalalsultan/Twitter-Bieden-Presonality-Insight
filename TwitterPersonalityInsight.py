#!pip install tweepy
#!pip install ibm_watson

# Import os to work with the operating system
import os 
# Import matplotlib 
from matplotlib import pyplot as plt
# Import seaborn
import seaborn as sns

# Import tweepy to work with the twitter API
import tweepy as tw

# Import pandas to work with dataframes
import pandas as pd

consumer_key = 'xgkA30ZnNtxpx5rZ4M2ZeADyt'
consumer_secret = 'xUiCmURo5NVXYVeNrL2pvO8br4B355zGBWrAwOCfa1L1yweZtE'
access_token = '1184086168608088064-YEY4L9ypjj3CfzeFN8C5knroTiDY26'
access_token_secret = 'PJPcRQVuXwLGVc3s21QGTIJUQCLk6g9CPshsD5NqJHom8'


# Authenticate
auth = tw.OAuthHandler(consumer_key, consumer_secret)
# Set Tokens
auth.set_access_token(access_token, access_token_secret)
# Instantiate API
api = tw.API(auth, wait_on_rate_limit=True)

handle = 'JoeBiden'

res = api.user_timeline(screen_name=handle, count=100, include_rts=True)

tweets = [tweet.text for tweet in res]

tweets

text = ''.join(str(tweet) for tweet in tweets)

text

# Import Watson
from ibm_watson import PersonalityInsightsV3

# Import authenticator
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = 'SZTVxTvY1_Ll0Hdp3u_6EGWZxPWFciNoPoNeLJF4XNWG'
url = 'https://gateway-lon.watsonplatform.net/personality-insights/api'

# Authenticate to PI service
authenticator = IAMAuthenticator(apikey)
personality_insights = PersonalityInsightsV3(
        version='2017-10-13', 
        authenticator=authenticator
)
personality_insights.set_service_url(url)

profile = personality_insights.profile(text, accept='application/json').get_result()
profile

for personality in profile['personality']:
    print(personality['name'], personality['percentile'])

for personality in profile['values']:
    print(personality['name'], personality['percentile'])

for personality in profile['needs']:
    print(personality['name'], personality['percentile'])

# Visualise profiles 
needs = profile['needs']
result = {need['name']:need['percentile'] for need in needs}
df = pd.DataFrame.from_dict(result, orient='index')
df.reset_index(inplace=True)
df.columns = ['need', 'percentile']

df.head()

# Create Plot
plt.figure(figsize=(15,5))
sns.barplot(y='percentile', x='need', data=df).set_title('Needs')
plt.show()

# Create plotting Function
def create_trait_plot(name, traits):
    result = {trait['name']:trait['percentile'] for trait in traits}
    df=pd.DataFrame.from_dict(result, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['need', 'percentile']
    plt.figure(figsize=(15,5))
    sns.barplot(y='percentile', x='need', data=df).set_title(name)
    plt.show()

[create_trait_plot(personality_trait['name'], personality_trait['children']) for personality_trait in profile['personality']]


