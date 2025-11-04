import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


STORE_DIR = "data/rag_store"

def build_docs(df):
    docs = []
    for _, r in df.iterrows():
        content = (
            f"Date: {r.get('Date','')}\n"
            f"State: {r.get('State','')}\n"
            f"Mine: {r.get('Mine','')}\n"
            f"MineType: {r.get('MineType','')}\n"
            f"AccidentType: {r.get('AccidentType','')}\n"
            f"Injuries: {r.get('Injuries','')}\n"
            f"Fatalities: {r.get('Fatalities','')}\n"
            f"Description: {r.get('Description','')}\n"
            f"Source: {r.get('Source','')}\n"
            f"Url: {r.get('Url','')}"
        )
        docs.append(Document(page_content=content, metadata={"id": r.get("Id",""), "source":"accident"}))
    return docs

def main():

    base = pd.read_csv("data/accidents.csv") if os.path.exists("data/accidents.csv") else pd.DataFrame()
    live = pd.read_csv("data/live_incidents.csv") if os.path.exists("data/live_incidents.csv") else pd.DataFrame()
    df = pd.concat([base, live], ignore_index=True)

    if df.empty:
        print("No accident data found. Make sure accidents.csv or live_incidents.csv exist.")
        return

    docs = build_docs(df)

    os.makedirs(STORE_DIR, exist_ok=True)

    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print(f"Generating embeddings for {len(docs)} docs...")

    store = FAISS.from_documents(docs, embed_model)
    store.save_local(STORE_DIR)

    print(f"FAISS database updated at: {STORE_DIR}")


if __name__ == "__main__":
    main()
