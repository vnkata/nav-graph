import dash
import json
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, Input, State, html, ALL, ServersideOutput, Trigger
from dash import ctx, callback, no_update
from re import search
from dash.exceptions import PreventUpdate
import functools
# components
from components import graph, sidebar, canvas, toast, html_ids, sockets, \
    elements, header, screenshot, css, assertions, cache
from builder import builder, files
from loguru import logger


def title(graph_id=None):
    return f"{graph_id} Analysis"


dash.register_page(__name__, path_template="/graph/<graph_id>", path="/graph")


def layout(graph_id=None, **other_unknown_query_strings):
    return html.Div([
        toast.create_toast(html_ids.ID_TOAST),
        dbc.Container(
            children=[
                graph.create_graph_content(builder.load_graph(graph_id)),
                sidebar.create_sidebar_content(),
                elements.create_element_model(),
                canvas.create_graph_info(builder.metadata)
            ],
            id=html_ids.ID_APP_CONTENT, fluid=True
        )
    ])


@callback(
    Output(canvas.OFF_CANVAS_GRAPH_INFO, "is_open"),
    Input(graph.BUTTON_GRAPH_INFO, "n_clicks"),
    State(canvas.OFF_CANVAS_GRAPH_INFO, "is_open"),
    prevent_initial_call=True
)
def toggle_graph_info(n1, is_open):
    return not is_open if n1 else is_open


# @functools.lru_cache(maxsize=32)
@callback(
    [
        Output(sidebar.TAB_PROPERTIES, "disabled"),
        Output(sidebar.TAB_SCREENSHOT, "disabled"),
        Output(sidebar.TAB_ASSERTION, "disabled"),
        Output(html_ids.STORE_STARTED_NODE, "data"),
        Output(html_ids.STORE_PREV_SOCKET_STARTED_NODE, "data"),
        Output("id-button-add-more", "href"),
    ],
    [
        Input(html_ids.ID_GRAPH, "selected"),
        Input(html_ids.STORE_SOCKET_STARTED_NODE, "data"),
        Input(html_ids.STORE_PREV_SOCKET_STARTED_NODE, "data")
    ],
    background=True,
    prevent_initial_call=True,
    # manager=cache.long_callback_manager
)
def show_selected(selected_node, socket_node, last_socket_node):
    started_node = selected_node
    if type(socket_node) == str and socket_node != '':
        if socket_node != last_socket_node:
            started_node = socket_node
    if started_node is None:
        logger.debug("started_node is None")
        raise PreventUpdate
    try:
        data = builder.get_node_data(started_node)
        if data is None:
            logger.debug("data is None")
            raise PreventUpdate
        else:
            # logger.debug(f"data={data}")
            pass
        data['id'] = started_node
        # url = getattr(data, "screenshot", None)
        if hasattr(data, "assertions"):
            # data["assertions"] = None  # list(data["assertions"])
            pass
        if hasattr(data, "selectors"):
            pass
            # data["selectors"] = None  # list(data["selectors"])
        from_test_script = getattr(data, "from_test_script", False)
        return False, from_test_script, from_test_script, data, socket_node, f"/editor/{started_node}"
    except Exception as e:
        logger.error(e)
        raise PreventUpdate


@callback(
    Output(sidebar.BUTTON_PLAY_TO_HERE, "style"),
    Output(sidebar.BUTTON_PLAY_FROM_HERE, "style"),
    Input(html_ids.ID_GRAPH, "selected"),
    prevent_initial_call=True
)
def show_play_button(selected_node):
    if builder.is_place(selected_node):
        return css.float_right(), css.float_right()
    else:
        return css.display_none(), css.display_none()


@callback(
    ServersideOutput(html_ids.ID_SCREENSHOT, "children"),
    Input(html_ids.ID_GRAPH, "selected"),
    prevent_initial_call=True
)
def show_screenshot(place_id):
    return screenshot.create_screenshot_view(place_id)


