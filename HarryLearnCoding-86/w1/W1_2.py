"""Week 1 Task 2: Word frequency analysis."""


def word_count(text: str) -> dict[str, int]:
    """Count frequency of each word in text, ignoring punctuation and casing.

    Args:
        text: Input text string.

    Returns:
        Mapping of words to their occurrence count.
    """
    for char in ".,!?;:":
        text = text.replace(char, "")

    words = text.lower().split()
    counts: dict[str, int] = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    """Return top k most frequent words sorted by count descending, then word ascending.

    Args:
        text: Input text string.
        k: Maximum number of top words to return.

    Returns:
        List of (word, count) tuples.
    """
    counts = word_count(text)
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]
