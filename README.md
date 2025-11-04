# 🛡️ AI-Powered Mine Safety Intelligence System  
Real-time mining accident monitoring, RAG-based incident analysis, and AI safety assistant

## 🚀 Features
✅ Mine accident ingestion from DGMS, Twitter, Google News  
✅ OCR + LLM extraction from DGMS SANKET PDF  
✅ FAISS + RAG search on accident history  
✅ Streamlit mining safety chat assistant  
✅ Real-time alerting for fatality spikes  
✅ Daily automated incident updates  

## 🧠 System Architecture
PDF → OCR → LLM → CSV → FAISS RAG → Chatbot → Alerts
Twitter/DGMS/News → Live ingestion → CSV → RAG update → Alerts


## 🏗️ Tech Stack
| Layer | Tool |
|---|---|
Language Model | GPT-4 / GPT-5 ready  
Vector DB | FAISS  
Web UI | Streamlit  
OCR | Tesseract  
Scraping | Python requests / snscrape  

## 📦 Install

```bash
git clone https://github.com/<your-username>/mine-safety-intelligence-system
cd mine-safety-intelligence-system
python -m venv .venv
.venv/Scripts/activate  # (Windows)
pip install -r requirements.txt
```

Add OpenAI key:

cp .env.example .env

🏃 Run

1️⃣ Fetch live data
python scripts/fetch_live.py

2️⃣ Send alerts
python -m src.alerts.notify

3️⃣ Update RAG index
python -m src.rag.update_index

4️⃣ Run chatbot
streamlit run app/chat_web.py

🗄️ Data Sources

DGMS India mining accident alerts

Open news feeds

Twitter scrape

DGMS SANKET accident statistics (LLM-processed)

🎯 Demo Use Cases

Mine operators early warning tool

DGMS inspector support

Mine safety training AI

Risk analytics dashboard




