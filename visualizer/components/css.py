#  Created by nphau on 9/15/22, 11:47 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:47 PM


def get_row_style(index):
    if index % 2 == 0:
        return "assert-row-even"
    else:
        return "assert-row-odd"


def float_right():
    return {"float": "right"}


def display_none():
    return {"display": "none"}