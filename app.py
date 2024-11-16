import streamlit as st
from reddit_crud import create_post, read_user_posts, update_post, delete_post, initialize_reddit
from utils import load_credentials_from_file

# Set up the Streamlit app interface
st.title("Reddit Bot")

# Upload credentials file
uploaded_file = st.file_uploader("Upload your credentials.env file", type=["env"])

# Load credentials and initialize Reddit client
if uploaded_file:
    if load_credentials_from_file(uploaded_file):
        reddit = initialize_reddit()
        if reddit is None:
            st.stop()
    else:
        st.stop()
else:
    st.warning("Please upload your .env file to proceed.")
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
