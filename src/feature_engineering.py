import pandas as pd

def generate_wallet_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate grouped wallet-level behavioral features from raw transaction data.

    Args:
        df (pd.DataFrame): Cleaned transaction-level DataFrame.

    Returns:
        pd.DataFrame: Aggregated wallet-level features with userWallet as index.
    """
    # Group by wallet
    wallet_groups = df.groupby('userWallet')

    features = []

    for wallet, group in wallet_groups:
        wallet_data = {
            'userWallet': wallet,
            'n_txns': len(group),
            'n_deposit': (group['actionType'] == 'Deposit').sum(),
            'n_borrow': (group['actionType'] == 'Borrow').sum(),
            'n_repay': (group['actionType'] == 'Repay').sum(),
            'n_redeem': (group['actionType'] == 'RedeemUnderlying').sum(),
            'n_liquidation': (group['actionType'] == 'LiquidationCall').sum(),
            'total_deposit_amount': group.loc[group['actionType'] == 'Deposit', 'amount'].sum(),
            'total_borrow_amount': group.loc[group['actionType'] == 'Borrow', 'amount'].sum(),
            'total_repay_amount': group.loc[group['actionType'] == 'Repay', 'amount'].sum(),
            'avg_txn_amount': group['amount'].mean(),
            'active_days': group['timestamp'].dt.date.nunique(),
            'asset_diversity': group['assetSymbol'].nunique()
        }
        features.append(wallet_data)

    # Create DataFrame from list of wallet dicts
    wallet_features = pd.DataFrame(features)
    wallet_features.set_index('userWallet', inplace=True)

    return wallet_features
