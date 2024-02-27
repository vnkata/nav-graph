#  Created by nphau on 9/15/22, 11:31 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:31 PM
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from dash_extensions.enrich import Output, Input, State, html, ALL
import dash_bootstrap_components as dbc
from icons import icon_run_to_this_place, icon_run_from_this_place, icon_edit, icon_delete
import html_ids
from html_ids import ID_SCREENSHOT, ID_SIDE_BAR, ID_PROPERTIES
from assertions import create_assertion_tab
import pandas as pd
from dash import dash_table, ctx, callback, no_update

TAB_PROPERTIES = "tab-properties"
TAB_SCREENSHOT = "tab-screenshot"
TAB_ASSERTION = "tab-assertion"
BUTTON_PLAY_TO_HERE = "ws-button-play-to-here"
BUTTON_PLAY_FROM_HERE = "ws-button-play-from-here"

IGNORE_PROPERTIES_FIELDS = ["current_title", "visited_flags", "uuid", "selected", "obj_uuids", "screenshot",
                            "text"]

KEY_DISPLAY_MAPPING = {
    "name": "Name",
    "text": "Text",
    "size": "Size",
    "rect": "Rect",
    "title": "Title",
    "location": "Location",
    "is_displayed": "Is Displayed",
    "is_enabled": "Is Enabled",
    "is_selected": "Is Selected",
    "tag_name": "Tag Name",
    "class": "Class",
    "href": "Href",
    "accessible_name": "Accessible Name",
    "access_time": "Recorded Time",
    "current_title": "Title",
    "current_url": "URL",
    "screenshot": "Screenshot",
    "num_objects": "Act. Elements"
}


def get_display_title(json_str):
    title = json_str.get("current_title", "")
    if not title:
        title = json_str.get("title", "")
        if not title:
            title = json_str.get("text", "")
    return title


def properties_to_table(json_str):
    fields = []
    values = []
    for key, value in json_str.items():
        if key not in IGNORE_PROPERTIES_FIELDS:
            if value is not None:
                fields.append(KEY_DISPLAY_MAPPING.get(key, key))
                values.append(str(value))
    df = pd.DataFrame({"Field": fields, "Value": values})
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        fixed_rows={'headers': True},
        style_table={'maxHeight': '784px', 'overflowY': 'auto'},
        style_cell={
            'lineHeight': '32px',
            'minHeight': '32px',
            'padding': '8px',
            'maxHeight': '32px',
            'textAlign': 'left',
            'maxWidth': '192px',
            'overflow': 'hidden',
            'font': 'Arial',
            'textOverflow': 'ellipsis'
        },
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Field'}, 'width': '20%'}
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(0,0,0,.03)',
            }
        ]
    )


tab_properties = dbc.Card(
    [
        dbc.CardBody(id=ID_PROPERTIES),
        dbc.CardFooter(
            dbc.ButtonGroup(
                children=[
                    dbc.Button(
                        icon_run_to_this_place(),
                        id=BUTTON_PLAY_TO_HERE, n_clicks=0,
                        color="primary", style={"display": "none"}
                    ),
                    dbc.Button(
                        icon_run_from_this_place(),
                        id=BUTTON_PLAY_FROM_HERE, n_clicks=0,
                        color="success", style={"display": "none"}
                    ),
                    dbc.Button(
                        icon_delete(),
                        n_clicks=0,
                        color="danger"
                    ),
                    dbc.Button(
                        icon_edit({"marginRight": "6px"}),
                        color="warning"
                    )
                ],
                style={"float": "right"}
            )
        )
    ],
    className="mt-3"
)


def create_sidebar_content():
    return dbc.CardBody(
        dbc.Tabs(
            [
                dbc.Tab(tab_properties, id=TAB_PROPERTIES, label="Properties", disabled=True),
                dbc.Tab(create_assertion_tab(), id=TAB_ASSERTION, label="Assertions", disabled=True),
                dbc.Tab(html.Div(id=ID_SCREENSHOT), id=TAB_SCREENSHOT, label="Screenshot", disabled=True)
            ]
        ),
        style={},
        id=ID_SIDE_BAR,
    )


@callback(
    Output(html_ids.ID_PROPERTIES, "children"),
    Input(html_ids.STORE_STARTED_NODE, "data"),
    prevent_initial_call=True
)
def show_properties(data):
    return html.Div([
        dbc.Badge(
            get_display_title(data), color="danger", className="me - 1",
            style={"marginBottom": "16px", "width": "100%"}),
        properties_to_table(data)
    ])
