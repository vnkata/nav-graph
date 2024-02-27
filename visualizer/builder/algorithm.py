#  Created by nphau on 12/22/22, 11:14 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 12/22/22, 11:14 AM


def is_point_inside_rect(cmp_x, cmp_y, x0, x1, y0, y1):
    return x0 <= cmp_x <= x1 and y0 <= cmp_y <= y1


# Returns true if `a` contains `b`
# (x1, y1) and (x2, y2) are top-left and bottom-right corners
def compare_rects(x0, x1, y0, y1, cmp_x0, cmp_x1, cmp_y0, cmp_y1):
    return x0 <= cmp_x0 and y0 <= cmp_y0 and x1 >= cmp_x1 and y1 >= cmp_y1
