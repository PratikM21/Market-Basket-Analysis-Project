APP_TITLE = "Market Basket Recommendation System"
APP_SUBTITLE = "Product recommendations using association rules from the Instacart dataset"

DEFAULT_TOP_N = 5
MIN_TOP_N = 3
MAX_TOP_N = 15

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "recommendation_base.csv"