def word_count(text: str) -> dict[str,int]:
    count={}
    for word in text.lower().split():
        word=word.strip(".,!?;:")
        if word:
            count[word]=count.get(word,0)+1
    return count

def top_k(text: str, k: int) -> list[tuple[str, int]]:
    count = word_count(text)
    result = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return result[:k]