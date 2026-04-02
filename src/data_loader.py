import ast
import pandas as pd
import streamlit as st


def clean_item(x):
    if pd.isna(x):
        return ""

    x = str(x).strip()

    try:
        parsed = ast.literal_eval(x)
        if isinstance(parsed, (list, set, tuple)):
            parsed = list(parsed)
            if len(parsed) > 0:
                return str(parsed[0]).strip()
    except Exception:
        pass

    return x.strip("{}[]()'\" ")


@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)

    if "antecedents" not in df.columns or "consequents" not in df.columns:
        st.error(f"Expected columns not found. Columns are: {df.columns.tolist()}")
        st.stop()

    df["antecedents"] = df["antecedents"].apply(clean_item)
    df["consequents"] = df["consequents"].apply(clean_item)

    df["antecedents_lower"] = df["antecedents"].astype(str).str.lower().str.strip()
    df["consequents_lower"] = df["consequents"].astype(str).str.lower().str.strip()

    return df


def get_all_products(df_rules):
    return sorted(set(df_rules["antecedents"].dropna().tolist()))