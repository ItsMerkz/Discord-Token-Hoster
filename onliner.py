import json
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import websocket


def changegame(token, game, type, status):
    print("Done " + token)
    ws = websocket.WebSocket()
    if status == "random":
        stat = ['online', 'dnd', 'idle']
        status = random.choice(stat)
    ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
    hello = json.loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    if type == "Playing":
        gamejson = {
            "name": game,
            "type": 0
        }
    elif type == 'Streaming':
        gamejson = {
            "name": game,
            "type": 1,
            "url": "https://www.twitch.tv/soulless.cc"
        }
    elif type == "Listening to":
        gamejson = {
            "name": game,
            "type": 2
        }
    elif type == "Watching":
        gamejson = {
            "name": game,
            "type": 3
        }
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": sys.platform,
                "$browser": "RTB",
                "$device": f"{sys.platform} Device"
            },
            "presence": {
                "game": gamejson,
                "status": status,
                "since": 0,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    ws.send(json.dumps(auth))
    ack = {
        "op": 1,
        "d": None
    }
    while True:
        time.sleep(heartbeat_interval / 1000)
        try:
            ws.send(json.dumps(ack))
        except Exception as e:
            break


def main():
    types = ['Playing', 'Streaming', 'Watching', 'Listening to']
    type = "Playing"
    game = input("status: ")
    status = ['online', 'dnd', 'idle','random']
    status = status[3]
    executor = ThreadPoolExecutor(max_workers=1000)

    for token in open("tokens.txt","r+").readlines():
        threading.Thread(target=lambda : changegame(token.replace("\n",""), game, type, status)).start()

main()