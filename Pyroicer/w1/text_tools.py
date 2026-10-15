import re
def word_count(text: str) -> dict[str, int]:
    cleaned=re.sub(r'[ .,!?;:]', '', text.lower())
    cleaned.split()
    counts = {}
    for i in cleaned:
        counts[i] = counts.get(i, 0) + 1
    return counts
def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words[:k]