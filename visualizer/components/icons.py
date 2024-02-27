#  Created by nphau on 9/15/22, 9:30 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 9:30 PM

from dash_extensions.enrich import html


def icon_edit(new_style=None):
    return html.Span([html.I(className="bi bi-pencil-square", style=new_style)])


def icon_play(title=""):
    return html.Span([html.I(className="bi bi-play-fill", style={"marginRight": "6px"}), title])


def icon_graph(title=""):
    return html.Span([html.I(className="bi bi-diagram-3-fill", style={"marginRight": "6px"}), title])


def icon_delete(title="", new_style=None):
    if new_style is None:
        new_style = {}
    return html.Span([html.I(className="bi bi-trash3-fill", style=new_style), title])


def icon_add(title="", new_style=None):
    if new_style is None:
        new_style = {}
    return html.Span([html.I(className="bi bi-plus-square-fill", style=new_style), title])


def icon_element_selected(id):
    return html.Span(
        [html.I(className="bi bi-box-arrow-in-up-right", style={"marginLeft": "6px", "color": "blue"})],
        id=id, n_clicks=None
    )


def icon_assertion_add():
    return icon_add("Add", {"marginRight": "6px"})


def icon_assertion_delete():
    return icon_delete("Delete", {"marginRight": "6px"})


def icon_assertion_save():
    return html.Span([html.I(className="bi bi-send-plus-fill", style={"marginRight": "6px"}), "Save"])


def icon_run_to_this_place():
    return html.Span([html.I(className="bi bi-box-arrow-in-down-right", style={"marginRight": "6px"})])


def icon_run_from_this_place():
    return html.Span([html.I(className="bi bi-box-arrow-in-up-right", style={"marginRight": "6px"})])