@callback(
    Output(elements.ELEMENT_MODAL, "is_open"),
    Output(html_ids.STORE_CURRENT_ASSERTION_INDEX, "data"),
    Output(html_ids.STORE_ASSERTIONS, "data"),
    # When selected node
    Input(html_ids.ID_GRAPH, "selected"),
    # Click events
    Trigger("id-button-assertion-add", "n_clicks"),
    Input("id-button-assertion-delete", "n_clicks"),
    Input(elements.ELEMENT_BUTTON_OK, "n_clicks"),
    Input({"type": assertions.TYPE_ASSERTIONS_OBJECT, "index": ALL}, "n_clicks"),
    # Input({"type": assertions.TYPE_ASSERTIONS_ATTRIBUTE, "index": ALL}, "n_clicks"),
    # assertion types changed
    Input({"type": assertions.TYPE_ASSERTIONS_TYPES, "index": ALL}, "value"),
    # assertion input changed
    Input({"type": assertions.TYPE_ASSERTIONS_INPUTS, "index": ALL}, "value"),
    # Data from memory
    State(elements.ELEMENT_SELECTED_OBJECT, "children"),
    State(html_ids.STORE_ASSERTIONS, "data"),
    State(html_ids.STORE_CURRENT_ASSERTION_INDEX, "data"),
    prevent_initial_call=True
)
def on_assertion_actions_clicked(selected_node,
                                 add_clicks, delete_clicked, ele_ok_clicks, assert_objects_clicked,
                                 # assertion_attributes,
                                 assertion_types, assertion_new_inputs,
                                 selected_element_object, existing_assertions, existing_selected_index):
    triggered_id = ctx.triggered_id
    if triggered_id is None:
        raise PreventUpdate
    """ Reload assertions from files """
    if triggered_id == html_ids.ID_GRAPH:
        updated_assertions = assertions.get_assertions_from_file(selected_node)
        return no_update, no_update, updated_assertions
    """ When users click ADD assertion """
    if triggered_id == "id-button-assertion-add":
        if add_clicks is not None:
            updated_assertions = assertions.on_handle_button_add(selected_node, existing_assertions)
            return no_update, no_update, updated_assertions
        else:
            raise PreventUpdate
    """ When users click DELETE assertion """
    if triggered_id == "id-button-assertion-delete" and delete_clicked is not None:
        assertions.delete_latest_assertion(existing_assertions)
        return no_update, no_update, existing_assertions
    """ When users click OK in ElementsDialog """
    if triggered_id == html_ids.ELEMENT_BUTTON_OK:
        selected_index = int(existing_selected_index)
        # Combine between [json] and [props]
        element_object = selected_element_object['props']['data']
        updated_assertions = assertions.on_object_selected(
            element_object,
            selected_index - 1,
            existing_assertions
        )
        return False, no_update, updated_assertions
    else:
        current_type = triggered_id.get("type", None)
        current_key = triggered_id.get("index", -1)
        """ When users start to select object from assertions """
        if current_type == assertions.TYPE_ASSERTIONS_OBJECT:
            for index, value in enumerate(assertion_types):
                existing_assertions[index]["assertion_type"] = value
            return True, current_key, existing_assertions
        """ When users select attribute from assertions """
        # if current_type == assertions.TYPE_ASSERTIONS_ATTRIBUTE:
        #     selected_index = int(existing_selected_index)
        #     updated_assertions = assertions.on_handle_attribute_dropdown(
        #         selected_index, current_key, existing_assertions
        #     )
        #     return False, existing_selected_index, updated_assertions
        """ When users start to select type from assertions """
        if current_type == assertions.TYPE_ASSERTIONS_TYPES:
            idx = int(current_key) - 1
            assertion_type = ctx.triggered[0]['value']
            assertions.on_assertion_type_changed(existing_assertions, idx, assertion_type)
            return no_update, no_update, existing_assertions
        if current_type == assertions.TYPE_ASSERTIONS_INPUTS:
            idx = int(current_key) - 1
            existing_assertions[idx]["data"] = ctx.triggered[0]['value']
            return no_update, no_update, existing_assertions
        else:
            raise PreventUpdate


@callback(
    [
        Output("id-assertion-table-view", "children"),
        Output("id-button-assertion-delete", "disabled"),
        Output("id-button-assertion-add", "disabled")
    ],
    [
        Input("store-current-assertions", "data")
    ],
    prevent_initial_call=True
)
def on_assertion_changed(new_assertions):
    # if len(new_assertions) > 0:
    #     is_add_button_disable = new_assertions[len(new_assertions) - 1][html_ids.ASSERTIONS_OBJECT] is None
    views = []
    for assertion_index, item in enumerate(new_assertions):
        views.append(
            dbc.Row(
                [
                    assertions.create_assertion_types_view(assertions.TYPE_ASSERTIONS_TYPES, item),
                    assertions.create_assertion_objects_view(assertions.TYPE_ASSERTIONS_OBJECT, item),
                    assertions.create_assertion_attributes_view(assertions.TYPE_ASSERTIONS_INPUTS, item)
                ], className=css.get_row_style(assertion_index)
            )
        )
    return views, len(new_assertions) <= 0, False  # , is_add_button_disable


