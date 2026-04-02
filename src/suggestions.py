import re
from difflib import get_close_matches


def normalize_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_product_suggestions(product_name, product_list, n=10):
    """
    Suggestion priority:
    1. exact normalized match
    2. substring match
    3. token overlap match
    4. fuzzy match with stricter cutoff
    """
    if not product_name or not isinstance(product_name, str):
        return []

    query = normalize_text(product_name)
    if not query:
        return []

    normalized_products = [(p, normalize_text(p)) for p in product_list]

    exact_matches = [orig for orig, norm in normalized_products if norm == query]
    if exact_matches:
        return exact_matches[:n]

    substring_matches = [orig for orig, norm in normalized_products if query in norm]

    query_tokens = set(query.split())
    token_matches = []

    for orig, norm in normalized_products:
        product_tokens = set(norm.split())
        if query_tokens and (query_tokens & product_tokens):
            token_matches.append(orig)

    normalized_only = [norm for _, norm in normalized_products]
    fuzzy_norm_matches = get_close_matches(query, normalized_only, n=n, cutoff=0.7)

    fuzzy_matches = []
    for orig, norm in normalized_products:
        if norm in fuzzy_norm_matches:
            fuzzy_matches.append(orig)

    final_matches = []
    for item in substring_matches + token_matches + fuzzy_matches:
        if item not in final_matches:
            final_matches.append(item)

    return final_matches[:n]