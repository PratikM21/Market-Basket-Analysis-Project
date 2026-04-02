# 🛒 Market Basket Analysis Recommendation System

## 🚀 Live Demo

🔗 **Try the app here:**
👉 [https://your-streamlit-app-link.streamlit.app](https://market-basket-analysis-project-ludgetodztkd7rdctw49xm.streamlit.app/)

---

## 📌 Overview

This project implements a complete **Market Basket Analysis system** using the Instacart dataset to uncover hidden product relationships and generate smart recommendations.

It uses **Association Rule Mining (FP-Growth)** to power both:

* 🛍️ Single product recommendations
* 🧺 Basket-based recommendations

All wrapped inside an interactive **Streamlit web application**.

---

## 🎯 Problem Statement

Retail businesses need to understand purchasing behavior to:

* 📈 Increase cross-selling
* 💰 Boost average order value
* 🧠 Understand customer buying patterns
* 🏪 Improve product placement

This project solves that using data-driven association rules.

---

## 📊 Dataset

📦 **Instacart Market Basket Analysis Dataset**

### Files Used:

* `order_products__prior.csv`
* `products.csv`

### 🔍 Data Summary:

* 🧾 100,000 sampled orders
* 🛒 Average basket size: ~10 items
* 📦 Initial products: ~35,000+
* ⚡ Filtered products (freq ≥ 100): **1,788**

---

## ⚙️ Methodology

### 🧹 Data Preparation

* Merged order & product datasets
* Grouped by `order_id` to create transactions
* Removed low-frequency items to reduce sparsity

---

### 🔢 Encoding

* Used **TransactionEncoder** for one-hot encoding

---

### 🤖 Model

* Algorithm: **FP-Growth**
* Minimum Support: **0.001**

---

### 📏 Rule Generation

* Generated association rules using **Lift**
* Applied filtering:

  * ✅ Confidence ≥ 0.10
  * ✅ Lift between 1.5 and 50

---

### 🧠 Final Output

* 🔥 **1026 high-quality 1 → 1 recommendation rules**

---

## ✨ Features

### 🔍 Smart Product Recommendation

* Get related products instantly
* Handles partial matches & suggestions

---

### 🧺 Basket-Based Recommendation

* Recommend products from multiple inputs
* Shows:

  * ✅ Matched items
  * ❌ Unmatched items

---

### 🎨 Interactive UI (Streamlit)

* 🔎 Searchable product picker
* 🧺 Multi-select basket builder
* ♻️ Clear basket flow
* 📊 Product insights panel
* ⭐ Highlighted top recommendation

---

## 🛠️ Tech Stack

* 🐍 Python
* 📊 Pandas, NumPy
* ⚡ MLXtend (FP-Growth)
* 🌐 Streamlit

---

## 📁 Project Structure

```
app/                → Streamlit app  
src/                → Core logic & modules  
data/processed/     → Final recommendation dataset  
notebooks/          → EDA & model development  
```

---

## ▶️ Run Locally

```bash
git clone <your-repo-url>
cd Market-Basket-Analysis
pip install -r requirements.txt
streamlit run app/app.py
```

---

## 📸 App Preview

*(Add screenshots here later)*

```md
![Home](assets/screenshots/home.png)
![Recommendations](assets/screenshots/recommendation.png)
```

---

## 🚧 Future Improvements

* 🧠 Category-aware recommendations
* ⚡ Real-time recommendation API (FastAPI)
* 📊 Advanced ranking system
* 🌍 Scalable large dataset processing

---

## 👨‍💻 Author

**Ohidur Rahman Pratik**

* 💼 Aspiring AI Engineer
* 📊 Data Science Enthusiast
* 🤖 Machine Learning & AI Projects

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
