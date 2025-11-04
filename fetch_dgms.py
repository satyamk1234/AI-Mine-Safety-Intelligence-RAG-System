import requests
from datetime import datetime

DGMS_URL = "https://dgms.gov.in/UserView/index"

def fetch_dgms_alerts():
    return [] 

def to_incident(raw):
    return {
        "Id": raw.get("id","dgms-"+datetime.utcnow().isoformat()),
        "Date": raw.get("date",""),
        "State": raw.get("state",""),
        "Mine": raw.get("mine",""),
        "MineType": raw.get("mine_type",""),
        "AccidentType": raw.get("accident_type",""),
        "Injuries": raw.get("injuries",""),
        "Fatalities": raw.get("fatalities",""),
        "Description": raw.get("description",""),
        "Source": "DGMS",
        "Url": raw.get("url","")
    }
