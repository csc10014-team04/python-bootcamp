def word_count(text: str) -> dict[str, int]:
    for char in ".,!?;:":
        text = text.replace(char, "") # remove specific punctuation
    words = text.lower().split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1 # count word occurrences
    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0])) # sort by count then alphabetical
    return sorted_items[:k]