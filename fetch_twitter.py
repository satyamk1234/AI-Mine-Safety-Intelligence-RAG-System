import datetime

def fetch_tweets():
    return [
        {
            "Id": "twitter-"+datetime.datetime.utcnow().isoformat(),
            "Date": datetime.datetime.utcnow().date().isoformat(),
            "State": "",
            "Mine": "",
            "MineType": "",
            "AccidentType": "Mine accident",
            "Injuries": "",
            "Fatalities": "",
            "Description": "No real Twitter scrape yet - placeholder",
            "Source": "Twitter",
            "Url": ""
        }
    ]
