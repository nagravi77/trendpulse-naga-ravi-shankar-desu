import pandas as pd
import numpy as np

# 1 — Load and Explore

df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")
print()
print("First 5 rows:")
print(df.head())
print()

avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"Average score   : {avg_score:,.2f}")
print(f"Average comments: {avg_comments:,.2f}")
print()

# 2 — Basic Analysis with NumPy