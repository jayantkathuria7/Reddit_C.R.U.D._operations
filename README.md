# Reddit CRUD Operations Bot 🤖

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-orange?style=for-the-badge&logo=streamlit)](https://reddit-crud-operations.streamlit.app/)  

## 📖 Project Overview

This project is a **Reddit Bot** powered by **Streamlit** and **PRAW (Python Reddit API Wrapper)** that allows users to perform **CRUD (Create, Read, Update, Delete) operations** on Reddit posts. It also includes an **Analytics Dashboard** to track post performance and user engagement.

🔗 **Live Demo**: [Reddit CRUD Operations App](https://reddit-crud-operations.streamlit.app/)  
📂 **GitHub Repository**: [Reddit CRUD Operations Bot](https://github.com/jayantkathuria7/Reddit_C.R.U.D._operations)

---

## 🚀 Features

### CRUD Operations 📝
- **Create**: Post new content to a subreddit.
- **Read**: Retrieve and display your recent posts.
- **Update**: Edit the title or content of an existing post.
- **Delete**: Remove a post by providing its URL.
- **Schedule**: Schedule posts to be published at a future date and time.

### Analytics Dashboard 📊
- **Post Analytics**: Analyze post frequency, upvotes, and view a word cloud of post titles.
- **Engagement Insights**: Track upvote ratios and comment counts.
- **Growth Metrics**: Monitor posting trends over time.

---

## 🛠️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/jayantkathuria7/Reddit_C.R.U.D._operations.git
cd Reddit_C.R.U.D._operations
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project directory with your Reddit API credentials:
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
USER_AGENT=your_user_agent
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

### 4. Run the App
```bash
streamlit run app.py
```

### 5. Access the App
Open the provided URL from the terminal in your browser.

---

## 📋 Usage Guide

1. **Upload `.env` File**: Upload your Reddit API credentials using the `.env` file uploader.
2. **Choose an Operation**: Select a CRUD operation or navigate to the Analytics Dashboard using the sidebar.

---

## 📚 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python (PRAW, dotenv, logging)
- **Data Visualization**: Plotly, Pandas

---

## 📊 Screenshots

### Home Screen
![Home Screen](https://github.com/user-attachments/assets/aed94b1e-751c-4511-83cb-ae39d054a3e7)


### CRUD Operations
![CRUD Operations](https://github.com/user-attachments/assets/0c0ec773-d75b-42fe-95a3-b71d9fc19194)

### Analytics Dashboard
![Analytics Dashboard](https://github.com/user-attachments/assets/2dcb7c52-7db9-4d14-87da-2378651af02a)

---

## 🚧 Future Enhancements

- **Sentiment Analysis**: Analyze comments for sentiment insights.
- **Enhanced Scheduling**: Add recurring post schedules.
- **Moderation Tools**: Automate community management tasks.

---

## 🤝 Contributing

Contributions are welcome!  
1. Fork the repository.  
2. Create a feature branch.  
3. Submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

### 👨‍💻 Developed by [Jayant Kathuria](https://github.com/jayantkathuria7)
```

You can replace the placeholder image URLs with actual screenshots of your project. Let me know if you need further adjustments!
