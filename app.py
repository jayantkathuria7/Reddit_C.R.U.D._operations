import streamlit as st
import praw
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from threading import Thread
import pandas as pd
from io import StringIO

# Import custom modules
from reddit_crud import create_post, read_user_posts, update_post, delete_post, schedule_post
from analytics import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit app layout
st.title("Reddit Bot 🤖")

# Sidebar navigation
sidebar = st.sidebar.selectbox("Select a Section", ["CRUD Operations 📝", "Analytics Dashboard 📊"])

# Credentials upload
uploaded_file = st.file_uploader("Upload your credentials.env file 📁", type=["env"])

# Load credentials and initialize Reddit client
if uploaded_file:
    try:
        # Read the content of the uploaded file
        content = uploaded_file.getvalue().decode("utf-8")

        # Use StringIO to simulate a file for dotenv
        env_data = StringIO(content)
        load_dotenv(stream=env_data)

        logger.info("Credentials loaded successfully from uploaded file.")
    except Exception as e:
        logger.error(f"Failed to load credentials from file: {e}")
        st.error("Failed to load credentials. Please upload a valid .env file.")
        st.stop()
else:
    st.error("No file uploaded. Please upload your credentials.env file.")
    st.stop()

# Initialize Reddit client
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

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
except Exception as e:
    logger.error(f"Error initializing Reddit client: {e}")
    st.stop()

