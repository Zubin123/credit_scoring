import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def calculate_rule_based_scores(wallet_features: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a rule-based credit score (0–1000) for each wallet using engineered features.

    Args:
        wallet_features (pd.DataFrame): DataFrame containing aggregated wallet features.

    Returns:
        pd.DataFrame: Original DataFrame with an added 'rule_score' column.
    """

    # Compute borrow-to-repay ratio with epsilon to avoid division by zero
    wallet_features['borrow_to_repay_ratio'] = (
        wallet_features['total_repay_amount'] / (wallet_features['total_borrow_amount'] + 1e-6)
    ).replace([np.inf, -np.inf], 0).fillna(0)

    # Create a copy to avoid mutation
    X = wallet_features.copy()

    # Log scale large fields and clip outliers
    X['total_deposit_amount'] = np.log1p(X['total_deposit_amount'])
    X['borrow_to_repay_ratio'] = np.clip(X['borrow_to_repay_ratio'], 0, 5)
    X['borrow_to_repay_ratio'] = np.log1p(X['borrow_to_repay_ratio'])

    # Select features for scoring
    features_for_scoring = [
        'n_repay', 'borrow_to_repay_ratio', 'active_days',
        'total_deposit_amount', 'n_liquidation'
    ]

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X[features_for_scoring])

    # Apply rule-based weighted formula
    rule_score_raw = (
        1.5 * X_scaled[:, 0] +   # n_repay
        2.0 * X_scaled[:, 1] +   # borrow_to_repay_ratio
        1.0 * X_scaled[:, 2] +   # active_days
        0.5 * X_scaled[:, 3] -   # total_deposit_amount (mild influence)
        2.0 * X_scaled[:, 4]     # n_liquidation (penalty)
    )

    # Rescale to 0–1000 and add to DataFrame
    wallet_features['rule_score'] = MinMaxScaler().fit_transform(rule_score_raw.reshape(-1, 1)) * 1000
    wallet_features['rule_score'] = wallet_features['rule_score'].round(2)

    return wallet_features
