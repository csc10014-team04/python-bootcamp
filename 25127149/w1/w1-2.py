def word_count(text: str) -> dict[str, int]:
    text = text.lower()

    for p in (".,!?;:"):
        text = text.replace(p, "")

    words = text.split()
    result = {}

    for word in words:
        result[word] = result.get(word, 0) + 1

    return result

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    counts = word_count(text)
    items = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return items[:k]
