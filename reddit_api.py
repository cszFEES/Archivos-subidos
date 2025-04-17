
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

import praw
reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent="script:myredditapp:v1.0 (by u/your_reddit_username)",
    username=config['reddit']['username'],
    password=config['reddit']['password']
)
#print(reddit.user.me())

try:
    subreddit_name = "learnpython"
    subreddit = reddit.subreddit(subreddit_name)
    print(f"\nLatest 5 posts from r/{subreddit_name}:\n")
    for submission in subreddit.new(limit=5):
        print(f"Title: {submission.title}")
        print(f"Author: {submission.author}")
        print(f"Upvotes: {submission.score}\n")
except Exception as e:
    print(e)