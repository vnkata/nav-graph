#  Created by nphau on 9/15/22, 11:25 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 9:01 PM

from pathlib import Path
import dash_bootstrap_components as dbc
from dash import callback
import html_ids
from dash_extensions.enrich import Output, Input, html, ServersideOutput
from loguru import logger
from PIL import Image
from builder import builder, files


def get_screenshot_path(url):
    return f"{Path(__file__).parent.parent.parent}/{url}"


#
#
# @callback(
#     ServersideOutput(html_ids.ID_SCREENSHOT, "children"),
#     Input(html_ids.ID_GRAPH, "selected"),
#     prevent_initial_call=True
# )
def create_screenshot_view(place_id):
    try:
        data = builder.get_node_data(place_id)
        url = data.get("screenshot", None)
        absolute_path = get_screenshot_path(url)
        return html.Div(
            [
                dbc.Button(
                    html.Span(
                        ["Click on the image below to add more assertions   ",
                         html.I(className="bi bi-arrows-fullscreen")]),
                    href=f"/editor/{place_id}", target="_blank", external_link=True,
                    outline=True, color="danger", size="sm", className="me-1",
                    style={"marginTop": "8px", "marginLeft": "32px", "marginRight": "32px", "display": "block"}
                ),
                html.A(
                    html.Img(
                        src=Image.open(absolute_path),
                        style={"objectFit": "contain", "objectPosition": "center", "marginTop": "12px",
                               "width": "90%", "height": "auto", "cursor": "pointer"}
                    ),
                    href=f"/editor/{place_id}", target="_blank"
                )
            ]
        )
    except Exception as e:
        logger.error(e)
    return html.Br()
