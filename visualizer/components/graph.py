#  Created by nphau on 9/15/22, 11:28 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 9:00 PM
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
import dash_interactive_graphviz as graphviz
from html_ids import ID_GRAPH

BUTTON_RUN_ALL = "ws-button-run-all"
BUTTON_GRAPH_INFO = "button-graph-info"
BUTTON_GRAPH_EXTEND = "button-graph-extend"
BUTTON_GRAPH_EXTEND_ICON = "button-graph-extend-icon"


def create_graph_content(dot_string):
    return dbc.Card(
        id="graph-card",
        children=[
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                "J2Demo.com",
                                html.Small("Click on a node to see its details here", className="text-muted")
                            ],
                            style={"display": "flex", "justifyContent": "center", "flexDirection": "column",
                                   "fontWeight": "bold"},
                            md=10
                        ),
                        dbc.Col(
                            dbc.ButtonGroup(
                                [
                                    dbc.Button(
                                        html.I(className="bi bi-sliders", style={"color": "blue"}),
                                        color="light", size="md", id=BUTTON_GRAPH_INFO, style={"float": "right"}
                                    ),
                                    dbc.Button(
                                        html.I(className="bi bi-download", style={"color": "blue"}),
                                        color="light", size="md", style={"float": "right"}
                                    ),
                                    dbc.Button(
                                        html.I(
                                            className="bi bi-chevron-double-right", style={"color": "blue"},
                                            id=BUTTON_GRAPH_EXTEND_ICON
                                        ),
                                        color="light", size="md", id=BUTTON_GRAPH_EXTEND, style={"float": "right"}
                                    ),
                                    dbc.Button(
                                        html.I(className="bi bi-play", style={"color": "blue"}),
                                        id=BUTTON_RUN_ALL, n_clicks=0,
                                        style={"float": "right"},
                                        color="light", size="md", className="me-1"
                                    )
                                ],
                                style={"float": "right"}
                            ),
                            md=2
                        )
                    ],
                )),
            dbc.CardBody(
                graphviz.DashInteractiveGraphviz(
                    id=ID_GRAPH, dot_source=dot_string,
                    # "dot", "neato",
                    fit_button_content="⦿", style={"width": "95%"},
                    fit_button_style={"fontSize": "48px", "color": "grey", "marginLeft": "8px", "marginTop": "8px"}
                )
            )
        ]
    )
