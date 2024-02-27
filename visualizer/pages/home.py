#  Created by nphau on 10/22/22, 3:29 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 10/22/22, 3:29 PM
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import dash
import dash_bootstrap_components as dbc
from dash import ctx, callback, no_update
from dash_extensions.enrich import Output, Input, State, html, dcc, ALL
from dash.exceptions import PreventUpdate
from db.db_firebase import DbFirebase
from components import icons, html_ids, validator, encryptor, cache
import page_utils
import home_utils
import home_crawling

dash.register_page(__name__, path="/", redirect_from=["/home"])

TYPE_PROJECT_ROW = "type-project-row"
ID_PROJECT_VIEW = "id-project-view"
ID_PROJECT_LIST = "id-project-list"
ID_BUTTON_ADD_PROJECT = "id-button-add-project"
ID_BUTTON_APPLY_PROJECT = "id-button-apply-project"
ID_PROJECT_EDITOR_DIALOG = "id-project-editor-dialog"
ID_PROJECT_EDITOR_DIALOG_TITLE = "id-project-editor-dialog-title"
ID_PROJECT_NAME = "id-project-name"
ID_PROJECT_URL = "id-project-url"
ID_PROJECT_TYPE = "id-project-type"
ID_PROJECT_DESCRIPTION = "id-project-description"
ID_DIALOG_DELETE_CONFIRM = "id-dialog-delete-confirm"
STORE_REFRESH_PROJECT_LIST = "store-refresh-projects"
STORE_PROJECTS = "store-projects"
STORE_SELECTED_PROJECT = "store-selected-project"

dbFireBase = DbFirebase()


def create_project_view(idx, item, selected):
    return dbc.ListGroupItem(
        [
            home_utils.create_project_status_badge(item),
            html.H6(f"{page_utils.extract_value(item, 'url')}", className="mb-1"),
            html.P(
                f"Places: {page_utils.extract_value(item, 'place')} - Transition: {page_utils.extract_value(item, 'transition')} - "
                f"Object: {page_utils.extract_value(item, 'object')} - "
                f"Interaction paths: {page_utils.extract_value(item, 'paths')} - Roots: {page_utils.extract_value(item, 'root')}",
                className="mb-1"),
            html.Small(f"{page_utils.to_date(page_utils.extract_value(item, 'endTime'))}", className="text-muted",
                       style={"float": "right"}),
            html.Br(),
            html.Small(f"{page_utils.duration(item)}", className="text-muted", style={"float": "right"})
        ], key=f"{item['id']}", className="pointer", color=f"{page_utils.extract_value(item, 'status')}",
        id={
            "type": TYPE_PROJECT_ROW,
            "index": idx
        }
    )


def create_project_editor():
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Project View", id=ID_PROJECT_EDITOR_DIALOG_TITLE,
                    style={"fontSize": "1em", "width": "100%", "textAlign": "center", "fontWeight": "bold"}
                )
            ),
            dbc.ModalBody(
                [
                    dbc.Row(
                        [
                            dbc.Col([
                                dbc.Label("Name", html_for=ID_PROJECT_NAME),
                                dbc.Input(type="text", id=ID_PROJECT_NAME)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Url", html_for=ID_PROJECT_URL),
                                dbc.Input(type="text", id=ID_PROJECT_URL)
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Type"),
                                dbc.RadioItems(
                                    options=dbFireBase.project_types(),
                                    value=1, id=ID_PROJECT_TYPE, inline=True
                                ),
                            ], width=4)
                        ]
                    ),
                    dbc.Textarea(rows="5", className="mb-3", id=ID_PROJECT_DESCRIPTION,
                                 placeholder="Description", style={"marginTop": "16px"})
                ], style={"padding": "16px"}
            ),
            dbc.ModalFooter(
                dbc.Button("OK", id=ID_BUTTON_APPLY_PROJECT, color="primary", className="me-1", size="sm",
                           n_clicks=0)
            ),
        ],
        id=ID_PROJECT_EDITOR_DIALOG,
        keyboard=False,
        size="lg",
        backdrop="static",
        scrollable=True,
        is_open=False
    )


