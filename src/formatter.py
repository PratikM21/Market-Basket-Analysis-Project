def format_results_table(results_df):
    display_results = results_df.copy()

    for col in ["support", "confidence", "lift"]:
        if col in display_results.columns:
            display_results[col] = display_results[col].round(4)

    return display_results