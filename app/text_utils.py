import re
from collections import Counter
from difflib import SequenceMatcher


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "for", "from",
    "how", "i", "in", "is", "it", "me", "my", "of", "on", "or", "the",
    "to", "what", "when", "where", "why", "with", "would", "you", "your",
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./ -]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> list[str]:
    return [word for word in normalize(text).split() if word not in STOPWORDS]


def char_ngrams(text: str, size: int = 4) -> Counter[str]:
    compact = normalize(text).replace(" ", "")
    if len(compact) <= size:
        return Counter([compact]) if compact else Counter()
    return Counter(compact[index:index + size] for index in range(len(compact) - size + 1))


def token_score(left: str, right: str) -> float:
    left_counts = Counter(tokens(left))
    right_counts = Counter(tokens(right))
    if not left_counts or not right_counts:
        return 0.0

    overlap = sum((left_counts & right_counts).values())
    precision = overlap / sum(left_counts.values())
    recall = overlap / sum(right_counts.values())
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def ngram_score(left: str, right: str) -> float:
    left_counts = char_ngrams(left)
    right_counts = char_ngrams(right)
    if not left_counts or not right_counts:
        return 0.0
    overlap = sum((left_counts & right_counts).values())
    return overlap / max(sum(left_counts.values()), sum(right_counts.values()))


def similarity(left: str, right: str) -> float:
    lexical = token_score(left, right)
    ngrams = ngram_score(left, right)
    sequence = SequenceMatcher(None, normalize(left), normalize(right)).ratio()
    return round((lexical * 0.62) + (ngrams * 0.25) + (sequence * 0.13), 4)
