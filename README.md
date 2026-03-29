
# 🚀 AI Financial News Analyzer

An end-to-end AI-powered financial intelligence system that analyzes real-time news, detects market sentiment, extracts companies, and answers user queries using a RAG-based chatbot.

📌 Overview

This project fetches live financial news and uses LLMs + NLP techniques to generate actionable insights such as:

Market sentiment (Bullish / Bearish / Neutral)
Company & stock ticker extraction
Sector-wise analysis
Context-aware Q&A using RAG
🧠 Key Features

✅ Real-time financial news scraping
✅ Sentiment analysis using LLM (Groq LLaMA)
✅ Company & stock ticker extraction (NLP-based)
✅ RAG-powered chatbot with source-aware answers
✅ Interactive dashboard with Plotly visualizations
✅ Full-stack architecture (FastAPI + Flask)

🏗️ Tech Stack

Backend:

Python
FastAPI
Groq LLaMA (LLM)
NLP (Regex + Text Processing)

Frontend:

Flask
HTML, CSS

Data & Visualization:

Plotly
Pandas

Other Tools:

REST APIs
Git & GitHub
📂 Project Structure
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
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/harshupadhyay14/AI-Financial-News-Analyser.git
cd AI-Financial-News-Analyser
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r frontend/requirements.txt
4️⃣ Add Environment Variables

Create a .env file:

GROQ_API_KEY=your_api_key_here
5️⃣ Run Backend
cd backend
uvicorn main:app --reload
6️⃣ Run Frontend

Open new terminal:

cd frontend
python app.py
📊 Features Breakdown
🔹 Sentiment Analysis

Classifies news into:

Bullish 📈
Bearish 📉
Neutral ⚖️
🔹 RAG Chatbot
Context-aware answers
Uses latest news data
Provides source-based responses
🔹 Dashboard
Sector-wise sentiment distribution
Interactive charts using Plotly
🚀 Deployment
Backend: Render
Frontend: Railway
📈 Resume Impact
Built a full-stack AI system analyzing real-time financial news using LLMs
Engineered RAG-based chatbot with NLP-driven entity extraction
Deployed production-ready system with sub-500ms response time
🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

📬 Contact

Harsh Upadhyay
📧 Connect on LinkedIn
💻 GitHub: https://github.com/harshupadhyay14
