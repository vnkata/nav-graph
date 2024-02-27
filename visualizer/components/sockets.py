#  Created by nphau on 9/26/22, 10:42 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/26/22, 10:42 PM
import os
import sys
from loguru import logger
from dash import ctx, callback, no_update
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from dash_extensions.enrich import Output, Input, State, html, ALL
from dash_extensions import WebSocket
import json
from dash.exceptions import PreventUpdate

WS_SERVER = "ws-server"
WS_INPUT = "ws-input"

SOCKET_PATH_SERVER = "ws://127.0.0.1:5000/server"

SOCKET_TYPE_PLAY = "PLAY"
# {
#     "type" : "PLAY",
#     "value": "adahl"
# }

SOCKET_TYPE_INIT = "INIT"

# {
#      "type" : "INIT",
#      "value": ["adahl", "jlgjm", "okzxy", "edyoo", "poaop"]
# }

SOCKET_TYPE_PLAY_TO_HERE = "PLAY_TO_HERE"
SOCKET_TYPE_FROM_TO_HERE = "PLAY_FROM_HERE"
SOCKET_TYPE_RUN_ALL = "RUN_ALL"

# {
#      "type" : "PLAY_TO_HERE",
#      "value": "adahl"
# }

SOCKET_TYPE_ASSERTION = "ASSERTION"


# {
#      "type" : "ASSERTION",
#      "value": {
# 	        "place_name":  "asdasd",
#           assertions: [
# 		        {"assertion_type": verifyElementVisible,  "object":  "uuid",   "attribute": None,  "desired_value":  None  },
# 		        {"assertion_type": verifyElementHasAttribute,  "object":  "uuid",   "attribute": "href",  "desired_value":  "https://google.com"  },
# 		        {"assertion_type": verifyTextPresent,  "object":  "abc456",   "attribute": None,  "desired_value":  "My Account"  }
#           ]
# 	    }
# }


def create_web_socket():
    return WebSocket(id=WS_SERVER, url=f"{SOCKET_PATH_SERVER}")


def create_assertion_event(body):
    return json.dumps({SOCKET_TYPE_ASSERTION: body})


def create_play_to_here_event(selected_node):
    logger.info("Signaling [PLAY_TO_HERE] ...")
    return json.dumps({
        "type": SOCKET_TYPE_PLAY_TO_HERE,
        "value": selected_node
    })


def create_play_from_here_event(selected_node):
    logger.info("Signaling [PLAY_FROM_HERE] ...")
    return json.dumps({
        "type": SOCKET_TYPE_FROM_TO_HERE,
        "value": selected_node
    })


def create_run_all():
    logger.info("Signaling [RUN_ALL] ...")
    return json.dumps({"type": SOCKET_TYPE_RUN_ALL})


@callback(
    Output(WS_SERVER, "send"),
    Input(WS_INPUT, "value")
)
def on_send(value):
    if value is None:
        raise PreventUpdate
    print(f"on_send: \n{value}")
    return value