import pandas as pd

def preprocess_transactions(file_path: str) -> pd.DataFrame:
    """
    Load and preprocess raw Aave V2 DeFi transaction data.
    
    Args:
        file_path (str): Path to the JSON file containing raw transaction data.

    Returns:
        pd.DataFrame: Cleaned and flattened transaction DataFrame.
    """
    # Load JSON file
    df = pd.read_json(file_path)

    # Flatten nested fields
    df = pd.json_normalize(df.to_dict(orient='records'))

    # Print summary stats
    print(f"✅ Total records loaded: {len(df)}")
    print("🧾 Columns:", df.columns.tolist())
    print("👛 Unique wallets:", df['userWallet'].nunique())

    # Convert UNIX timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    # Normalize transaction amount (assuming 1e18 scale by default)
    df['amount'] = pd.to_numeric(df['actionData.amount'], errors='coerce') / 1e18

    # Rename key nested fields for easier access
    df.rename(columns={
        'actionData.type': 'actionType',
        'actionData.assetPriceUSD': 'assetPriceUSD',
        'actionData.assetSymbol': 'assetSymbol'
    }, inplace=True)

    # Convert assetPriceUSD to float
    df['assetPriceUSD'] = pd.to_numeric(df['assetPriceUSD'], errors='coerce')

    # Select key columns for modeling
    cleaned_df = df[['userWallet', 'timestamp', 'action', 'actionType', 'amount', 'assetSymbol', 'assetPriceUSD']].copy()

    return cleaned_df
