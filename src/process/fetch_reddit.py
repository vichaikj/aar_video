"""Take the top post reddit in Ask-Reddit sub, and select the best long-enough comment"""
from html import unescape
import re

import praw
import toml

from variables import logins_path, ideas_path, story_path

# Read Reddit bot credentials
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

# Keywords that may indicate a post asking for stories
story_keywords = [
    "story", "share your", "personal experience", "what is your", "most",
    "memorable", "experience", "afraid", "fear"
]

# Already done ideas
with open(ideas_path, "r") as ideas_file:
    done_videos = [line.strip().lower() for line in ideas_file]

# Fetch the top posts from the subreddit
top_posts = subreddit.top(time_filter="year", limit=100)

# Number of story
_LIMIT = 1

# Minimum characters in comment
MIN_CHARS = 600

# Depth of comments, 0 means not including any sub-comments
COM_DEPTH = 0

# Score minimum for the comment
MIN_SCORE = 5000


def clean_text(to_clean):
    # Combine patterns and exclude text between square brackets
    combined_pattern = re.compile(
        r'(?i)&#[xX]?(?P<code>[0-9a-fA-F]+);|http[s]?://(?:[^\s]+)|[^a-zA-Z0-9.,?!\'":\s]'
    )

    # Use sub to replace the combined pattern in a single pass
    return combined_pattern.sub("", to_clean)


def fetch_topic(limit=_LIMIT):
    story_number = 0
    for submission in top_posts:
        # Check if the post is from the last month
        title = submission.title.lower()
        if any(keyword in title and title not in done_videos for keyword in story_keywords):
            # Fetch and filter comments for each post
            submission.comments.replace_more(limit=0)
            comment_list = submission.comments.list()
            filtered_comments = [
                comment
                for comment in comment_list
                if len(comment.body) > MIN_CHARS and comment.depth == COM_DEPTH and comment.score > MIN_SCORE
            ]

            if filtered_comments:
                # Sort comments by score in descending order
                sorted_comments = sorted(filtered_comments, key=lambda x: x.score, reverse=True)

                # Get the top comment information
                top_comment = sorted_comments[0]
                print(f"Title: {submission.title}")
                print(f"URL: {submission.url}")
                print(f"Post score: {submission.score}")
                print(f"Top Comment score: {top_comment.score}")
                print(f"Top Comment: \n{clean_text(unescape(top_comment.body))}")

                with open(story_path, "w") as out_file:
                    out_file.write(submission.title + "\n" + clean_text(unescape(top_comment.body)))

                story_number += 1
                if story_number >= limit:
                    break
            else:
                print(f"No comments above {MIN_CHARS} characters.")

            print("\n" + "-"*50 + "\n")


fetch_topic()
