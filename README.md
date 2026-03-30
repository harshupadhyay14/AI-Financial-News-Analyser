# 🚀 AI Financial News Analyzer
An end-to-end AI-powered financial intelligence system that processes real-time news, extracts insights, and enables intelligent querying using a RAG-based chatbot.

# 🌐 Live Demo
🚀 Frontend App:
https://ai-financial-news-analyser-frontend.onrender.com
⚡ Backend API:
https://ai-financial-news-analyser-api.onrender.com

# 📌 Overview
The AI Financial News Analyzer leverages LLMs + NLP techniques to transform raw financial news into actionable insights.
It performs:
📈 Market sentiment detection (Bullish / Bearish / Neutral)
🏢 Company & stock ticker extraction
📊 Sector-wise analysis
💬 Context-aware Q&A using Retrieval-Augmented Generation (RAG)

# 🧠 Key Features
✅ Real-time financial news scraping
✅ LLM-powered sentiment analysis (Groq LLaMA)
✅ Company & ticker extraction using NLP + Regex
✅ RAG-based chatbot with source-aware responses
✅ Interactive dashboard with Plotly visualizations
✅ Full-stack architecture (FastAPI + Flask)


# 🏗️ Tech Stack
🔹 Backend
Python
FastAPI
Groq LLaMA (LLM)
NLP (Regex + Text Processing)
🔹 Frontend
Flask
HTML, CSS
🔹 Data & Visualization
Pandas
Plotly
🔹 Tools
REST APIs
Git & GitHub

# 📂 Project Structure
AI_Financial_News_Analyzer/
│
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── sentiment.py
│   ├── embeddings.py
│   ├── company_extractor.py
│   └── news_scraper.py
│
├── frontend/
│   ├── app.py
│   ├── templates/
│   └── requirements.txt
│
└── README.md

# ⚙️ Installation & Setup
1️⃣ Clone the Repository
Bash
git clone https://github.com/harshupadhyay14/AI-Financial-News-Analyser.git
cd AI-Financial-News-Analyser

2️⃣ Create Virtual Environment
Bash
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
Bash
pip install -r frontend/requirements.txt

4️⃣ Add Environment Variables
Create a .env file:

GROQ_API_KEY=your_api_key_here

# ▶️ Running the Application
🔹 Start Backend
Bash
cd backend
uvicorn main:app --reload
🔹 Start Frontend
Bash
cd frontend
python app.py

# 📊 Feature Breakdown
🔹 Sentiment Analysis
Classifies financial news into:
📈 Bullish
📉 Bearish
⚖️ Neutral

🔹 RAG Chatbot
Context-aware answers
Uses latest scraped news
Provides source-based responses

🔹 Interactive Dashboard
Sector-wise sentiment distribution
Dynamic charts powered by Plotly

# 🚀 Deployment
Backend: Render
Frontend: Railway

# 📈 Resume Impact
Built a full-stack AI system analyzing real-time financial news using LLMs
Engineered a RAG-based chatbot with NLP-driven entity extraction
Developed a production-ready architecture with fast response times (<500ms)

# 🤝 Contributing
Contributions are welcome!
For major changes, please open an issue first to discuss your ideas.
📬 Contact
Harsh Upadhyay
💻 GitHub: https://github.com/harshupadhyay14⁠�
📧 LinkedIn: https://www.linkedin.com/in/harsh-u-53119124b
