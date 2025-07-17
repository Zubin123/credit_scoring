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

```
.
├── preprocessing.py             # Flatten + clean raw JSON data
├── feature_engineering.py       # Wallet-level aggregated features
├── score_wallets.py             # Rule-based scoring logic (0–1000)
├── run_scoring.py               # One-step script for input JSON → scored output
├── data/
│   └── user_transactions.json   # Input JSON file (87MB sample)
├── outputs/
│   └── wallet_scores.csv        # Final scored output
├── README.md                    # Project overview and instructions
└── analysis.md                  # Score distribution + wallet behavior insights
```

---

## ⚙️ How to Run

### 🔹 Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### 🔹 Step 2: Run the scoring script

```bash
python run_scoring.py --input data/user_transactions.json --output outputs/wallet_scores.csv
```

This will:
- Flatten and clean the input JSON
- Generate features for each wallet
- Compute credit score (0–1000)
- Save results in `outputs/`

---

## 🏗️ Methodology

### ✅ Preprocessing

- Loaded raw JSON and normalized nested fields
- Converted timestamps and numeric fields (e.g. `amount`, `assetPriceUSD`)
- Removed unusable or null-heavy columns

### ✅ Feature Engineering (per wallet)

- Transaction counts: deposits, borrows, repays, redemptions
- Volume-based metrics: total borrowed, repaid, deposited
- Behavioral metrics:
  - `avg_txn_amount`
  - `active_days`
  - `asset_diversity` (distinct tokens used)
  - `borrow_to_repay_ratio` (repayment effectiveness)

### ✅ Rule-Based Scoring Logic

We used a **weighted formula** on key normalized features:

```python
score_raw = (
    1.5 * n_repay +
    2.0 * log1p(borrow_to_repay_ratio) +
    1.0 * active_days +
    0.5 * log1p(total_deposit_amount) -
    2.0 * n_liquidation
)
```

Then we scaled the `score_raw` using `MinMaxScaler` to get a score between 0 and 1000:

- Higher scores = safer DeFi behavior
- Penalized wallets with liquidations and no repayments

---

## 📊 Key Observations (See `analysis.md`)

- Majority of wallets fall in the **100–400 score range**
- Very few wallets scored above **900**, indicating rare responsible behavior
- High scorers typically:
  - Repay more than they borrow
  - Have diverse token usage
  - Avoid liquidation
- Risky wallets:
  - Never repay
  - Frequently liquidated
  - Little to no long-term engagement

---

## ✅ Deliverables

- `run_scoring.py`: One-step script (input JSON → wallet_scores.csv)
- `wallet_scores.csv`: Contains wallet address, features, score, score_range
- `analysis.md`: Visualizations + behavioral insights
- `README.md`: Documentation

---

## 🧠 Potential Improvements

- Replace rules with a supervised ML model (e.g., XGBoost)
- Add real-time Aave API ingestion
- Integrate credit scoring with lending dApps or identity layers
- Add visualization dashboard using Streamlit or Dash

---

## 📧 Credits

Developed by: **Mohammed Zubin Essudeen**  
For internship task using **Aave V2 Polygon Dataset**

---

## 📎 References

- [Aave V2 Protocol Docs](https://docs.aave.com/)
- [Polygon Blockchain Explorer](https://polygonscan.com/)
