import os
import sys
import streamlit as st

# Allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import (
    APP_TITLE,
    APP_SUBTITLE,
    DEFAULT_TOP_N,
    MIN_TOP_N,
    MAX_TOP_N,
    DATA_PATH,
)
from src.data_loader import load_data, get_all_products
from src.suggestions import get_product_suggestions
from src.recommender import recommend_products, recommend_from_basket
from src.formatter import format_results_table
from src.insights import get_product_insights
from src.basket_utils import analyze_basket_items, clean_basket_input


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Market Basket Recommender",
    page_icon="🛒",
    layout="wide"
)


# -----------------------------
# Load Data
# -----------------------------
df_rules = load_data(DATA_PATH)
all_products = get_all_products(df_rules)


# -----------------------------
# Session State Initialization
# -----------------------------
def init_session_state():
    defaults = {
        "single_input": "",
        "single_suggestions": [],
        "selected_suggestion": "",
        "single_results": None,
        "single_message": "",
        "basket_results": None,
        "basket_message": "",
        "basket_text_input": "",
        "basket_multiselect_items": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# -----------------------------
# Styling
# -----------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 18px;
    }
    .sample-label {
        font-size: 14px;
        color: #666666;
        margin-bottom: 6px;
    }
    .small-note {
        font-size: 13px;
        color: #777777;
        margin-top: 6px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(f'<div class="main-title">{APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Settings")
top_n = st.sidebar.slider(
    "Number of recommendations",
    min_value=MIN_TOP_N,
    max_value=MAX_TOP_N,
    value=DEFAULT_TOP_N
)
st.sidebar.markdown("---")
st.sidebar.caption("Adjust how many recommendations to display.")


# -----------------------------
# Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Association Rules", f"{len(df_rules):,}")

with col2:
    st.metric("Unique Products", f"{len(all_products):,}")

with col3:
    st.metric("Top-N Setting", top_n)


# -----------------------------
# About Section
# -----------------------------
with st.expander("About this app"):
    st.write("""
    This recommendation system is built using association rules mined from the Instacart dataset.

    It supports:
    - Single-product recommendations
    - Basket-based recommendations
    - Smart product suggestions
    - Searchable product selection
    - Product insights
    """)


# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Single Product", "Basket Based"])


# =============================
# SINGLE PRODUCT TAB
# =============================
with tab1:
    st.subheader("Single Product Recommendation")

    st.markdown('<div class="sample-label">Try a sample product</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)

    with s1:
        if st.button("Banana", use_container_width=True):
            st.session_state.single_input = "Banana"
            st.session_state.single_results = None
            st.session_state.single_suggestions = []
            st.session_state.selected_suggestion = ""
            st.rerun()

    with s2:
        if st.button("Organic Whole Milk", use_container_width=True):
            st.session_state.single_input = "Organic Whole Milk"
            st.session_state.single_results = None
            st.session_state.single_suggestions = []
            st.session_state.selected_suggestion = ""
            st.rerun()

    with s3:
        if st.button("Strawberries", use_container_width=True):
            st.session_state.single_input = "Strawberries"
            st.session_state.single_results = None
            st.session_state.single_suggestions = []
            st.session_state.selected_suggestion = ""
            st.rerun()

    st.markdown("### Or pick from catalog")

    selected_catalog_product = st.selectbox(
        "Search product",
        options=[""] + all_products,
        index=0
    )

    if st.button("Use Selected Product", use_container_width=True):
        if selected_catalog_product:
            st.session_state.single_input = selected_catalog_product
            st.session_state.single_results = None
            st.session_state.single_suggestions = []
            st.session_state.selected_suggestion = ""
            st.rerun()
        else:
            st.warning("Select a product first.")

    product_input = st.text_input(
        "Enter a product name",
        value=st.session_state.single_input
    )

    colA, colB = st.columns(2)

    with colA:
        search_clicked = st.button("Get Recommendations", use_container_width=True)

    with colB:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state.single_input = ""
        st.session_state.single_results = None
        st.session_state.single_suggestions = []
        st.session_state.selected_suggestion = ""
        st.rerun()

    if search_clicked:
        st.session_state.single_input = product_input.strip()
        st.session_state.single_results = None
        st.session_state.single_suggestions = []
        st.session_state.selected_suggestion = ""

        if product_input.strip() == "":
            st.warning("Enter a product name")
        else:
            results, error = recommend_products(product_input, df_rules, top_n=top_n)

            if error:
                st.error(error)
                st.session_state.single_suggestions = get_product_suggestions(
                    product_input, all_products
                )
            else:
                st.session_state.single_results = results

    if st.session_state.single_results is not None:
        top_row = st.session_state.single_results.iloc[0]

        insights = get_product_insights(top_row["antecedents"], df_rules)

        if insights:
            st.markdown("### Product Insights")

            i1, i2, i3, i4 = st.columns(4)

            with i1:
                st.metric("Rules", insights["rule_count"])

            with i2:
                st.metric("Best Match", insights["best_recommendation"])

            with i3:
                st.metric("Confidence", f"{insights['best_confidence']:.2f}")

            with i4:
                st.metric("Lift", f"{insights['best_lift']:.2f}")

            st.caption(
                f"Avg confidence: {insights['avg_confidence']:.2f} | "
                f"Avg lift: {insights['avg_lift']:.2f}"
            )

        st.markdown("### Top Recommendation")
        st.info(
            f"Customers who buy **{top_row['antecedents']}** also buy "
            f"**{top_row['consequents']}** "
            f"(confidence {top_row['confidence']:.2f}, lift {top_row['lift']:.2f})"
        )

        st.dataframe(format_results_table(st.session_state.single_results), use_container_width=True)

    if st.session_state.single_suggestions:
        st.info("Did you mean:")

        selected = st.selectbox(
            "Suggestions",
            options=[""] + st.session_state.single_suggestions
        )

        if st.button("Use Suggestion"):
            if selected:
                st.session_state.single_input = selected
                st.session_state.single_suggestions = []
                st.rerun()


# =============================
# BASKET TAB
# =============================
with tab2:
    st.subheader("Basket Based Recommendation")

    basket_mode = st.radio(
        "Choose basket input method",
        ["Type Basket Items", "Select from Product Catalog"],
        horizontal=True
    )

    basket_items = []

    if basket_mode == "Type Basket Items":
        basket_input = st.text_area(
            "Enter basket items (comma-separated)",
            value=st.session_state.basket_text_input,
            placeholder="Banana, Milk, Bread"
        )

        st.markdown(
            '<div class="small-note">Duplicate items and empty values will be removed automatically.</div>',
            unsafe_allow_html=True
        )

        cleaned_basket_items = clean_basket_input(basket_input)
        st.session_state.basket_text_input = basket_input
        basket_items = cleaned_basket_items

    else:
        selected_basket_products = st.multiselect(
            "Search and select basket items",
            options=all_products,
            default=st.session_state.basket_multiselect_items
        )

        st.session_state.basket_multiselect_items = selected_basket_products
        basket_items = selected_basket_products

    if basket_items:
        matched_items, unmatched_items = analyze_basket_items(basket_items, all_products)

        st.markdown("### Basket Summary")

        b1, b2, b3 = st.columns(3)
        with b1:
            st.metric("Input Items", len(basket_items))
        with b2:
            st.metric("Matched Items", len(matched_items))
        with b3:
            st.metric("Unmatched Items", len(unmatched_items))

        if matched_items:
            st.markdown("**Matched Items:**")
            st.write(", ".join(matched_items))

        if unmatched_items:
            st.markdown("**Unmatched Items:**")
            st.write(", ".join(unmatched_items))

            st.markdown("### Suggested Fixes")
            for item in unmatched_items:
                suggestions = get_product_suggestions(item, all_products, n=5)
                if suggestions:
                    st.write(f"**{item}** → {', '.join(suggestions)}")
                else:
                    st.write(f"**{item}** → No close match found")

    colC, colD = st.columns(2)

    with colC:
        recommend_basket_clicked = st.button("Recommend from Basket", use_container_width=True)

    with colD:
        clear_basket_clicked = st.button("Clear Basket", use_container_width=True)

    if clear_basket_clicked:
        st.session_state.basket_results = None
        st.session_state.basket_message = ""
        st.session_state.basket_text_input = ""
        st.session_state.basket_multiselect_items = []
        st.rerun()

    if recommend_basket_clicked:
        st.session_state.basket_results = None
        st.session_state.basket_message = ""

        if not basket_items:
            st.warning("Please enter or select at least one basket item.")
        else:
            matched_items, unmatched_items = analyze_basket_items(basket_items, all_products)

            if not matched_items:
                st.error("None of the basket items matched the product catalog.")
            else:
                results, error = recommend_from_basket(matched_items, df_rules, top_n=top_n)

                if error:
                    st.error(error)
                else:
                    st.session_state.basket_results = results

                    if unmatched_items:
                        st.session_state.basket_message = (
                            f"Recommendations generated using {len(matched_items)} matched item(s). "
                            f"{len(unmatched_items)} unmatched item(s) were ignored."
                        )
                    else:
                        st.session_state.basket_message = "Basket recommendations generated successfully."

    if st.session_state.basket_message:
        st.success(st.session_state.basket_message)

    if st.session_state.basket_results is not None:
        top = st.session_state.basket_results.iloc[0]

        st.markdown("### Best Recommendation")
        st.info(
            f"Recommended: **{top['consequents']}** "
            f"(confidence {top['confidence']:.2f}, lift {top['lift']:.2f})"
        )

        st.markdown("### Basket Recommendation Table")
        st.dataframe(format_results_table(st.session_state.basket_results), use_container_width=True)


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with Streamlit | Market Basket Analysis Project")