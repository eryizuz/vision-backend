import json
import datetime

class AnalyticsLogger:
    def __init__(self, filename="analytics.jsonl"):
        self.filename = filename

    def log(self, data):
        data["timestamp"] = datetime.datetime.now().isoformat()
        with open(self.filename, "a") as f:
            f.write(json.dumps(data) + "\n")
