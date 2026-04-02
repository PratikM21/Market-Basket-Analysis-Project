def get_product_insights(product_name, rules_df):
    """
    Returns summary insights for a given antecedent product.
    """
    if not isinstance(product_name, str) or product_name.strip() == "":
        return None

    product_name_clean = product_name.strip().lower()
    filtered = rules_df[rules_df["antecedents_lower"] == product_name_clean].copy()

    if filtered.empty:
        return None

    best_row = filtered.sort_values(
        by=["confidence", "lift", "support"],
        ascending=False
    ).iloc[0]

    insights = {
        "product": best_row["antecedents"],
        "rule_count": len(filtered),
        "best_recommendation": best_row["consequents"],
        "best_confidence": float(best_row["confidence"]),
        "best_lift": float(best_row["lift"]),
        "avg_confidence": float(filtered["confidence"].mean()),
        "avg_lift": float(filtered["lift"].mean()),
        "avg_support": float(filtered["support"].mean()),
    }

    return insights