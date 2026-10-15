def word_count(text: str) -> dict[str, int]:
    
    punctuation = ".,!?;:"
    for mark in punctuation:
        text = text.replace(mark, " ")

    words = text.lower().split()
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


def top_k(text: str, k: int) -> list[tuple[str, int]]:
    
    counts = word_count(text)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:max(0, k)]
