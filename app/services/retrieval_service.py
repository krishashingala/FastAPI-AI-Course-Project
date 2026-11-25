import re


def retrieve_excerpt(text: str, question: str, max_chars: int = 1200) -> str:
    """Very small keyword-based retrieval demo; replace with embeddings/vector search for real RAG."""
    if not text.strip():
        return ""
    words = {w.lower() for w in re.findall(r"[A-Za-z0-9_+-]+", question) if len(w) > 2}
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|(?<=[.!?])\s+", text) if p.strip()]
    scored = []
    for paragraph in paragraphs:
        tokens = {w.lower() for w in re.findall(r"[A-Za-z0-9_+-]+", paragraph)}
        score = len(words & tokens)
        if score:
            scored.append((score, paragraph))
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        return text[:max_chars]
    return "\n".join(p for _, p in scored[:5])[:max_chars]
