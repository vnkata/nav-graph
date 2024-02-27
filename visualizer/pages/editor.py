#  Created by nphau on 10/22/22, 7:48 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 10/22/22, 7:48 PM
import dash
from dash_extensions.enrich import Output, Input, html, State, Trigger, ServersideOutput
from components import html_ids, screenshot, elements, icons, css, assertions, not_found, toast, sockets
import plotly.express as px
from skimage import io
from dash.exceptions import PreventUpdate
from dash import ctx, callback, no_update, dcc
from builder import builder, files
import dash_bootstrap_components as dbc
from loguru import logger
from dash import ctx, callback, no_update
from editor_utils import crop_image, TO_IMAGE_BUTTON_OPTIONS, MODE_BAR_BUTTONS_TO_ADD, MODE_BAR_BUTTONS_TO_REMOVE
from PIL import Image
import plotly.graph_objects as go

dash.register_page(__name__, path_template="/editor/<place_id>", path="/editor", title='Assertions')

ID_CACHE_PLACE_ID = "id_cache_place_id"
ID_IMAGE_GRAPH = "id_image_graph"
ID_IMAGE_GRAPH_DELETE = "id_image_graph_delete"
ID_IMAGE_GRAPH_SAVE = "id_image_graph_save"
ID_IMAGE_GRAPH_TYPES = "id_image_graph_types"
ID_IMAGE_GRAPH_ASSERTIONS = "id_image_graph_current_assertions"
ID_IMAGE_GRAPH_OBJECTS = "id_image_graph_objects"
ID_IMAGE_GRAPH_INPUTS = "id_image_graph_inputs"
ID_IMAGE_GRAPH_DESCRIPTION = "id_image_graph_description"
ID_IMAGE_GRAPH_TOAST = "id_image_graph_toast"

global selected_image


def layout(place_id=None, **other_unknown_query_strings):
    try:
        data = builder.get_node_data(place_id)
        url = data.get("screenshot", None)
        absolute_path = screenshot.get_screenshot_path(url)

        # Existing assertions
        existing_assertions = assertions.get_assertions_from_file(place_id)
        assertions_views, shapes = create_assertion_table_view(existing_assertions)

        # For crop purpose
        global selected_image
        selected_image = Image.open(absolute_path)

        # For display
        fig = px.imshow(io.imread(absolute_path), binary_backend="jpg")
        fig.update_layout(
            newshape_line_color=px.colors.qualitative.Light24[0],
            margin=dict(l=0, r=0, b=0, t=0, pad=4),
            dragmode="drawrect"
        )
        for shape in shapes:
            fig.add_shape(shape)

        return dbc.Container(
            children=[
                toast.create_toast(ID_IMAGE_GRAPH_TOAST, "Success"),
                dbc.Card(
                    id="graph-card",
                    children=[
                        dbc.CardBody(dcc.Graph(
                            id=ID_IMAGE_GRAPH, figure=fig, style={"height": "768px"},
                            config={
                                "scrollZoom": False, "displaylogo": False,
                                "toImageButtonOptions": TO_IMAGE_BUTTON_OPTIONS,
                                "modeBarButtonsToAdd": MODE_BAR_BUTTONS_TO_ADD,
                                "modeBarButtonsToRemove": MODE_BAR_BUTTONS_TO_REMOVE
                            },
                        ))
                    ]
                ),
                dbc.Card(
                    id=html_ids.ID_SIDE_BAR,
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col("Type", className="assert-cell-header", md=4),
                                dbc.Col("Object", className="assert-cell-header", md=4),
                                dbc.Col("Value", className="assert-cell-header", md=4)
                            ],
                            className="assert-row-header"
                        ),
                        dbc.CardBody(
                            assertions_views,
                            id=ID_IMAGE_GRAPH_DESCRIPTION,
                            style={"overflowY": "scroll", "height": "512px", "maxHeight": "512px"}
                        ),
                        assertions.create_assertion_tab_footer(
                            ID_IMAGE_GRAPH_DELETE,
                            ID_IMAGE_GRAPH_SAVE
                        )
                    ],
                    style={"marginLeft": "8px", "marginRight": "8px", "width": "50%"}
                ),
                dcc.Store(id=ID_CACHE_PLACE_ID, data=place_id),
                dcc.Store(id=ID_IMAGE_GRAPH_ASSERTIONS, data=existing_assertions),
            ],
            id=html_ids.ID_APP_CONTENT, fluid=True
        )
    except Exception as e:
        logger.error(e)
    return not_found.create_404_content()


