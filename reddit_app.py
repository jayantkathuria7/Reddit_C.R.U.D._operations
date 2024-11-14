import streamlit as st
import praw
import re
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file for credentials
load_dotenv("reddit_credentials.env")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to initialize the Reddit client using credentials from environment variables
# Function to initialize the Reddit client using credentials from environment variables
def initialize_reddit():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    user_agent = os.getenv("USER_AGENT")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")

    if not all([client_id, client_secret, user_agent, username, password]):
        logger.error("Missing one or more required environment variables.")
        st.error("Missing credentials. Please check your .env file.")
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
        st.error(f"Error initializing Reddit client: {e}")
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

# Function to read and display the latest posts from a subreddit
def read_user_posts(reddit, limit=10):
    """
    Reads and displays the latest posts by the authenticated user.
    
    Args:
        reddit (praw.Reddit): The initialized Reddit client.
        limit (int): The number of posts to retrieve.
        
    Returns:
        list: A list of tuples containing post details (subreddit, title, id, score, url).
    """
    try:
        posts = []
        for submission in reddit.user.me().submissions.new(limit=limit):
            posts.append((submission.subreddit.display_name, submission.title, submission.id, submission.score, submission.url))
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


# Streamlit app interface
st.title("Reddit Bot")

# Initialize Reddit client
reddit = initialize_reddit()
if reddit is None:
    st.stop()

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Create Post", "Read My Posts", "Update Post", "Delete Post"])

with tab1:
    st.header("Create a New Post")
    subreddit_name = st.text_input("Enter Subreddit Name", "")
    title = st.text_input("Enter Post Title", "")
    content = st.text_area("Enter Post Content", "")
    if st.button("Create Post"):
        post_url = create_post(reddit, subreddit_name, title, content)
        st.write(f"Post created successfully! [View post]({post_url})" if "Error" not in post_url else post_url)

with tab2:
    st.header("Read Your Latest Posts")
    limit = st.number_input("Enter the number of posts to display", min_value=1, max_value=50, value=10)
    if st.button("Read My Posts"):
        posts = read_user_posts(reddit, limit)
        if isinstance(posts, list):
            for subreddit, title, post_id, score, url in posts:
                st.write(f"Subreddit: r/{subreddit} | Title: {title} | ID: {post_id} | Upvotes: {score} | [Link]({url})")
        else:
            st.write(posts)

with tab3:
    st.header("Update an Existing Post")
    post_url = st.text_input("Enter Post URL to Update", "")
    new_title = st.text_input("Enter New Title", "")
    new_content = st.text_area("Enter New Content", "")
    if st.button("Update Post"):
        result = update_post(reddit, post_url, new_title, new_content)
        st.write(f"Post updated successfully! [View post]({result})" if "Error" not in result else result)

with tab4:
    st.header("Delete a Post")
    post_url = st.text_input("Enter Post URL to Delete", "")
    if st.button("Delete Post"):
        result = delete_post(reddit, post_url)
        st.write(result)