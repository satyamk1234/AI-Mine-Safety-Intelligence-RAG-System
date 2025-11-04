import datetime

def fetch_news():
    
    return [
        {
            "Id": "news-"+datetime.datetime.utcnow().isoformat(),
            "Date": datetime.datetime.utcnow().date().isoformat(),
            "State": "",
            "Mine": "",
            "MineType": "",
            "AccidentType": "Mining safety news",
            "Injuries": "",
            "Fatalities": "",
            "Description": "No real Google News scrape yet - placeholder",
            "Source": "News",
            "Url": ""
        }
    ]
