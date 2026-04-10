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

scores = df["score"].to_numpy()

print("---- Stats using Numpy Module ---")

print(f"Mean : {np.mean(scores):,.2f}")
print(f"Median : {np.median(scores):,.2f}")
print(f"Standard Deviation: {np.std(scores):,.2f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")
print()

categories, counts = np.unique(df["category"].to_numpy(), return_counts=True)
top_idx      = np.argmax(counts)
top_category = categories[top_idx]
top_count    = counts[top_idx]
print(f"Most stories in: {top_category} ({top_count} stories)")
print()

comments     = df["num_comments"].to_numpy()
top_idx      = np.argmax(comments)
most_commented = df.iloc[top_idx]
print(f'Most commented story: "{most_commented["title"]}"  — {most_commented["num_comments"]:,} comments')
print()

#Adding New Columns 
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

#Save the result
df.to_csv("data/trends_analysed.csv", index=False)
print("Saved to data/trends_analysed.csv")