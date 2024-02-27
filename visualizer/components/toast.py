#  Created by nphau on 9/15/22, 10:49 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 10:49 PM
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import dash_bootstrap_components as dbc


def create_toast(view_id, message="Sent"):
    return dbc.Toast(
        [
            message,
            dbc.Progress(value=100, animated=True, striped=True, style={"height": "3px"}, color="info")
        ],
        id=view_id, header="Notification", is_open=False, duration=1000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 256, "zIndex": 1000},
    )
