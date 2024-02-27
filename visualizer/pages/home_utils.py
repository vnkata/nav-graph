#  Created by nphau on 11/13/22, 4:01 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/13/22, 4:01 PM
import json
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import page_utils
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc
from components import icons
import crawler_logger

ID_BUTTON_START_CRAWLING = "id-button-start-crawling"
ID_BUTTON_STOP_CRAWLING = "id-button-stop-crawling"
ID_CRAWLING_DIALOG = "id-crawling-dialog"
ID_CRAWLING_PROGRESS_TITLE = "id-crawling-progress-title"
ID_CRAWLING_PROGRESS = "id-crawling-progress"
ID_CRAWLING_PROGRESS_CONTENT = "id-crawling-progress-content"
ID_CRAWLING_PROGRESS_INTERVAL = "id-crawling-progress-interval"

PROCESS_STATUS_NEW = "new"
PROCESS_STATUS_INPROGRESS = "inprogress"
PROCESS_STATUS_FAILED = "failure"


def create_project_status_badge(item):
    status = page_utils.extract_value(item, 'status')
    css_status = status
    if status == PROCESS_STATUS_NEW:
        css_status = "primary"
    if status == PROCESS_STATUS_INPROGRESS:
        css_status = "info"
    if status == PROCESS_STATUS_FAILED:
        css_status = "danger"
    status = status.capitalize()
    return dbc.Badge(f"{status}", color=f"{css_status}", className="me-1", style={"marginBottom": "8px"})


def create_project_action(item):
    status = page_utils.extract_value(item, 'status')
    if status == "new":
        return dbc.Button(
            icons.icon_play("Start a crawler"),
            id=ID_BUTTON_START_CRAWLING,
            color="success", style={"float": "right"}
        )
    if status == "inprogress":
        return dbc.Button(
            icons.icon_play("Re-start a crawler"),
            id=ID_BUTTON_START_CRAWLING,
            color="dark", style={"float": "right"}
        )
    if status == "success":
        return dbc.Button(
            icons.icon_graph("Visualizer >>"), color="primary",
            href=f"/graph/{item['id']}", target="_blank", external_link=True,
            style={"float": "right"})
    else:
        return dbc.Button(
            icons.icon_play("Start a crawler"),
            id=ID_BUTTON_START_CRAWLING,
            color="success", style={"float": "right"}
        )


def create_projects_view(item, project_types):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(create_project_status_badge(item)),
                    dbc.Col(create_project_action(item))
                ]),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Label("Name"),
                        dbc.Input(type="text", value=page_utils.extract_value(item, 'name'), readonly=True)
                    ], width=4),
                    dbc.Col([
                        dbc.Label("Url"),
                        dbc.Input(type="text", value=page_utils.extract_value(item, 'url'), readonly=True)
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Type"),
                        dbc.RadioItems(
                            options=project_types,
                            value=page_utils.extract_value(item, 'type'), inline=True
                        ),
                    ], width=2)
                ], style={"marginTop": "8px"}
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Label("Duration"),
                        dbc.Input(type="text", value=f"{page_utils.duration(item)}", readonly=True)
                    ], width=2),
                    dbc.Col([
                        dbc.Label("Start Time"),
                        dbc.Input(type="text",
                                  value=f"{page_utils.to_date(page_utils.extract_value(item, 'startTime'))}",
                                  readonly=True)
                    ], width=2),
                    dbc.Col([
                        dbc.Label("End Time"),
                        dbc.Input(type="text", value=f"{page_utils.to_date(page_utils.extract_value(item, 'endTime'))}",
                                  readonly=True)
                    ], width=2),
                    dbc.Col(html.Span(
                        [
                            dbc.Button(
                                [
                                    "Place",
                                    dbc.Badge(page_utils.extract_value(item, 'place'), color="light", pill=True,
                                              text_color="primary",
                                              className="ms-1"),
                                ],
                                color="primary",
                            ),
                            dbc.Button(
                                [
                                    "Transition",
                                    dbc.Badge(page_utils.extract_value(item, 'transition'), color="light", pill=True,
                                              text_color="secondary",
                                              className="ms-1"),
                                ],
                                color="secondary",
                            ),
                            dbc.Button(
                                [
                                    "Paths",
                                    dbc.Badge(page_utils.extract_value(item, 'paths'), color="light", pill=True,
                                              text_color="success",
                                              className="ms-1"),
                                ],
                                color="success",
                            ),
                            dbc.Button(
                                [
                                    "Roots",
                                    dbc.Badge(page_utils.extract_value(item, 'root'), color="light", pill=True,
                                              text_color="info",
                                              className="me-1"),
                                ],
                                color="info",
                            )
                        ]), width=6, style={"display": "flex", "alignItems": "end"})
                ], style={"marginTop": "8px"}
            ),
            dbc.Textarea(value=page_utils.extract_value(item, 'description'), rows="5", className="mb-3",
                         placeholder="Description", disabled=True,
                         style={"marginTop": "8px"})
        ]
    )


def create_crawling_dialog():
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Crawling", id=ID_CRAWLING_PROGRESS_TITLE,
                    style={"fontSize": "1em", "width": "100%", "textAlign": "center", "fontWeight": "bold"}
                ),
                close_button=False
            ),
            dbc.ModalBody(
                [
                    dbc.Progress(
                        id=ID_CRAWLING_PROGRESS,
                        label="0%", value=0, color="info", striped=True, animated=True,
                        style={"marginBottom": "16px"}
                    ),
                    dbc.ListGroup(id=ID_CRAWLING_PROGRESS_CONTENT,
                                  flush=True,
                                  style={"height": "256px", "overflow": "scroll"})
                ], style={"padding": "16px"}
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Stop", color="danger", className="me-1", size="sm", n_clicks=0,
                    id=ID_BUTTON_STOP_CRAWLING
                )
            )
        ],
        id=ID_CRAWLING_DIALOG,
        keyboard=False,
        size="lg",
        centered=True,
        backdrop="static",
        scrollable=False,
        is_open=False
    )


def create_crawling_interval():
    return dcc.Interval(id=ID_CRAWLING_PROGRESS_INTERVAL, n_intervals=0, interval=3 * 1000, disabled=True),


def parse_crawling_log(line, project_id):
    log = json.loads(line)
    timestamp = log['timestamp']
    message = log['message']
    if message == f"CRAWLING_START: {project_id}":
        return dbc.ListGroupItem(message, key=timestamp, color="primary", disabled=False), False
    if message == f"CRAWLING_END: {project_id}":
        return dbc.ListGroupItem(message, key=timestamp, color="danger", disabled=False), True
    return dbc.ListGroupItem(message, key=timestamp, disabled=True), False


def get_crawling_log(project_id):
    try:
        is_end = False
        with open(f"./{crawler_logger.get_log_file_path(project_id)}", "r") as f:
            views = []
            for line in f:
                try:
                    view, is_end_signal = parse_crawling_log(line.rstrip('\n'), project_id)
                    if is_end_signal:
                        is_end = is_end_signal
                except:
                    view = None
                if view is not None:
                    views.append(view)
            return views, is_end
    except:
        return [], False
