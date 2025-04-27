# Parse the data returned by the api

def parse_event(update):
    return {"timestamp": update["starred_at"], "user": update["user"]["login"], "event": "added"}
