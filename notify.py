import os, json, requests, pandas as pd
from .engine import compute_alerts

STATE_FILE = "data/.alerts_state.json"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE, "r", encoding="utf-8"))
    return {"last_alerts": []}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w", encoding="utf-8"))

def notify_slack(text):
    if not SLACK_WEBHOOK_URL:
        print(text)   # fallback to console
        return

    requests.post(SLACK_WEBHOOK_URL, json={"text": text})

def main():
    # Load historical + live data
    df = pd.read_csv("data/accidents.csv") if os.path.exists("data/accidents.csv") else pd.DataFrame()
    if os.path.exists("data/live_incidents.csv"):
        live = pd.read_csv("data/live_incidents.csv")
        df = pd.concat([df, live], ignore_index=True)

    if df.empty:
        print("No data available for alerts.")
        return

    alerts = compute_alerts(df)
    state = load_state()
    seen = set(tuple(a.items()) for a in state.get("last_alerts", []))

    fresh = [a for a in alerts if tuple(a.items()) not in seen]

    for a in fresh:
        msg = (
            f"Alert: {a['type']}\n"
            f"State: {a.get('state','')}\n"
            f"Period: {a.get('period','')}\n"
            f"Cause: {a.get('cause','')}\n"
            f"Fatalities: {a.get('fatalities','')}\n"
            f"Count: {a.get('count','')}"
        )
        notify_slack(msg)

    state["last_alerts"] = alerts
    save_state(state)

    print(f"Alerts processed. New alerts sent: {len(fresh)}")

if __name__ == "__main__":
    main()
