#  Created by nphau on 9/15/22, 11:21 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:21 PM

import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc
from icons import icon_play
from dash_extensions import Purify

OFF_CANVAS_GRAPH_INFO = "off-canvas-graph-info"


def create_info(metadata):
    info = []
    for m in metadata:
        info.append(dbc.ListGroupItem(Purify(f"{m[0]} : <b>{m[1]}</b>"), disabled=False))
    return dbc.ListGroup(info, flush=True)


def create_graph_info(metadata):
    return dbc.Offcanvas(
        children=[
            dbc.Badge(
                "Information", color="success", className="me-1",
                style={"marginBottom": "8px"}
            ),
            create_info(metadata),
            dbc.Card([
                dbc.CardHeader("Setting"),
                dbc.CardBody(
                    children=[
                        dbc.Badge(
                            "Filter", color="success", className="me-1",
                            style={"marginTop": "8px", "marginBottom": "8px"}
                        ),
                        dcc.Dropdown(
                            options={
                                '1': 'All',
                                '2': 'Only Error Path(s)',
                                '3': 'Only Success Path(s)',
                                '4': 'Dev/Tester'
                            },
                            value='1'
                        )
                    ]
                ),
                dbc.CardFooter(dbc.Button(icon_play(), color="primary", size="sm", style={"float": "right"}))
            ], style={"marginTop": "16px"})

        ],
        id=OFF_CANVAS_GRAPH_INFO, title="Graph Configuration", backdrop="static", is_open=False
    )