@callback(
    Output(elements.ELEMENT_MODEL_TITLE, "children"),
    ServersideOutput(elements.ELEMENT_RESULT, "children"),
    ServersideOutput(html_ids.STORE_UUID_FILES, "data"),
    Input(elements.ELEMENT_MODAL, "is_open"),
    Input(elements.ELEMENT_SEARCH, "value"),
    State(html_ids.STORE_STARTED_NODE, "data"),
    prevent_initial_call=True
)
def on_element_modal_showed(is_open, keyword, selected_node):
    triggered_id = ctx.triggered_id
    if is_open:
        modal_title = selected_node.get("current_title", selected_node.get("text", ""))
        display = f"Test Object Input [{modal_title}]"
        uuid_files = files.get_all_objs(selected_node)
        if keyword is None:
            return display, list(map(elements.map_element, uuid_files.values())), json.dumps(uuid_files)
        else:
            result = []
            for file in uuid_files.values():
                name = file.get("accessible_name", "").lower()
                tag_name = file.get("tag_name", "").lower()
                if search(keyword.lower(), tag_name) or search(keyword.lower(), name):
                    result.append(file)
            return no_update, list(map(elements.map_element, result)), no_update
    else:
        raise PreventUpdate


@callback(
    ServersideOutput(elements.ELEMENT_SELECTED_OBJECT, "children"),
    ServersideOutput(elements.ELEMENT_ROW_PROPERTIES_TITLE, "children"),
    Input({"type": elements.ELEMENT_OBJECT, "index": ALL}, "n_clicks"),
    State(html_ids.STORE_UUID_FILES, "data"),
    prevent_initial_call=True
)
def on_element_clicked(ele_clicks, store_files):
    triggered_id = ctx.triggered_id
    current_type = triggered_id.get("type", None)
    if current_type == elements.ELEMENT_OBJECT:
        uuid = triggered_id.get("index", None)
        content = files.get_json_by_uuid(store_files, uuid)
        element_json, element_title = elements.get_element_json_theme(content)
        return element_json, element_title
    else:
        raise PreventUpdate


@callback(
    Output(sockets.WS_INPUT, "value"),
    ServersideOutput(html_ids.ID_TOAST, "is_open"),
    Input(sidebar.BUTTON_PLAY_TO_HERE, "n_clicks"),
    Input(sidebar.BUTTON_PLAY_FROM_HERE, "n_clicks"),
    Input(graph.BUTTON_RUN_ALL, "n_clicks"),
    Input("id-button-assertion-save", "n_clicks"),
    State(html_ids.STORE_STARTED_NODE, "data"),
    State(html_ids.STORE_ASSERTIONS, "data"),
    prevent_initial_call=True
)
def on_play_button_clicked(play_to_here_clicks, play_from_here_clicks, run_all_here_clicks, send_clicks,
                           selected_node, existing_assertions):
    triggered_id = ctx.triggered_id
    if triggered_id is None:
        raise PreventUpdate
    if triggered_id == sidebar.BUTTON_PLAY_TO_HERE and play_to_here_clicks > 0:
        return sockets.create_play_to_here_event(selected_node["id"]), True
    elif triggered_id == sidebar.BUTTON_PLAY_FROM_HERE and play_from_here_clicks > 0:
        return sockets.create_play_from_here_event(selected_node["id"]), True
    elif triggered_id == graph.BUTTON_RUN_ALL:
        if run_all_here_clicks > 0:
            return sockets.create_run_all(), True
        else:
            raise PreventUpdate
    elif triggered_id == "id-button-assertion-save" and send_clicks > 0:
        place_name = selected_node["id"]
        assertions.save_assertion(place_name, existing_assertions)
        event = sockets.create_assertion_event({
            "place": place_name,
            "assertions": existing_assertions
        })
        return event, True
    else:
        raise PreventUpdate
