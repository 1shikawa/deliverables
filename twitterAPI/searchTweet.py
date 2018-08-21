# Tweepyライブラリをインポート
import tweepy
import config
import datetime

# 各種キーをセット
consumer_key    = config.CONSUMER_KEY
consumer_secret = config.CONSUMER_SECRET
access_key      = config.ACCESS_TOKEN
access_secret   = config.ACCESS_TOKEN_SECRET

#APIインスタンスを作成
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

print("検索内容を入力してください。")
search = input('>> ') #キーボード入力の取得
print('*******************************************')


for status in api.search(q='search', lang='ja', result_type='recent',count=10): #qに検索語句,countに検索結果の取得数
    print(status.user.name)#useridが出てくる
    print(status.user.screen_name)#ユーザー名が出てくる
    print(status.text) #ツイート内容が出てくる
    print(status.created_at+ datetime.timedelta(hours=9),format)