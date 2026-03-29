import sys
print("🚀 Step 1: Python started")
 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
print("✅ Step 2: FastAPI imported")
 
try:
    from news_scraper import fetch_news
    print("✅ Step 3: news_scraper loaded")
except Exception as e:
    print(f"❌ Step 3 FAILED: {e}")
    def fetch_news(): return []
 
try:
    from sentiment import analyze_news
    print("✅ Step 4: sentiment loaded")
except Exception as e:
    print(f"❌ Step 4 FAILED: {e}")
    def analyze_news(t): return {"sentiment": "➡️ Neutral", "analysis": t[:100], "confidence": "50"}
 
try:
    from company_extractor import extract_companies, get_sector_from_text
    print("✅ Step 5: company_extractor loaded")
except Exception as e:
    print(f"❌ Step 5 FAILED: {e}")
    def extract_companies(t): return {"companies": [], "sectors": []}
    def get_sector_from_text(t): return "General"
 
# NOTE: rag.py and embeddings.py are NOT imported — they load SentenceTransformer
# which hangs the server. We use keyword RAG instead (faster, no GPU needed).
print("✅ Step 6: using lightweight keyword RAG (no SentenceTransformer)")
 
app = FastAPI()
print("🚀 FastAPI app created successfully!")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ── in-memory store (reset on each /news call) ─────────────────────────────────
news_database = []
sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
sector_sentiment = {}
 
 
@app.get("/")
def home():
    return {"message": "AI Financial News Analyzer API 🚀", "status": "running"}
 
 
@app.get("/news")
def get_news():
    global news_database, sentiment_counts, sector_sentiment
 
    # ✅ RESET everything on each fetch — prevents duplicate stacking
    news_database = []
    sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
    sector_sentiment = {}
 
    try:
        raw_news = fetch_news()
        for item in raw_news:
            title = item["title"]
            analysis = analyze_news(title)
            companies_data = extract_companies(title)
            sector = get_sector_from_text(title)
 
            sentiment_str = analysis.get("sentiment", "➡️ Neutral")
            key = "bullish" if "📈" in sentiment_str else "bearish" if "📉" in sentiment_str else "neutral"
            sentiment_counts[key] += 1
 
            if sector not in sector_sentiment:
                sector_sentiment[sector] = {"bullish": 0, "bearish": 0, "neutral": 0}
            sector_sentiment[sector][key] += 1
 
            news_database.append({
                "title": title,
                "sentiment": sentiment_str,
                "analysis": analysis.get("analysis", title[:100]),
                "confidence": analysis.get("confidence", "50"),
                "companies": companies_data.get("companies", []),
                "sectors": companies_data.get("sectors", [sector]),
                "sector": sector,
            })
 
        return news_database
 
    except Exception as e:
        return {"error": str(e)}
 
 
@app.get("/metrics")
def get_metrics():
    total = sum(sentiment_counts.values())
    if total == 0:
        return {"error": "No data yet — fetch news first", "total_articles": 0}
    return {
        "sentiment_distribution": sentiment_counts,
        "sector_sentiment": sector_sentiment,
        "total_articles": total,
        "bullish_percentage": round(sentiment_counts["bullish"] / total * 100, 1),
        "bearish_percentage": round(sentiment_counts["bearish"] / total * 100, 1),
        "neutral_percentage": round(sentiment_counts["neutral"] / total * 100, 1),
    }
 
 
@app.get("/companies")
def get_all_companies():
    seen = {}
    for article in news_database:
        for c in article.get("companies", []):
            if c["ticker"] not in seen:
                seen[c["ticker"]] = {**c, "articles": []}
            seen[c["ticker"]]["articles"].append(article["title"])
    return {"companies": list(seen.values())}
 
 
@app.get("/ask")
def ask_question(query: str):
    """Keyword-based RAG — scores every article against the query and returns top 3."""
 
    if not news_database:
        return {
            "question": query,
            "answer": "❌ No news loaded yet. Please click 'Load / Refresh News' first.",
            "sources": [],
            "articles_analyzed": 0,
        }
 
    q = query.lower()
    scored = []
 
    for article in news_database:
        score = 0
        combined = (article.get("title", "") + " " + article.get("analysis", "")).lower()
        sentiment = article.get("sentiment", "")
 
        # sentiment intent
        if any(w in q for w in ["bullish","positive","rising","gains","up","rally","strong"]):
            if "📈" in sentiment: score += 10
        if any(w in q for w in ["bearish","negative","falling","loss","down","decline","weak"]):
            if "📉" in sentiment: score += 10
        if any(w in q for w in ["neutral","stable","flat","steady","unchanged"]):
            if "➡️" in sentiment: score += 10
 
        # sector
        for s in article.get("sectors", []):
            if s.lower() in q: score += 8
 
        # company / ticker
        for c in article.get("companies", []):
            if c.get("name","").lower() in q: score += 12
            if c.get("ticker","").lower() in q: score += 12
 
        # general keyword overlap (skip tiny words)
        for word in q.split():
            if len(word) > 3 and word in combined:
                score += 3
 
        scored.append((score, article))
 
    # sort descending — always return top 3 even if score is 0
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [a for _, a in scored[:3]]
 
    titles = [a["title"] for a in top]
    sentiments = [a["sentiment"] for a in top]
 
    all_companies, all_sectors = [], []
    for a in top:
        for c in a.get("companies", []):
            if c["ticker"] not in [x["ticker"] for x in all_companies]:
                all_companies.append(c)
        for s in a.get("sectors", []):
            if s not in all_sectors:
                all_sectors.append(s)
 
    answer = "Based on the latest financial news:\n\n"
    answer += "Key Headlines:\n"
    for i, t in enumerate(titles, 1):
        answer += f"{i}. {t}\n"
    if all_companies:
        answer += "\nCompanies Mentioned: " + ", ".join(f"{c['ticker']} ({c['name']})" for c in all_companies[:4]) + "\n"
    if all_sectors:
        answer += f"\nSectors: {', '.join(all_sectors)}\n"
    answer += f"\nMarket Sentiment: {', '.join(dict.fromkeys(sentiments))}\n"
    answer += f"\n📊 Analysed {len(top)} relevant articles."
 
    return {
        "question": query,
        "answer": answer,
        "sources": titles,
        "sentiment": sentiments,
        "articles_analyzed": len(top),
    }