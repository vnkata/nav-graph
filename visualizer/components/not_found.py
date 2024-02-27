#  Created by nphau on 12/29/22, 9:15 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 12/29/22, 9:15 AM

from dash import html
import dash_bootstrap_components as dbc


def create_404_content():
    return html.Div(
        [
            html.H1("404", style={"fontWeight": "bold"}),
            html.P([
                html.Span("Opps! ", style={"color": "red"}),
                "Page not found."
            ]),
            html.P("The page you’re looking for doesn’t exist."),
            dbc.Col(
                dbc.Button("Go Home", color="primary", href="/")
            )
        ], style={"textAlign": "center", "marginTop": "96px"}
    )
