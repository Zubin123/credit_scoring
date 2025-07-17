import pandas as pd
from preprocessing import preprocess_transactions
from feature_engineering import generate_wallet_features
from score_wallets import calculate_rule_based_scores
import os

def main():
    input_path = "data/user-wallet-transactions.json"
    output_dir = "outputs"
    output_file = os.path.join(output_dir, "wallet_scores.csv")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print("🔄 Step 1: Preprocessing raw transactions...")
    tx_df = preprocess_transactions(input_path)
    print(f"✅ Loaded and flattened {len(tx_df)} transactions.")

    print("🔄 Step 2: Generating wallet-level features...")
    wallet_features = generate_wallet_features(tx_df)
    print(f"✅ Generated features for {len(wallet_features)} unique wallets.")

    print("🔄 Step 3: Scoring wallets (0–1000)...")
    scored_wallets = calculate_rule_based_scores(wallet_features)
    print("✅ Scoring complete.")

    print(f"💾 Saving results to: {output_file}")
    scored_wallets.to_csv(output_file, index=False)
    print("🎉 Done!")


if __name__ == "__main__":
    main()
