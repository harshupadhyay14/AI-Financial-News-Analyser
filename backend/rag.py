import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embeddings import get_model

# -----------------------------
# 1. SEGMENTATION (LIGHTWEIGHT)
# -----------------------------
def segment_text(text):
    """
    For financial news, keep it simple.
    Split by sentences instead of word chunks.
    """
    sentences = text.split(". ")
    return [s.strip() for s in sentences if len(s.strip()) > 20]


# -----------------------------
# 2. RETRIEVAL (FIXED)
# -----------------------------
def retrieve(query, docs, embeddings, top_k=3):
    model = get_model()

    # encode query
    query_embedding = model.encode([query])

    # similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # get top matches
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [docs[i] for i in top_indices]


# -----------------------------
# 3. BUILD CONTEXT
# -----------------------------
def build_context(news_articles):
    """
    Convert your news_cache into usable text
    """
    docs = []

    for article in news_articles:
        text = article.get("title", "")

        # optional: include description if available
        if "description" in article:
            text += ". " + article["description"]

        # segment it
        segments = segment_text(text)
        docs.extend(segments)

    return docs


# -----------------------------
# 4. MAIN RAG FUNCTION
# -----------------------------
def retrieve_relevant_news(query, news_articles):
    docs = build_context(news_articles)

    if not docs:
        return ["No relevant news found"]

    model = get_model()
    embeddings = model.encode(docs)

    top_docs = retrieve(query, docs, embeddings)

    return top_docs