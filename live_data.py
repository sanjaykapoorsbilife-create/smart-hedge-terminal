import websocket
import json
import threading

# GLOBAL STORAGE (used by Streamlit)
live_prices = {
    "NIFTY": 0,
    "SENSEX": 0,
    "VIX": 0
}

CLIENT_ID = "YOUR_CLIENT_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

def on_message(ws, message):
    global live_prices

    data = json.loads(message)

    if "data" in data:
        for item in data["data"]:
            sec_id = item.get("securityId")
            price = item.get("lastTradedPrice")

            if sec_id == "13":
                live_prices["NIFTY"] = price
            elif sec_id == "51":
                live_prices["SENSEX"] = price
            elif sec_id == "17":
                live_prices["VIX"] = price

def on_open(ws):
    print("Connected to Dhan WebSocket")

    payload = {
        "RequestCode": 15,
        "InstrumentCount": 3,
        "InstrumentList": [
            {"ExchangeSegment": "IDX_I", "SecurityId": "13"},
            {"ExchangeSegment": "IDX_I", "SecurityId": "51"},
            {"ExchangeSegment": "IDX_I", "SecurityId": "17"}
        ]
    }

    ws.send(json.dumps(payload))

def start_ws():
    ws = websocket.WebSocketApp(
        "wss://api-feed.dhan.co",
        header=[
            f"access-token:{ACCESS_TOKEN}",
            f"client-id:{CLIENT_ID}"
        ],
        on_open=on_open,
        on_message=on_message
    )

    ws.run_forever()

def start_background_ws():
    thread = threading.Thread(target=start_ws)
    thread.daemon = True
    thread.start()