# CRUD Operations Section
if sidebar == "CRUD Operations 📝":
    st.header("CRUD Operations 📝")
    crud_tab = st.selectbox("Choose CRUD Operation", [
        "Create Post ✨",
        "Read My Posts 📖",
        "Update Post ✏️",
        "Delete Post 🗑️",
        "Schedule Post 🕒"
    ])

    # Create Post
    if crud_tab == "Create Post ✨":
        st.subheader("Create a New Post ✨")
        subreddit_name = st.text_input("Enter Subreddit Name", key="create_subreddit_name")
        title = st.text_input("Enter Post Title", key="create_title")
        content = st.text_area("Enter Post Content", key="create_content")

        if st.button("Create Post 📬"):
            if not all([subreddit_name, title, content]):
                st.error("Please fill in all fields 🛑")
            else:
                post_url = create_post(reddit, subreddit_name, title, content)
                st.write(
                    f"Post created successfully! [View post]({post_url})" if "Error" not in post_url else post_url)

    # Read Posts
    elif crud_tab == "Read My Posts 📖":
        st.subheader("Read Your Latest Posts 📖")
        limit = st.number_input("Enter the number of posts to display", min_value=1, max_value=50, value=10)

        if st.button("Read My Posts 📜"):
            posts = read_user_posts(reddit, limit)
            if isinstance(posts, list):
                for subreddit, title, post_id, score, url in posts:
                    st.write(
                        f"Subreddit: r/{subreddit} | Title: {title} | ID: {post_id} | Upvotes: {score} | [Link]({url})")
            else:
                st.write(posts)

    # Update Post
    elif crud_tab == "Update Post ✏️":
        st.subheader("Update an Existing Post ✏️")
        post_url = st.text_input("Enter Post URL to Update", key="update_post_url")
        new_title = st.text_input("Enter New Title", key="update_title")
        new_content = st.text_area("Enter New Content", key="update_content")

        if st.button("Update Post 🔄"):
            if not post_url:
                st.error("Please provide a post URL 🛑")
            else:
                result = update_post(reddit, post_url, new_title, new_content)
                st.write(f"Post updated successfully! [View post]({result})" if "Error" not in result else result)

    # Delete Post
    elif crud_tab == "Delete Post 🗑️":
        st.subheader("Delete a Post 🗑️")
        post_url = st.text_input("Enter Post URL to Delete", key="delete_post_url")

        if st.button("Delete Post 🗑️"):
            if not post_url:
                st.error("Please provide a post URL 🛑")
            else:
                result = delete_post(reddit, post_url)
                st.write(result)

    # Schedule Post
    elif crud_tab == "Schedule Post 🕒":
        st.subheader("Schedule a Post 🕒")
        subreddit_name = st.text_input("Enter Subreddit Name", key="schedule_subreddit_name")
        title = st.text_input("Enter Post Title", key="schedule_title")
        content = st.text_area("Enter Post Content", key="schedule_content")

        scheduled_time = st.date_input("Pick a date 📅", key="schedule_date", format="DD/MM/YYYY")

        col1, col2 = st.columns(2)

        with col1:
            scheduled_hour = st.number_input("Pick an hour ⏰", 0, 23, key="schedule_hour")

        with col2:
            scheduled_minute = st.number_input("Pick a minute 🕔", 0, 59, key="schedule_minute")

        if scheduled_time and scheduled_hour is not None and scheduled_minute is not None:
            scheduled_datetime = datetime.combine(scheduled_time, datetime.min.time())
            scheduled_datetime = scheduled_datetime.replace(hour=scheduled_hour, minute=scheduled_minute)

            if st.button("Schedule Post 🗓️"):
                # Schedule the post in a new thread
                thread = Thread(target=schedule_post,
                                args=(reddit, subreddit_name, title, content, scheduled_datetime))
                thread.start()
                st.success(f"Post scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

# Analytics Dashboard Section
elif sidebar == "Analytics Dashboard 📊":
    st.header("Analytics Dashboard 📊")

    # Fetch analytics data
    try:
        post_data = get_post_analytics(reddit)
        engagement_data = get_engagement_analytics(reddit)
        growth_data = get_growth_analytics(reddit)
    except Exception as e:
        st.error(f"Error fetching analytics data: {e}")
        post_data = engagement_data = growth_data = None

    # Overview Section
    st.subheader("Overview Analytics 📊")
    if post_data is not None:
        page = st.selectbox("Choose Dashboard Section", [
            "Post Analytics 📊",
            "Engagement Insights 📈",
            "Growth Metrics 📅"
        ])

        if page == "Post Analytics 📊":
            st.subheader("Post Analytics 📊")
            # Display post details table
            post_table_fig = post_details_table(post_data)
            st.plotly_chart(post_table_fig)

            # Display post scores chart (Upvotes)
            post_scores_fig = post_scores_chart(post_data)
            st.plotly_chart(post_scores_fig)

            # Display post frequency chart
            post_frequency_fig = post_frequency_chart(post_data)
            st.plotly_chart(post_frequency_fig)

            # Display Word Cloud for post titles
            wordcloud_img = word_cloud_chart(post_data)
            st.image(wordcloud_img, caption="Word Cloud for Post Titles")

        elif page == "Engagement Insights 📈":
            st.subheader("Engagement Insights 📈")
            engagement_titles = [engage['title'] for engage in engagement_data]
            upvote_ratios = [engage['upvote_ratio'] for engage in engagement_data]
            num_comments = [engage['num_comments'] for engage in engagement_data]

            st.write("Upvote Ratios and Number of Comments for Recent Posts:")
            engagement_fig = px.bar(
                x=engagement_titles,
                y=upvote_ratios,
                labels={'x': 'Post Title', 'y': 'Upvote Ratio'},
                title="Engagement Metrics (Upvote Ratio)"
            )
            st.plotly_chart(engagement_fig)

            st.write("Number of Comments per Post:")
            comments_fig = px.bar(
                x=engagement_titles,
                y=num_comments,
                labels={'x': 'Post Title', 'y': 'Number of Comments'},
                title="Post Engagement (Number of Comments)"
            )
            st.plotly_chart(comments_fig)

        elif page == "Growth Metrics 📅":
            st.subheader("Growth Metrics 📅")
            # Display Post Frequency Chart (Growth over time)
            growth_frequency_fig = post_frequency_chart(post_data)
            st.plotly_chart(growth_frequency_fig)
