from html import unescape
import os
import re
from datetime import datetime, timedelta

import praw
import toml

# Read Reddit bot credentials
script_dir = os.path.dirname(os.path.abspath(__file__))
logins_path = os.path.join(script_dir, "../resources/logins.toml")
with open(logins_path, "r") as login_toml:
    logins = toml.load(login_toml)

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=logins["reddit_bot"]["CLIENT_ID"],
    client_secret=logins["reddit_bot"]["CLIENT_SECRET"],
    user_agent="mozilla"
)

# Specify the subreddit you want to fetch data from
subreddit = reddit.subreddit("AskReddit")

# Timestamp one month ago
one_month_ago_timestamp = int((datetime.utcnow() - timedelta(days=30)).timestamp())

# Keywords that may indicate a post asking for stories
story_keywords = [
    "story", "share your", "personal experience", "what is your", "most", "memorable", "experience", "afraid", "fear"
]

# Already done ideas
ideas_path = os.path.join(script_dir, "../resources/done_ideas.txt")
with open(ideas_path, "r") as ideas_file:
    done_videos = [line.strip().lower() for line in ideas_file]

# Fetch the top posts from the subreddit
top_posts = subreddit.top(time_filter="month", limit=100)

# Output file: raw text composed of Title + best comment
story_path = os.path.join(script_dir, "../resources/story.txt")

# Number of story
_LIMIT = 1
# Init number, to not modify
_STORY_NUMBER = 0


def fetch_topic(limit=_LIMIT, story_number=_STORY_NUMBER):
    for submission in top_posts:
        # Check if the post is from the last month
        title = submission.title.lower()
        if submission.created_utc > one_month_ago_timestamp:
            if any(keyword in title and title not in done_videos for keyword in story_keywords):
                # Fetch and filter comments for each post
                submission.comments.replace_more(limit=0)
                comment_list = submission.comments.list()
                filtered_comments = [
                    comment
                    for comment in comment_list
                    if len(comment.body) > 700 and comment.depth == 0 and comment.score > 5000
                ]

                if filtered_comments:
                    # Sort comments by score in descending order
                    sorted_comments = sorted(filtered_comments, key=lambda x: x.score, reverse=True)

                    # Regex to remove patterns such as "&#x200B;"
                    pattern = re.compile(r"&#[xX]?(?P<code>[0-9a-fA-F]+);")

                    # Get the top comment information
                    top_comment = sorted_comments[0]
                    print(f"Title: {submission.title}")
                    print(f"URL: {submission.url}")
                    print(f"Top Comment score: {top_comment.score}")
                    print(f"Top Comment: \n{pattern.sub('', unescape(top_comment.body))}")

                    with open(story_path, "w") as out_file:
                        out_file.write(submission.title + "\n" + pattern.sub('', unescape(top_comment.body)))

                    story_number += 1
                    if story_number >= limit:
                        break
                else:
                    print("No comments above 700 characters.")

                print("\n" + "-"*50 + "\n")