def create_assertion_table_view(new_assertions):
    views = []
    shapes = []
    for assertion_index, item in enumerate(new_assertions):
        if 'shape' in item:
            shapes.append(item['shape'])
        views.append(dbc.Row(
            children=[
                assertions.create_assertion_types_view(ID_IMAGE_GRAPH_TYPES, item),
                assertions.create_assertion_objects_view(ID_IMAGE_GRAPH_OBJECTS, item),
                assertions.create_assertion_attributes_view(ID_IMAGE_GRAPH_INPUTS, item)
            ], className=css.get_row_style(assertion_index)
        ))
    return views, shapes


@callback(
    Output(ID_IMAGE_GRAPH_TOAST, "is_open"),
    ServersideOutput(ID_IMAGE_GRAPH_ASSERTIONS, "data"),
    ServersideOutput(ID_IMAGE_GRAPH_DESCRIPTION, "children"),
    Output(ID_IMAGE_GRAPH_DELETE, "disabled"),
    [
        Input(ID_IMAGE_GRAPH, "relayoutData"),
        Input(ID_IMAGE_GRAPH, "clickData"),
        Input(ID_IMAGE_GRAPH_DELETE, "n_clicks"),
        Input(ID_IMAGE_GRAPH_SAVE, "n_clicks")
    ],
    State(ID_CACHE_PLACE_ID, "data"),
    State(ID_IMAGE_GRAPH_ASSERTIONS, "data"),
    prevent_initial_call=True
)
def on_rect_selected(layout_data, click_data,
                     delete_clicks, save_clicks,
                     place_id, existing_assertions):
    triggered_id = ctx.triggered_id
    if triggered_id is None:
        raise PreventUpdate
    if triggered_id == ID_IMAGE_GRAPH:
        cb_context = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if cb_context == f"{ID_IMAGE_GRAPH}.relayoutData" and layout_data is not None:
            # If user draw any shapes
            if "shapes" in layout_data:
                # Get latest drawable
                shapes = layout_data["shapes"]
                if len(shapes) > 0:
                    shape = shapes[-1]
                    x0 = shape['x0']
                    y0 = shape['y0']
                    x1 = shape['x1']
                    y1 = shape['y1']
                    # Crop region
                    region_file_name = crop_image(selected_image, place_id, x0, x1, y0, y1)
                    assertions.append_new_region_assertion(place_id, existing_assertions, shape, region_file_name)
                    assertions_views, _ = create_assertion_table_view(existing_assertions)
                    return no_update, existing_assertions, assertions_views, len(existing_assertions) <= 0
            return no_update, no_update, no_update, len(existing_assertions) <= 0
        if click_data is not None and "points" in click_data:
            y = click_data["points"][0]["y"]
            x = click_data["points"][0]["x"]
            z = click_data["points"][0]["z"]
            selected_node = builder.get_node_data(place_id)
            element_objects = files.find_objects_by_position(selected_node, x, y, z)
            assertions.append_new_assertion(place_id, existing_assertions, element_objects)
            assertions_views, _ = create_assertion_table_view(existing_assertions)
            return no_update, existing_assertions, assertions_views, len(existing_assertions) <= 0
    if triggered_id == ID_IMAGE_GRAPH_SAVE:
        assertions.save_assertion(place_id, existing_assertions)
        return True, no_update, no_update, no_update
    if triggered_id == ID_IMAGE_GRAPH_DELETE:
        assertions.delete_latest_assertion(existing_assertions)
        assertions_views, _ = create_assertion_table_view(existing_assertions)
        return no_update, existing_assertions, assertions_views, len(existing_assertions) <= 0
    raise PreventUpdate

#
# @callback(
#     ServersideOutput(ID_IMAGE_GRAPH_DESCRIPTION, "children"),
#     Output(ID_IMAGE_GRAPH_DELETE, "disabled"),
#     Output(ID_IMAGE_GRAPH, "figure"),
#     Input(ID_IMAGE_GRAPH_ASSERTIONS, "data"),
#     State(ID_IMAGE_GRAPH, "figure"),
#     prevent_initial_call=True
# )
# def on_assertion_changed(new_assertions, figure):
#     triggered_id = ctx.triggered_id
#     if triggered_id is None:
#         raise PreventUpdate
#     assertions_views, shapes = create_assertion_table_view(new_assertions)
#     new_figure = go.Figure(figure)
#     new_figure['layout']['shapes'] = []
#     for shape in shapes:
#         new_figure.add_shape(shape)
#     return assertions_views, len(new_assertions) <= 0, no_update
