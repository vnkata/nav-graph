#  Created by nphau on 9/15/22, 11:49 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:49 PM
import dash_bootstrap_components as dbc


def create_dropdown(**kwargs):
    return dbc.Select(**kwargs, style={"fontSize": "12px"})

