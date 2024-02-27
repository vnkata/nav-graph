#  Created by nphau on 9/15/22, 11:16 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:16 PM

from dash_extensions.enrich import html
import dash_bootstrap_components as dbc


def create_header(dash_app):
    return dbc.Row(
        dbc.Col(
            [
                html.A(html.Img(src=dash_app.get_asset_url("hcmus.png")), href="/"),
                html.A(
                    html.Img(src=dash_app.get_asset_url("lyon.png"), style={"height": "32px"}),
                    href="/")
            ], md=12),
        className="app_banner"
    )
