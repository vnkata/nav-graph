#  Created by nphau on 9/15/22, 11:34 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:34 PM

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from dash_extensions.enrich import Output, Input, State, html, dcc, ALL
import dash_bootstrap_components as dbc
import html_ids
from icons import icon_assertion_add, icon_assertion_delete, icon_assertion_save, icon_element_selected
from elements import create_element_display
from dropdown import create_dropdown
from loguru import logger
import json
from PIL import Image

# region DEFINE
ASSERTIONS_TYPE = "assertion-type"
TYPE_ASSERTIONS_INPUTS = "type-assertion-input"
TYPE_ASSERTIONS_ATTRIBUTE = "type-assertion-attribute"
TYPE_ASSERTIONS_OBJECT = "type-assertion-object"
TYPE_ASSERTIONS_TYPES = "type-assertion-types"
DOM_OBJECT = "DOM Object"
ASSERT_TYPE_VERIFY_REGION = "verifyRegionExist"
ASSERT_TYPE_VERIFY_TEXT_PRESENT = "verifyTextPresent"
ASSERT_TYPE_VERIFY_ELEMENT_VISIBLE = "verifyElementVisible"
ASSERT_TYPE_VERIFY_ELEMENT_ATTRIBUTE = "verifyElementAttributeValue"
ASSERT_TYPE_VERIFY_ELEMENT_HAS_ATTRIBUTE = "verifyElementHasAttribute"
ASSERTIONS_TYPES = [
    {"label": ASSERT_TYPE_VERIFY_ELEMENT_VISIBLE, "value": ASSERT_TYPE_VERIFY_ELEMENT_VISIBLE},
    {"label": ASSERT_TYPE_VERIFY_ELEMENT_HAS_ATTRIBUTE, "value": ASSERT_TYPE_VERIFY_ELEMENT_HAS_ATTRIBUTE},
    {"label": ASSERT_TYPE_VERIFY_TEXT_PRESENT, "value": ASSERT_TYPE_VERIFY_TEXT_PRESENT},
    {"label": ASSERT_TYPE_VERIFY_ELEMENT_ATTRIBUTE, "value": ASSERT_TYPE_VERIFY_ELEMENT_ATTRIBUTE},
    {"label": ASSERT_TYPE_VERIFY_REGION, "value": ASSERT_TYPE_VERIFY_REGION}
]


# endregion

def get_assertion_folder(selected_node):
    directory = os.path.join(
        os.path.split(os.path.abspath(os.getcwd()))[0],
        "running_logs", f"ASSERTIONS/{selected_node}"
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_assertion_file_path(selected_node):
    return f"{get_assertion_folder(selected_node)}/{selected_node}.json"


def save_assertion(place_name, assertions):
    with open(get_assertion_file_path(place_name), "w") as fp:
        fp.write(json.dumps(assertions, indent=2))


def get_assertions_from_file(selected_node):
    if selected_node is None:
        return []
    file = get_assertion_file_path(selected_node)
    assertions = []
    if os.path.exists(file):
        with open(file, "rb") as fp:
            assertions = json.load(fp)
    return assertions


def create_attributes_dropdown(tag_type, attributes):
    dropdown = []
    for index, item in enumerate(attributes):
        key = item.get("key", "")
        value = item.get("value", "")
        dropdown.append(dbc.DropdownMenuItem(
            [
                html.B(str(key)), html.Br(),
                html.Div(
                    str(value),
                    style={"overflow": "hidden"}
                )
            ], n_clicks=0, id={
                "type": tag_type,
                "index": index
            }
        ))
        dropdown.append(dbc.DropdownMenuItem(divider=True))
    return dropdown


def create_assertions_header():
    return dbc.Row(
        children=[
            dbc.Col("Type", className="assert-cell-header", md=4),
            dbc.Col("Object", className="assert-cell-header", md=4),
            dbc.Col("Value", className="assert-cell-header", md=4)
        ],
        className="assert-row-header"
    )


def create_assertion_tab_footer(delete_id, save_id, more_id=None, id_add=None):
    buttons = [
        dbc.Button(
            icon_assertion_delete(), id=delete_id, n_clicks=0, disabled=True,
            style={"float": "left"}, outline=True, color="primary", size="sm", className="me-1"
        ),
        dbc.Button(
            icon_assertion_save(), id=save_id, n_clicks=0, style={"float": "right"},
            color="primary", size="sm", className="me-1"
        )
    ]

    if more_id is not None:
        buttons.insert(1, dbc.Button(
            html.Span([html.I(className="bi bi-arrows-fullscreen"), "  More"]),
            id=more_id, target="_blank", external_link=True,
            color="success", size="sm", className="me-1", style={"float": "right"}
        ))
    if id_add is not None:
        buttons.insert(0,
                       dbc.Button(
                           icon_assertion_add(), id=id_add, style={"float": "left"},
                           outline=True, color="primary", size="sm", className="me-1")
                       )
    return dbc.CardFooter(buttons)


def create_assertion_tab():
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    create_assertions_header(),
                    html.Div(
                        id="id-assertion-table-view", children=[],
                        style={"height": "500px", "maxHeight": "500px", "overflowY": "scroll"}),
                ]
            ),
            create_assertion_tab_footer(
                "id-button-assertion-delete",
                "id-button-assertion-save",
                "id-button-add-more",
                "id-button-assertion-add"
            )
        ], className="mt-3"
    )


