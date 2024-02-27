import asyncio
import json
from quart import websocket, Quart

app = Quart(__name__)

SOCKET_PATH_SERVER = "/server"
SOCKET_PATH_CLIENT = "/client"


@app.websocket(f"{SOCKET_PATH_SERVER}")
async def ws():
    play_back = {'type': 'INIT',
                 'value': ['ybwhh', 'burdn', 'yhxcl', 'efflf', 'abzzr', 'pnuqd', 'pzbqh', 'mrmqd', 'pvoah', 'xsmdc']}
    json_string = json.dumps(play_back)
    print(f"Init play back ...{play_back['value']}")
    print("1 ...")
    await asyncio.sleep(1)
    print("2 ...")
    await asyncio.sleep(1)
    print("3 ...")
    await asyncio.sleep(1)
    await websocket.send_json(json_string)
    await asyncio.sleep(10)
    #
    for node in play_back['value']:
        await asyncio.sleep(1)
        print(f"Play ...{node}")
        play_node = {'type': 'PLAY', 'value': node}
        json_string = json.dumps(play_node)
        await websocket.send_json(json_string)


if __name__ == "__main__":
    app.run(port=5000)
