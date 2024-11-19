import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to create a table showing post details
def post_details_table(post_data):
    """
    Create a table showing post details including title, upvotes, comments, and URL.

    Parameters:
        post_data (list): A list of dictionaries, each containing post details.

    Returns:
        fig (plotly.graph_objects.Figure): A plotly figure representing the post details table.
    """
    # Create a DataFrame from the post data
    df = pd.DataFrame(post_data)

    # Create a table chart using plotly
    fig = go.Figure(go.Table(
        header=dict(values=["Title", "Upvotes", "Comments", "URL"]),
        cells=dict(values=[df['title'], df['upvotes'], df['comments'], df['url']])
    ))

    return fig

# Function to get post analytics
def get_post_analytics(reddit):
    posts = []
    for submission in reddit.user.me().submissions.new(limit=10):  # Adjust limit as needed
        post = {
            'title': submission.title,
            'upvotes': submission.score,
            'comments': submission.num_comments,
            'url': submission.url,
        }
        posts.append(post)
    return posts

# Function to get engagement analytics
def get_engagement_analytics(reddit):
    engagement_data = []
    for submission in reddit.user.me().submissions.new(limit=10):  # Adjust limit as needed
        engagement_data.append({
            'title': submission.title,
            'upvote_ratio': submission.upvote_ratio,
            'num_comments': submission.num_comments,
            'score': submission.score,
        })
    return engagement_data

# Function to get growth analytics
def get_growth_analytics(reddit):
    growth_data = []
    for submission in reddit.user.me().submissions.new(limit=10):  # Adjust limit as needed
        growth_data.append({
            'title': submission.title,
            'created_utc': submission.created_utc,  # Correct access for PRAW object
            'score': submission.score,
        })
    return growth_data


# Function to generate a post frequency chart
def post_frequency_chart(post_data):
    post_titles = [post['title'] for post in post_data]
    post_dates = []

    for post in post_data:
        try:
            post_dates.append(pd.to_datetime(post['created_utc'], unit='s'))  # Convert UTC to datetime
        except KeyError:
            post_dates.append(None)  # Handle missing 'created_utc' field

    # Create a DataFrame with post titles and post dates
    df = pd.DataFrame({'title': post_titles, 'date': post_dates})

    # Handle invalid datetime conversion gracefully
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.date

    # Count the frequency of posts per date
    post_frequency = df['date'].value_counts().sort_index()

    # Convert the post_frequency (Series) to DataFrame for Plotly compatibility
    post_frequency_df = post_frequency.reset_index()
    post_frequency_df.columns = ['date', 'post_count']  # Rename columns for clarity

    # Create the bar chart using Plotly
    fig = px.bar(post_frequency_df, x='date', y='post_count', labels={'x': 'Date', 'y': 'Post Count'})

    return fig

# Function to create a word cloud from post titles
def word_cloud_chart(post_data):
    text = ' '.join([post['title'] for post in post_data])
    wordcloud = WordCloud(width=800, height=400).generate(text)
    wordcloud_image = wordcloud.to_image()  # Convert to PIL image
    return wordcloud_image

# Function to create post scores chart
def post_scores_chart(post_data):
    post_titles = [post['title'] for post in post_data]
    post_scores = [post['upvotes'] for post in post_data]
    fig = px.bar(x=post_titles, y=post_scores, labels={'x': 'Post Title', 'y': 'Upvotes'})
    return fig

# Function to create follower count chart (mock data used for this example)
def follower_count_chart(followers_data):
    # Create a DataFrame with index as the x-axis
    df = pd.DataFrame({'follower_count': followers_data})
    df['index'] = df.index  # Adding an index as a column for the x-axis

    # Plot using the index as the x-axis
    fig = px.line(df, x='index', y='follower_count', title="Follower Count Over Time")
    return fig
