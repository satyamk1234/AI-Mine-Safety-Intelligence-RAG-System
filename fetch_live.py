import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import pandas as pd
from datetime import datetime
from src.ingest.fetch_dgms import fetch_dgms_alerts, to_incident as dgms_to_incident
from src.ingest.fetch_twitter import fetch_tweets
from src.ingest.fetch_news import fetch_news

RAW_DIR = "data/live_raw"
LIVE_FILE = "data/live_incidents.csv"

def ensure_dirs():
    for p in ["dgms", "twitter", "news"]:
        os.makedirs(os.path.join(RAW_DIR, p), exist_ok=True)

def append_jsonl(path, items):
    with open(path, "a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def load_live():
    if os.path.exists(LIVE_FILE):
        return pd.read_csv(LIVE_FILE)
    return pd.DataFrame(columns=["Date","State","Mine","MineType","AccidentType","Injuries","Fatalities","Description","Source","Url","Id"])

def save_live(df):
    df.to_csv(LIVE_FILE, index=False)

def dedupe(df):
    if "Id" in df.columns:
        return df.drop_duplicates(subset=["Id"])
    return df.drop_duplicates(subset=["Description","Url"])

def main():
    print("Fetching live mining incidents...")

    ensure_dirs()

    print("Fetching DGMS alerts...")
    dg_items = fetch_dgms_alerts()
    dg_incidents = [dgms_to_incident(x) for x in dg_items]
    append_jsonl(os.path.join(RAW_DIR, "dgms", "items.jsonl"), dg_items)

    print("Fetching Twitter incidents...")
    tw_incidents = fetch_tweets()

    print("Fetching Google News...")
    news_incidents = fetch_news()

    new_incidents = dg_incidents + tw_incidents + news_incidents
    new_df = pd.DataFrame(new_incidents)

    live_df = load_live()
    merged = dedupe(pd.concat([live_df, new_df], ignore_index=True))
    save_live(merged)

    print(f"New incidents added: {len(new_incidents)}")
    print(f"Total live incidents: {len(merged)}")
    print("Live incident feed updated!")

if __name__ == "__main__":
    main()
