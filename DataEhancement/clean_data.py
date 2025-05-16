import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# load data
df = pd.read_csv("uniswap_swaps_with_features.csv")

# drop rows missing target values
df = df.dropna(subset=['GAS_PRICE_GWEI', 'SWAP_USD'])

# remove swaps with USD value too small 
df = df[df['SWAP_USD'] > 10]  

# select features
features = ['GAS_PRICE_GWEI', 'SWAP_USD', 'SLIPPAGE_RATIO', 'HOUR_OF_DAY', 'IS_HIGH_SLIPPAGE', 'IS_SAME_SENDER_RECIPIENT']
X = df[features]

# scaling features
print("scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✅ scaling done.")

# train isolation forest
print("training isolation forest model...")
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(X_scaled)
print("✅ model training complete.")

# predict anomalies
print("predicting anomalies...")
df['anomaly_score'] = model.decision_function(X_scaled)
df['is_anomaly'] = model.predict(X_scaled)

# convert predictions: -1 = anomaly, 1 = normal
df['is_anomaly'] = df['is_anomaly'].map({1: 0, -1: 1})
print(f"✅ anomalies predicted. total anomalies detected: {df['is_anomaly'].sum()}")

# view first 10 suspicious swaps
suspicious = df[df['is_anomaly'] == 1]
print(suspicious[['TX_HASH', 'GAS_PRICE_GWEI', 'SWAP_USD', 'SLIPPAGE_RATIO']].head(10))

# save full dataset
df.to_csv("uniswap_swaps_anomaly_detection.csv", index=False)

# save only suspicious swaps
df[df['is_anomaly'] == 1].to_csv("uniswap_swaps_suspicious_only.csv", index=False)

print("✅ all files saved. done!")