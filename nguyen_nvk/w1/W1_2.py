def word_count(text: str) -> dict[str, int]:
    for char in ".,!?;:":
        text = text.replace(char, "")
    
    words = text.lower().split()
    counts = {}
    
    for word in words:
        counts[word] = counts.get(word, 0) + 1
        
    return counts

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]