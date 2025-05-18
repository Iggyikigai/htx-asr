import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from tqdm import tqdm

# Configuration
csv_path = r"C:\htx-asr\elastic-backend\cv-valid-dev.csv"
index_name = "cv-transcriptions"
API_KEY = "Uml1TDRaWUJJX1RSOF9jcWVMNU06YUw4b3YwZjNUcmlhOTlvdTY5eWNsdw=="

# Elasticsearch Connection with API Key 
es = Elasticsearch(
    "http://localhost:9200",
    headers={"Authorization": f"ApiKey {API_KEY}"}
)

# STEP 1: Load CSV 
print("\U0001F4C4 Loading CSV...")
df = pd.read_csv(csv_path)

# STEP 2: Basic Validations 
if "generated_text" not in df.columns:
    raise ValueError("\u274C 'generated_text' column not found in CSV. Please run cv-decode.py first.")

# STEP 3: Clean and Sanitize Data 
df["duration"] = pd.to_numeric(df["duration"], errors="coerce").fillna(0)
df["age"] = df.get("age", pd.Series(["unknown"] * len(df))).fillna("unknown")
df["gender"] = df.get("gender", pd.Series(["unknown"] * len(df))).fillna("unknown")
df["accent"] = df.get("accent", pd.Series(["unknown"] * len(df))).fillna("unknown")
df["generated_text"] = df["generated_text"].fillna("")

# STEP 4: Define Index Mapping 
mapping = {
    "mappings": {
        "properties": {
            "generated_text": {"type": "text"},
            "duration": {"type": "float"},
            "age": {"type": "keyword"},
            "gender": {"type": "keyword"},
            "accent": {"type": "keyword"}
        }
    }
}

# STEP 5: Create Index If Not Exists 
if not es.indices.exists(index=index_name):
    try:
        es.indices.create(index=index_name, body=mapping)
        print("\U0001F7E2 Index created.")
    except Exception as e:
        print(f"\u274C Failed to create index: {e}")
else:
    print("\u2139\ufe0f Index already exists.")

# STEP 6: Index Rows 
print("\U0001F4E4 Indexing data...")
for _, row in tqdm(df.iterrows(), total=len(df)):
    try:
        doc = {
            "generated_text": str(row["generated_text"]),
            "duration": float(row["duration"]),
            "age": str(row["age"]),
            "gender": str(row["gender"]),
            "accent": str(row["accent"])
        }
        es.index(index=index_name, document=doc)
    except Exception as e:
        print(f"\u274C Skipping row: {e}")

print("\u2705 Indexing complete.")
