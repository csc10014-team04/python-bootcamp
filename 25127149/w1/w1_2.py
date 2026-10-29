"""Count words in text and return the most frequent words."""


def word_count(text: str) -> dict[str, int]:
    """Return a mapping from normalized words to their occurrence counts."""
    normalized_text = text.lower()
    for punctuation in ".,!?;:":
        normalized_text = normalized_text.replace(punctuation, "")

    counts: dict[str, int] = {}
    for word in normalized_text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return at most k words ordered by descending count, then alphabetically."""
    if k <= 0:
        return []
    counts = word_count(text)
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return items[:k]
