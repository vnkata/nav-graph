#  Created by nphau on 9/16/22, 12:22 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/16/22, 12:22 AM
import os
import sys
import dash_renderjson

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc
from html_ids import *

ELEMENT_RESULT = "element-list"
ELEMENT_SEARCH = "element-search"
ELEMENT_OBJECT = "element-object"
SEARCH_HOLDER = "Enter tag name or display name to quickly find element..."
ELEMENT_ROW_PROPERTIES_TITLE = "row-element-properties-title"
ELEMENT_MODAL = "element-modal"
ELEMENT_MODEL_TITLE = "element-modal-title"
ELEMENT_SELECTED_OBJECT = "row-element-properties"
ELEMENT_BUTTON_OK = "button-element-ok"


def get_element_title(element):
    name = element.get("name", element.get("accessible_name", ""))
    return f"{name}"


def tag_name_mapping(tag_name):
    types = {
        "a": ["Anchor Link", "secondary"],
        "button": ["Button", "success"],
        "form": ["Input Field", "warning"],
    }
    return types.get(tag_name, "Unknown")


def create_element_display(element=None):
    if element is None:
        return []
    tags = tag_name_mapping(element.get("tag_name", ""))
    title = get_element_title(element)
    return [dbc.Badge(tags[0], color=tags[1], className="me-1"), f" {title}"]


def map_element(element):
    uuid = element.get("uuid", None)
    if uuid is not None:

        return dbc.ListGroupItem(
            create_element_display(element),
            id={
                "type": ELEMENT_OBJECT,
                "index": uuid
            }, n_clicks=0
        )
    else:
        return {}


def create_element_model_body():
    return dbc.Row(
        [
            dbc.Col(
                children=[
                    dbc.FormFloating(
                        [
                            dbc.Input(id=ELEMENT_SEARCH, type="text", placeholder=SEARCH_HOLDER),
                            dbc.Label(SEARCH_HOLDER),
                        ]
                    ),
                    dcc.Loading(
                        type="default",
                        children=dbc.ListGroup(
                            id=ELEMENT_RESULT, flush=True,
                            style={"height": "948px", "marginTop": "16px", "overflowY": "scroll", "cursor": "pointer"}
                        )
                    )
                ],
                className="assert-cell"
            ),
            dbc.Col(
                [
                    html.Div(
                        id=ELEMENT_ROW_PROPERTIES_TITLE,
                        style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "8px"}
                    ),
                    html.Div(id=ELEMENT_SELECTED_OBJECT)
                ],
                className="assert-cell"
            )
        ],
        className="assert-row-odd"
    )


def create_element_model():
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Test Object Input",
                    id=ELEMENT_MODEL_TITLE,
                    style={"fontSize": "1em", "width": "100%", "textAlign": "center", "fontWeight": "bold"}
                )
            ),
            dbc.ModalBody(create_element_model_body()),
            dbc.ModalFooter(
                dbc.Button("OK", id=ELEMENT_BUTTON_OK, color="primary", className="me-1", size="sm", n_clicks=0)
            )
        ],
        id=ELEMENT_MODAL,
        keyboard=False,
        size="xl",
        backdrop="static",
        scrollable=True,
        is_open=False
    )


def get_element_json_theme(content):
    theme = {
        "scheme": "monokai",
        "base00": "#272822",
        "base01": "#383830",
        "base02": "#49483e",
        "base03": "#75715e",
        "base04": "#a59f85",
        "base05": "#f8f8f2",
        "base06": "#f5f4f1",
        "base07": "#f9f8f5",
        "base08": "#f92672",
        "base09": "#fd971f",
        "base0A": "#f4bf75",
        "base0B": "#a6e22e",
        "base0C": "#a1efe4",
        "base0D": "#66d9ef",
        "base0E": "#ae81ff",
        "base0F": "#cc6633",
    }
    json_view = dash_renderjson.DashRenderjson(data=content, max_depth=-1, theme=theme, invert_theme=True)
    return json_view, map_element(content)
