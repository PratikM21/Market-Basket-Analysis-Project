def analyze_basket_items(basket_items, all_products):
    """
    Splits basket items into matched and unmatched items using exact lowercase comparison.
    Returns:
        matched_original_names,
        unmatched_input_items
    """
    if not basket_items:
        return [], []

    product_lookup = {p.lower().strip(): p for p in all_products}

    matched = []
    unmatched = []

    for item in basket_items:
        cleaned = item.strip().lower()
        if cleaned in product_lookup:
            matched.append(product_lookup[cleaned])
        else:
            unmatched.append(item)

    return matched, unmatched


def clean_basket_input(basket_input):
    """
    Converts comma-separated text input into cleaned list of basket items.
    Removes empty values and duplicates while preserving order.
    """
    if not isinstance(basket_input, str) or basket_input.strip() == "":
        return []

    raw_items = [item.strip() for item in basket_input.split(",") if item.strip()]

    cleaned = []
    seen = set()

    for item in raw_items:
        key = item.lower().strip()
        if key not in seen:
            cleaned.append(item)
            seen.add(key)

    return cleaned