layout = [
    html.H2(
        "Navigation Graph Projects",
        className="app_header uppercase bold",
        style={"marginTop": "32px"}
    ),
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            "Projects",
                            dbc.Button(
                                icons.icon_add(), id=ID_BUTTON_ADD_PROJECT,
                                outline=True, color="primary", size="sm", className="me-1",
                                style={"float": "right"}
                            )
                        ]
                    ),
                    dbc.CardBody(id=ID_PROJECT_LIST)
                ]
            ), width=4),
            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader("Project View"),
                    dbc.CardBody([
                        html.Div(id=ID_PROJECT_VIEW),
                        dcc.ConfirmDialogProvider(
                            children=dbc.Button(
                                icons.icon_delete(),
                                color="danger",
                                style={"float": "right"}
                            ),
                            id=ID_DIALOG_DELETE_CONFIRM,
                            message='Are you sure you want to delete?'
                        )
                        # dbc.Button(
                        #     icons.icon_play("Start crawling"),
                        #     id=ID_BUTTON_START_CRAWLING,
                        #     color="success", style={"float": "right"}
                        # )
                    ])
                ]
            ), width=8)
        ], style={"margin": "32px 1%"}
    ),
    create_project_editor(),
    home_utils.create_crawling_dialog(),
    dcc.Interval(id=home_utils.ID_CRAWLING_PROGRESS_INTERVAL, n_intervals=0, interval=5 * 1000, disabled=True),
    dcc.Store(id=STORE_PROJECTS, data=[]),
    dcc.Store(id=STORE_SELECTED_PROJECT, data={}),
    dcc.Store(id=STORE_REFRESH_PROJECT_LIST, data=True)
]


@callback(
    Output(ID_PROJECT_VIEW, "children"),
    Output(STORE_SELECTED_PROJECT, "data"),
    Input({"type": TYPE_PROJECT_ROW, "index": ALL}, "n_clicks"),
    State(STORE_PROJECTS, "data")
)
def on_project_row_clicked(n_clicks, projects):
    try:
        triggered_id = ctx.triggered_id
        if triggered_id is None:
            selected = projects[0]
            return home_utils.create_projects_view(selected, dbFireBase.project_types()), selected
        else:
            view_type = triggered_id.get("type", None)
            index = triggered_id.get("index", -1)
            if view_type == TYPE_PROJECT_ROW:
                selected = projects[index]
                return home_utils.create_projects_view(selected, dbFireBase.project_types()), selected
            raise PreventUpdate
    except:
        raise PreventUpdate


@callback(
    Output(STORE_PROJECTS, "data"),
    Output(ID_PROJECT_LIST, "children"),
    Input(STORE_REFRESH_PROJECT_LIST, "data"),
    State(STORE_SELECTED_PROJECT, "data")
)
def load_projects(is_refresh, selected_project):
    if is_refresh:
        projects = dbFireBase.get_projects()
        views = []
        for idx, item in enumerate(projects):
            if item['id'] == page_utils.extract_value(selected_project, 'id'):
                views.append(create_project_view(idx, item, True))
            else:
                views.append(create_project_view(idx, item, False))
        return projects, dbc.ListGroup(views, style={"height": "384px", "overflow": "scroll"})
    else:
        raise PreventUpdate


