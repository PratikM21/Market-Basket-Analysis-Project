def recommend_products(product_name, rules_df, top_n=5):
    """
    Recommend products for a single product input.
    """
    if not isinstance(product_name, str) or product_name.strip() == "":
        return None, "Please enter a valid product name."

    product_name_clean = product_name.strip().lower()
    filtered = rules_df[rules_df["antecedents_lower"] == product_name_clean].copy()

    if filtered.empty:
        return None, "Product not found."

    filtered = filtered.sort_values(
        by=["confidence", "lift", "support"],
        ascending=False
    )

    result = (
        filtered[["antecedents", "consequents", "support", "confidence", "lift"]]
        .head(top_n)
        .reset_index(drop=True)
    )

    return result, None


def recommend_from_basket(basket_items, rules_df, top_n=5):
    """
    Recommend products from multiple basket items.
    Combines rules for all input items and removes already selected products.
    """
    if not basket_items or not isinstance(basket_items, list):
        return None, "Please enter at least one basket item."

    cleaned_basket = [
        item.strip().lower()
        for item in basket_items
        if isinstance(item, str) and item.strip() != ""
    ]

    if not cleaned_basket:
        return None, "Please enter valid basket items."

    filtered = rules_df[rules_df["antecedents_lower"].isin(cleaned_basket)].copy()

    if filtered.empty:
        return None, "No recommendations found for the selected basket."

    filtered = filtered[~filtered["consequents_lower"].isin(cleaned_basket)]

    if filtered.empty:
        return None, "No new recommendations found after excluding already selected basket items."

    grouped = (
        filtered.groupby("consequents", as_index=False)
        .agg({
            "support": "max",
            "confidence": "mean",
            "lift": "mean"
        })
        .sort_values(by=["confidence", "lift", "support"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return grouped, None