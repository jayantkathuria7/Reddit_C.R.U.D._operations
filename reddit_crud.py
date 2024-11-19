import os
import praw
import logging
import re
import time
from datetime import datetime
from threading import Thread
import pytz

# Set up logging
logger = logging.getLogger(__name__)

# Function to initialize the Reddit client using credentials from environment variables
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

# Function to extract submission ID from URL
def extract_submission_id(url):
    pattern = r'reddit\.com/r/.+/comments/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Function to create a new post
def create_post(reddit, subreddit_name, title, content):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title, selftext=content)
        logger.info(f"Post created in r/{subreddit_name}: {title} (ID: {submission.id})")
        return submission.url
    except Exception as e:
        logger.error(f"An error occurred while creating the post: {e}")
        return f"Error: {e}"

# Function to schedule a post
import time
from datetime import datetime
import logging


def schedule_post(reddit, subreddit_name, title, content, scheduled_datetime):
    """
    Schedules the post to be made at the specified time.

    Parameters:
        reddit (praw.Reddit): The authenticated Reddit instance.
        subreddit_name (str): The name of the subreddit to post to.
        title (str): The title of the Reddit post.
        content (str): The content (body) of the Reddit post.
        scheduled_datetime (datetime): The datetime object representing when the post should be created.
    """
    try:
        # Wait until the scheduled time
        current_time = datetime.now()

        # If the scheduled time is in the future, wait until that time
        while current_time < scheduled_datetime:
            time_difference = (scheduled_datetime - current_time).total_seconds()

            if time_difference > 10:
                time.sleep(10)  # Sleep for 10 seconds if the time difference is more than 10 seconds
            else:
                time.sleep(time_difference)  # Sleep exactly until the scheduled time

            current_time = datetime.now()

        # Now that the scheduled time has passed, create the post
        post_url = create_post(reddit, subreddit_name, title, content)
        logging.info(f"Post successfully scheduled and created! [View post]({post_url})")
        return f"Post successfully scheduled and created! [View post]({post_url})"

    except Exception as e:
        logging.error(f"Error creating post: {str(e)}")
        return f"Error creating post: {str(e)}"


# Function to read and display the latest posts from a subreddit
def read_user_posts(reddit, limit=10):
    try:
        posts = []
        for submission in reddit.user.me().submissions.new(limit=limit):
            posts.append((submission.subreddit, submission.title, submission.id, submission.score, submission.url))
        return posts
    except Exception as e:
        logger.error(f"An error occurred while reading user posts: {e}")
        return f"Error: {e}"

# Function to update a post's title and content with ownership check
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

# Function to delete a post with ownership check
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
