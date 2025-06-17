import os
import tweepy
import feedparser
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Twitter API 認証
client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Qiita組織のRSS URL
FEED_URL = "https://qiita.com/organizations/hackathon-challenge/activities.atom"

# 最後に取得した記事IDを保存（ローカルファイル使用）
LAST_ID_FILE = "last_qiita_id.txt"

def get_last_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_id(entry_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(entry_id)

def fetch_latest_entry():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return None
    return feed.entries[0]

def tweet_new_entry(entry):
    title = entry.title
    link = entry.link
    user = entry.author
    tweet = f"【Qiita更新】{title} by {user}\n{link} #Qiita #HackathonChallenge"
    client.create_tweet(text=tweet)
    print("✅ ツイートしました：", tweet)

def main():
    latest_entry = fetch_latest_entry()
    if not latest_entry:
        print("⚠️ フィードが空です")
        return

    last_id = get_last_id()
    if latest_entry.id != last_id:
        tweet_new_entry(latest_entry)
        save_last_id(latest_entry.id)
    else:
        print("🟢 新しい記事はありません")

if __name__ == "__main__":
    main()
