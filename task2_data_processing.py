import pandas as pd
import glob
import os

# 1 — Load the JSON File
json_files = glob.glob("data/trends_*.json")

if not json_files:
    raise FileNotFoundError("trends JSON files not found in data/. Make sure Task 1 has been run.")

json_path = json_files[0] #use the first match

print(f"processing the CSV file : {json_path}")
df= pd.read_json(json_path)

print(f"Loaded {len(df)} stories from {json_path}")
print()

#2 - Clean the Data

print(f"Rows before processing the cleaning process : {len(df)}")
# Remove duplicate post_ids
df = df.drop_duplicates(subset="post_id")
print(f"Rows after removing duplicates: {len(df)}")

#drop rows missing values for post_id, title, or score
df=df.dropna(subset=["post_id","title","score"])
print(f"Rows after removing missing values: {len(df)}")

# Ensure correct data types
df["score"] = pd.to_numeric(df["score"],errors="coerce").fillna(0).astype(int)
df["num_comments"] = pd.to_numeric(df["num_comments"],errors="coerce").fillna(0).astype(int)

#remove stories where score is less than 5
df = df[df["score"] >= 5]
print(f"Rows after removing the rows with score less than 5: {len(df)}")

#stripping the white speace from title
df["title"] = df["title"].str.strip()

#3 - Save as CSV
os.makedirs("data", exist_ok=True)
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
print()

#Summary - stories per category
print("Stories per categoty:")
category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<16}{count}")