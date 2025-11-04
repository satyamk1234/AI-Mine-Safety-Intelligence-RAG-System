import os, pandas as pd, streamlit as st
from src.rag.chat import answer_query
from src.reports.generator import generate_incident_report

st.set_page_config(page_title="Mine Safety Officer — Chat", layout="wide")

with st.sidebar:
    st.title("Mine Safety Officer")
    st.caption("RAG-powered assistant over DGMS incidents + live feeds")
    st.markdown("---")
    st.subheader("Filters for Reports")
    flt_state = st.text_input("State", "")
    flt_mine = st.text_input("Mine", "")
    flt_cause = st.text_input("Accident Type", "")
    flt_year = st.text_input("Year", "")
    st.markdown("---")
    st.write("**Data Sources**")
    st.write("• Historical (DGMS SANKET 2016–2022)")
    st.write("• Live (DGMS/Twitter/Google News @ 6h)")

st.title("💬 Digital Mine Safety Officer")
st.write("Ask about incidents, trends, and safety insights.")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("e.g., 'List methane-related accidents in 2021 underground coal mines in Jharkhand'")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    try:
        answer, sources = answer_query(prompt)
        st.session_state.messages.append({"role":"assistant","content":answer, "sources": sources})
    except Exception as e:
        st.session_state.messages.append({"role":"assistant","content":f"Error: {e}"})
        sources = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Sources (RAG matches)"):
                for s in m["sources"]:
                    st.write(s)

st.markdown("---")
st.subheader("Generate Incident Report (PDF)")
colA, colB = st.columns([3,1])
with colA:
    st.write("Build a report from filters and (optionally) your latest RAG matches.")
with colB:
    go = st.button("Generate PDF")

if go:
    path = "data/accidents.csv"
    df = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
    if os.path.exists("data/live_incidents.csv"):
        live = pd.read_csv("data/live_incidents.csv")
        df = pd.concat([df, live], ignore_index=True)
    filters = {"State": flt_state, "Mine": flt_mine, "AccidentType": flt_cause, "Year": flt_year}

    similar = []
    for m in reversed(st.session_state.messages):
        if m.get("sources"):
            similar = m["sources"]
            break
    pdf_path = generate_incident_report(df, filters, similar)
    st.success(f"Report created: {pdf_path}")
    st.download_button("Download Report", data=open(pdf_path,"rb").read(), file_name=pdf_path.split("/")[-1], mime="application/pdf")