def create_default_assertion(selected_node, next_key):
    return {
        "key": str(next_key),
        "id": selected_node,
        "ui_display": None,
        "assertion_type": "verifyElementVisible",
        "object_uuid": None,
        "data": None
    }


def append_new_region_assertion(selected_node, existing_assertions, shape, image_file):
    if image_file is not None:
        next_key = len(existing_assertions) + 1
        new_assertion = create_default_assertion(selected_node, next_key)
        new_assertion['data'] = image_file
        new_assertion['shape'] = shape
        new_assertion['assertion_type'] = ASSERT_TYPE_VERIFY_REGION
        new_assertion['ui_display'] = DOM_OBJECT
        existing_assertions.append(new_assertion)


def append_new_assertion(selected_node, existing_assertions, element_objects):
    if len(element_objects) > 0:
        next_key = len(existing_assertions) + 1
        for element_object in element_objects:
            new_assertion = create_default_assertion(selected_node, next_key)
            existing_assertions.append(new_assertion)
            key = next_key - 1
            on_object_selected(element_object['object'], key, existing_assertions)
            next_key = next_key + 1


def on_handle_button_add(selected_node, existing_assertions):
    if existing_assertions is None:
        return [create_default_assertion(selected_node, 1)]
    else:
        next_key = len(existing_assertions) + 1
        existing_assertions.append(create_default_assertion(selected_node, next_key))
        return existing_assertions


def delete_latest_assertion(existing_assertions):
    if existing_assertions is not None and len(existing_assertions) > 0:
        existing_assertions.pop()


def create_attributes_value_filter(element):
    attributes = []
    for key in element.keys():
        if element[key] is not None:
            attributes.append({"key": key, "ui_display": element[key]})
    if len(attributes) == 0:
        return "Attribute;Value"
    else:
        return attributes


def create_attributes_filter(element):
    attributes = []
    for key in element.keys():
        if element[key] is not None:
            attributes.append({"key": key})
    if len(attributes) == 0:
        return "Attribute"
    else:
        return attributes


def on_object_selected(element_object, index, existing_assertions):
    try:
        assertion_type = existing_assertions[index]["assertion_type"]
        on_assertion_type_changed(existing_assertions, index, assertion_type)
        existing_assertions[index]["object_uuid"] = element_object["uuid"]
        existing_assertions[index]["ui_display"] = create_element_display(element_object)
    except Exception as e:
        logger.debug(str(e))
    return existing_assertions


