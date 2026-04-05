import re
from app.constants import DOMAIN_KEYWORDS


def extract_keywords(text: str, role: str):
    text = text.lower()
    keywords = set()

    domain_terms = DOMAIN_KEYWORDS.get(role, [])

    # phrase matching
    for term in domain_terms:
        if term in text:
            keywords.add(term)

    # clean text
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = text.split()

    # add individual words
    for w in words:
        if len(w) > 3:
            keywords.add(w)

    return keywords