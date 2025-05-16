import pandas as pd

# Load enriched dataset
df = pd.read_csv("uniswap_swaps_20k_enriched.csv")

# Create swap usd value
df['SWAP_USD'] = df[['AMOUNT0_USD', 'AMOUNT1_USD']].max(axis=1)

# Create hour of day
df['HOUR_OF_DAY'] = pd.to_datetime(df['BLOCK_TIMESTAMP']).dt.hour

# Flag if slippage is high (example threshold 5%)
df['IS_HIGH_SLIPPAGE'] = df['SLIPPAGE_RATIO'] > 0.05  # Adjust threshold later if needed

# OPTIONAL (future): if sender == recipient
df['IS_SAME_SENDER_RECIPIENT'] = df['SENDER'].str.lower() == df['RECIPIENT'].str.lower()

# Save intermediate dataset
df.to_csv("uniswap_swaps_with_features.csv", index=False)