def on_assertion_type_changed(existing_assertions, index, assertion_type):
    existing_assertions[index]["assertion_type"] = assertion_type
    if assertion_type == ASSERT_TYPE_VERIFY_ELEMENT_ATTRIBUTE:
        """verifyElementAttributeValue"""
        existing_assertions[index]["data"] = "<attr>;<expected_value>"  # create_attributes_value_filter(element)
    elif assertion_type == ASSERT_TYPE_VERIFY_ELEMENT_HAS_ATTRIBUTE:
        """verifyElementHasAttribute"""
        existing_assertions[index]["data"] = "<attr>"  # create_attributes_filter(element)
    elif assertion_type == ASSERT_TYPE_VERIFY_ELEMENT_VISIBLE:
        """verifyElementVisible"""
        existing_assertions[index]["ui_display"] = ""
        existing_assertions[index]["data"] = "--- do not enter ---"
    elif assertion_type == ASSERT_TYPE_VERIFY_TEXT_PRESENT:
        """verifyTextPresent"""
        existing_assertions[index]["ui_display"] = DOM_OBJECT
        existing_assertions[index]["data"] = "<text_data>"
    elif assertion_type == ASSERT_TYPE_VERIFY_REGION:
        """verifyRegion"""
        existing_assertions[index]["ui_display"] = DOM_OBJECT
        existing_assertions[index]["data"] = None
    else:
        existing_assertions[index]["data"] = ""
    return existing_assertions


#
# def on_handle_attribute_dropdown(selected_assertion_index, dropdown_index, existing_assertions):
#     items = existing_assertions[selected_assertion_index - 1][ASSERTIONS_ATTRIBUTES_VALUE]
#     key = items[dropdown_index].get("key", "")
#     value = items[dropdown_index].get("value", None)
#     display = f"{key};{value}"
#     if value is None:
#         display = f"{key}"
#     existing_assertions[selected_assertion_index - 1][ASSERTIONS_DESIRED_VALUE] = display
#     return existing_assertions


def create_assertion_types_view(group_id, assertion):
    return dbc.Col(
        create_dropdown(
            id={
                "type": group_id,
                "index": assertion["key"]
            },
            value=assertion["assertion_type"],
            options=ASSERTIONS_TYPES
        ), md=4, className="assert-cell"
    )


def create_assertion_objects_view(group_id, assertion):
    ui_display = assertion.get("ui_display", None)
    key = assertion["key"]
    view_id = {"type": group_id, "index": key}
    if ui_display is None:
        ui_display = [icon_element_selected(view_id)]
    elif isinstance(ui_display, str):
        if ui_display == DOM_OBJECT:
            ui_display = [html.Div(ui_display)]
        else:
            ui_display = [icon_element_selected(view_id), html.Div(ui_display)]
    else:
        ui_display.insert(0, icon_element_selected(view_id))
    return dbc.Col(
        children=ui_display,
        md=4, style={"cursor": "pointer"}, className="assert-cell"
    )


def create_attributes_input(group_id, assertion):
    # Show region
    if assertion["assertion_type"] == ASSERT_TYPE_VERIFY_REGION:
        file_name = assertion['data']
        if file_name is not None:
            place_id = assertion['id']
            absolute_path = f"{get_assertion_folder(place_id)}/{file_name}"
            if os.path.exists(absolute_path):
                return dbc.Col(html.Img(
                    src=Image.open(absolute_path), style={"height": "32px"}),
                    className="assert-cell", md=3
                )
        return dbc.Col(md=4)
    else:
        data = assertion["data"]
        return dbc.Input(
            id={
                "type": group_id,  # TYPE_ASSERTIONS_INPUTS,
                "index": assertion["key"]
            },
            placeholder=str(data or ""),
            value=data,
            type="text",
            disabled=True if data is None else False,
            style={"display": "none"} if data is None else {}
        )


def create_assertion_attributes_view(group_id, assertion):
    # if isinstance(attributes, list):
    #     return dbc.InputGroup(
    #         [
    #             create_attributes_input(key, input_value),
    #             # dbc.DropdownMenu(
    #             #     create_attributes_dropdown(TYPE_ASSERTIONS_ATTRIBUTE, attributes),
    #             #     style={"width": "256px", "height": "256px"}
    #             # )
    #         ],
    #         id=ASSERTIONS_ATTRIBUTE
    #     )
    # else:
    if assertion["assertion_type"] not in ["verifyElementVisible"]:
        return dbc.Col(
            create_attributes_input(group_id, assertion),
            md=4, className="assert-cell")
    else:
        return dbc.Col(md=4)
