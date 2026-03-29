import re

# Common stock tickers and their sectors
STOCK_TICKERS = {
    "AAPL": {"name": "Apple", "sector": "Technology"},
    "MSFT": {"name": "Microsoft", "sector": "Technology"},
    "GOOGL": {"name": "Google", "sector": "Technology"},
    "AMZN": {"name": "Amazon", "sector": "Technology"},
    "TSLA": {"name": "Tesla", "sector": "Energy/Tech"},
    "META": {"name": "Meta", "sector": "Technology"},
    "NVDA": {"name": "Nvidia", "sector": "Technology"},
    "AMD": {"name": "AMD", "sector": "Technology"},
    "IBM": {"name": "IBM", "sector": "Technology"},
    "INTC": {"name": "Intel", "sector": "Technology"},
    "JPM": {"name": "JPMorgan", "sector": "Finance"},
    "BAC": {"name": "Bank of America", "sector": "Finance"},
    "GS": {"name": "Goldman Sachs", "sector": "Finance"},
    "BRK": {"name": "Berkshire Hathaway", "sector": "Finance"},
    "XOM": {"name": "ExxonMobil", "sector": "Energy"},
    "CVX": {"name": "Chevron", "sector": "Energy"},
    "COP": {"name": "ConocoPhillips", "sector": "Energy"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare"},
    "PFE": {"name": "Pfizer", "sector": "Healthcare"},
    "UNH": {"name": "UnitedHealth", "sector": "Healthcare"},
    "WMT": {"name": "Walmart", "sector": "Retail"},
    "MCD": {"name": "McDonald's", "sector": "Consumer"},
    "NKE": {"name": "Nike", "sector": "Consumer"},
}

# Company names to search for
COMPANY_NAMES = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Meta": "META",
    "Nvidia": "NVDA",
    "Goldman Sachs": "GS",
    "JPMorgan": "JPM",
}

def extract_companies(text):
    """Extract stock tickers and company names from text"""
    companies = []
    sectors = set()
    
    # Search for stock tickers
    for ticker, info in STOCK_TICKERS.items():
        if re.search(rf'\b{ticker}\b', text, re.IGNORECASE):
            companies.append({
                "ticker": ticker,
                "name": info["name"],
                "sector": info["sector"]
            })
            sectors.add(info["sector"])
    
    # Search for company names
    for company, ticker in COMPANY_NAMES.items():
        if company.lower() in text.lower() and ticker not in [c["ticker"] for c in companies]:
            if ticker in STOCK_TICKERS:
                info = STOCK_TICKERS[ticker]
                companies.append({
                    "ticker": ticker,
                    "name": info["name"],
                    "sector": info["sector"]
                })
                sectors.add(info["sector"])
    
    return {
        "companies": companies,
        "sectors": list(sectors),
        "count": len(companies)
    }

def get_sector_from_text(text):
    """Identify sector from news text"""
    text_lower = text.lower()
    
    sectors = {
        "Technology": ["tech", "software", "hardware", "ai", "artificial intelligence", "semiconductor", "chip"],
        "Finance": ["bank", "financial", "investment", "fed", "interest rate", "dollar", "trading"],
        "Energy": ["oil", "gas", "opec", "energy", "renewable", "solar", "wind"],
        "Healthcare": ["pharma", "drug", "health", "medical", "hospital", "vaccine"],
        "Consumer": ["retail", "consumer", "shopping", "brand", "products"],
    }
    
    detected_sectors = []
    for sector, keywords in sectors.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_sectors.append(sector)
    
    return detected_sectors[0] if detected_sectors else "General"