@callback(
    [
        Output(ID_PROJECT_EDITOR_DIALOG, 'is_open'),
        Output(ID_PROJECT_EDITOR_DIALOG_TITLE, 'children'),
        Output(STORE_REFRESH_PROJECT_LIST, 'data')
    ],
    [
        Input(ID_BUTTON_ADD_PROJECT, 'n_clicks'),
        Input(ID_BUTTON_APPLY_PROJECT, 'n_clicks'),
        Input(ID_DIALOG_DELETE_CONFIRM, 'submit_n_clicks')
    ],
    [
        State(STORE_SELECTED_PROJECT, 'data'),
        State(ID_PROJECT_NAME, 'value'),
        State(ID_PROJECT_URL, 'value'),
        State(ID_PROJECT_TYPE, 'value'),
        State(ID_PROJECT_DESCRIPTION, 'value'),
    ],
    prevent_initial_call=True
)
def project_actions(add_clicks, apply_clicks, delete_clicks,
                    selected_project, name, url, type, description):
    triggered_id = ctx.triggered_id
    if triggered_id == ID_BUTTON_ADD_PROJECT:
        return True, "New Project", no_update
    if triggered_id == ID_DIALOG_DELETE_CONFIRM:
        dbFireBase.delete_project(selected_project['id'])
        return no_update, no_update, True
    if triggered_id == ID_BUTTON_APPLY_PROJECT:
        if name and validator.is_url_valid(url):
            dbFireBase.create_project(url, name, type, description)
        return False, no_update, True
    raise PreventUpdate


@callback(
    [
        Output(home_utils.ID_CRAWLING_DIALOG, 'is_open'),
        Output(home_utils.ID_CRAWLING_PROGRESS_INTERVAL, 'disabled'),
        Output(home_utils.ID_CRAWLING_PROGRESS, "value"),
        Output(home_utils.ID_CRAWLING_PROGRESS, "label"),
        Output(home_utils.ID_CRAWLING_PROGRESS_CONTENT, "children"),
        Output(home_utils.ID_CRAWLING_PROGRESS_TITLE, "children"),
    ],
    [
        Input(home_utils.ID_CRAWLING_PROGRESS_INTERVAL, "n_intervals"),
        Input(home_utils.ID_BUTTON_START_CRAWLING, 'n_clicks'),
        Input(home_utils.ID_BUTTON_STOP_CRAWLING, 'n_clicks'),
    ],
    State(STORE_SELECTED_PROJECT, 'data'),
    prevent_initial_call=True
)
def on_update_crawling_progress(n, start_clicks, stop_clicks, selected_project):
    triggered_id = ctx.triggered_id
    # When tap on START
    if triggered_id == home_utils.ID_BUTTON_START_CRAWLING and start_clicks is not None:
        dbFireBase.start_project(selected_project['id'])
        home_crawling.start_crawling(selected_project)
        # Open dialog | Start internal
        return True, False, no_update, no_update, no_update, no_update
    # When tap on STOP
    if triggered_id == home_utils.ID_BUTTON_STOP_CRAWLING and stop_clicks is not None:
        dbFireBase.end_project(selected_project['id'], home_utils.PROCESS_STATUS_FAILED)
        home_crawling.stop_crawling()
        # Close dialog | Stop internal
        return False, True, 0, "0%", [], no_update
    # When REFRESH
    if triggered_id == home_utils.ID_CRAWLING_PROGRESS_INTERVAL:
        crawling_logs, is_end = home_utils.get_crawling_log(selected_project['id'])
        # if there is any END signal event, the crawling process will end
        if is_end:
            # Keep dialog open | Stop internal |  Progress: 100 | Progress value: 100% | dialog Title
            return no_update, True, 100, "100%", crawling_logs, f"Crawling: {selected_project['url']}"
        else:
            # only add text after 5% progress to ensure text isn't squashed too much
            # check progress of some background process, in this example we'll just
            # use n_intervals constrained to be in 0-100
            progress = min(n % 110, 100)
            if n > 1:
                if len(crawling_logs) == 0:
                    return no_update, no_update, progress, f"{progress} %" if progress >= 5 else "", no_update, no_update
                else:
                    return no_update, no_update, progress, f"{progress} %" if progress >= 5 else "", crawling_logs, no_update
            return no_update, no_update, progress, f"{progress} %" if progress >= 5 else "", no_update, f"Crawling: {selected_project['url']}"
    else:
        raise PreventUpdate
