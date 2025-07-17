# 💳 DeFi Wallet Credit Scoring using Aave V2 Transaction Data

This project builds a **rule-based machine learning model** to assign a **credit score (0–1000)** to Ethereum wallets based on their historical behavior on the **Aave V2 protocol**. The scoring is based entirely on **DeFi transaction actions** like deposits, borrows, repayments, and liquidations, with the goal of identifying **responsible vs risky wallets**.

---

## 📌 Objective

Given a sample of 100K raw transaction records from Aave V2 protocol:
- 🎯 Score each wallet based on its historical behavior
- 📊 Credit scores range from **0 (risky/exploitative)** to **1000 (highly reliable)**
- 🧠 Build a **transparent, rule-based model** for interpretability
- 📁 Deliver a one-step script + feature analysis + documentation

---

## 📂 Project Structure

├── preprocessing.py # Flatten + clean raw JSON data
├── feature_engineering.py # Wallet-level aggregated features
├── score_wallets.py # Rule-based scoring logic (0–1000)
├── run_scoring.py # One-step script for input JSON → scored output
├── data/
│ └── user_transactions.json # Input JSON file (87MB sample)
├── outputs/
│ └── wallet_scores.csv # Final scored output
├── README.md # Project overview and instructions
└── analysis.md # Score distribution + wallet behavior insights


---

## ⚙️ How to Run

### 🔹 Step 1: Install dependencies

```bash
pip install -r requirements.txt

🔹 Step 2: Run one-step scoring script
python run_scoring.py --input data/user_transactions.json --output outputs/wallet_scores.csv

This will:

Flatten + clean the input JSON

Generate features for each wallet

Compute credit score (0–1000)

Save results in outputs/

