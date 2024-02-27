#  Created by nphau on 9/26/22, 11:36 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/26/22, 11:36 PM

import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
import datetime


def create_footer():
    today = datetime.date.today()
    year = today.year
    return dbc.Row([
        dbc.Col(f"20C14003 | Nguyen Phuc Hau © {year}", width=10, align="center"),
        dbc.Col(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(
                        html.A(html.I(className="bi bi-github"), href='https://github.com/nphausg',
                               target="_blank"),
                        className="none"
                    ),
                    dbc.ListGroupItem(
                        html.A(html.I(className="bi bi-twitter"), href='https://twitter.com/nphausg',
                               target="_blank"),
                        className="none"
                    )
                ],
                horizontal=True, flush=True,
                className="mb-2", style={"float": "right"}
            ),
            width=2, align="center"
        )
    ], className="footer", align="center")
