import os
import re
import time
from groq import Groq
from dotenv import load_dotenv
 
load_dotenv()
 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
# ── simple in-process rate limiter ────────────────────────────────────────────
_call_times = []          # timestamps of recent API calls
RPM_LIMIT    = 25         # stay safely under Groq's 30 RPM limit
MIN_INTERVAL = 60 / RPM_LIMIT   # minimum seconds between calls (~2.4s)
 
def _wait_for_rate_limit():
    """Block until we're allowed to make another Groq call."""
    now = time.time()
    # Remove timestamps older than 60s
    global _call_times
    _call_times = [t for t in _call_times if now - t < 60]
 
    if len(_call_times) >= RPM_LIMIT:
        # We've hit the limit — wait until the oldest call expires
        sleep_for = 60 - (now - _call_times[0]) + 0.5
        if sleep_for > 0:
            print(f"⏳ Rate limit: waiting {sleep_for:.1f}s before next Groq call...")
            time.sleep(sleep_for)
 
    # Also enforce minimum gap between consecutive calls
    if _call_times:
        gap = time.time() - _call_times[-1]
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
 
    _call_times.append(time.time())
 
 
# ── keyword fallback (used when Groq is unavailable) ──────────────────────────
def _keyword_sentiment(text):
    t = text.lower()
    bullish_words = ["surge","rally","gains","strong","bull","upgrade","rise","rises",
                     "higher","record","beat","beats","profit","growth","positive","up"]
    bearish_words = ["decline","fall","falls","loss","weak","bear","downgrade","drop",
                     "drops","lower","miss","misses","negative","down","concern","risk"]
    b = sum(1 for w in bullish_words if w in t)
    r = sum(1 for w in bearish_words if w in t)
    if b > r:
        return {"sentiment": "📈 Bullish",  "confidence": "65", "analysis": text[:150]}
    elif r > b:
        return {"sentiment": "📉 Bearish",  "confidence": "65", "analysis": text[:150]}
    else:
        return {"sentiment": "➡️ Neutral",  "confidence": "50", "analysis": text[:150]}
 
 
# ── main function ─────────────────────────────────────────────────────────────
def analyze_news(text):
    """Analyze sentiment via Groq with rate-limit handling and keyword fallback."""
    try:
        _wait_for_rate_limit()
 
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{
                "role": "user",
                "content": (
                    "Analyze this financial news headline and respond with EXACTLY this format:\n"
                    "SENTIMENT: [BULLISH or BEARISH or NEUTRAL]\n"
                    "CONFIDENCE: [number 0-100]\n"
                    "ANALYSIS: [1 sentence]\n\n"
                    f"News: {text}"
                )
            }],
            max_tokens=100,
        )
 
        raw = response.choices[0].message.content
 
        # parse
        sentiment = "➡️ Neutral"
        if "BULLISH" in raw.upper():   sentiment = "📈 Bullish"
        elif "BEARISH" in raw.upper(): sentiment = "📉 Bearish"
 
        conf_m = re.search(r"CONFIDENCE:\s*(\d+)", raw)
        confidence = conf_m.group(1) if conf_m else "70"
 
        anal_m = re.search(r"ANALYSIS:\s*(.+?)(?:\n|$)", raw, re.DOTALL)
        analysis = anal_m.group(1).strip()[:200] if anal_m else text[:150]
 
        return {"sentiment": sentiment, "analysis": analysis, "confidence": confidence, "raw": raw}
 
    except Exception as e:
        # 429 or any other error → fall back to keywords
        if "429" in str(e):
            print(f"⚠ Rate limit hit — using keyword fallback for: {text[:60]}...")
        else:
            print(f"Groq API Error: {e}")
        return _keyword_sentiment(text)