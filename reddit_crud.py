import os
import praw
import re
from utils import logger

# Initialize the Reddit client
def initialize_reddit():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    user_agent = os.getenv("USER_AGENT")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    if not all([client_id, client_secret, user_agent, username, password]):
        logger.error("Missing one or more required environment variables.")
        return None

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        reddit.validate_on_submit = True
        logger.info("Reddit client initialized successfully.")
        return reddit
    except Exception as e:
        logger.error(f"Error initializing Reddit client: {e}")
        return None

# Create a new post
def create_post(reddit, subreddit_name, title, content):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title, selftext=content)
        logger.info(f"Post created in r/{subreddit_name}: {title} (ID: {submission.id})")
        return submission.url
    except Exception as e:
        logger.error(f"An error occurred while creating the post: {e}")
        return f"Error: {e}"

# Read user's posts
def read_user_posts(reddit, limit=10):
    try:
        posts = [
            (sub.display_name, sub.title, sub.id, sub.score, sub.url)
            for sub in reddit.user.me().submissions.new(limit=limit)
        ]
        return posts
    except Exception as e:
        logger.error(f"An error occurred while reading user posts: {e}")
        return f"Error: {e}"

# Update a post's title and content
def update_post(reddit, post_url, new_title, new_content):
    submission_id = extract_submission_id(post_url)
    if not submission_id:
        return "Invalid URL. Please provide a valid Reddit post URL."

    try:
        submission = reddit.submission(id=submission_id)
        if submission.author != reddit.user.me():
            return "You are not the author of this post, so it cannot be updated."

        submission.edit(new_content)
        logger.info(f"Post updated: {new_title} (ID: {submission.id})")
        return submission.url
    except Exception as e:
        logger.error(f"An error occurred while updating the post: {e}")
        return f"Error: {e}"

# Delete a post
def delete_post(reddit, post_url):
    submission_id = extract_submission_id(post_url)
    if not submission_id:
        return "Invalid URL. Please provide a valid Reddit post URL."

    try:
        submission = reddit.submission(id=submission_id)
        if submission.author != reddit.user.me():
            return "You are not the author of this post, so it cannot be deleted."

        submission.delete()
        logger.info(f"Post deleted: {submission_id}")
        return "Post deleted successfully!"
    except Exception as e:
        logger.error(f"An error occurred while deleting the post: {e}")
        return f"Error: {e}"

# Extract submission ID from URL
def extract_submission_id(url):
    pattern = r'reddit\.com/r/.+/comments/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None
