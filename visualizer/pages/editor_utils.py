#  Created by nphau on 12/29/22, 10:50 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 12/29/22, 10:50 AM

from components import assertions, screenshot, html_ids
import time
from PIL import ImageOps

TO_IMAGE_BUTTON_OPTIONS = {
    'format': 'jpeg',  # one of png, svg, jpeg, webp
    'height': 480,
    'width': 640,
    'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
}
MODE_BAR_BUTTONS_TO_ADD = ['drawrect', 'eraseshape']
MODE_BAR_BUTTONS_TO_REMOVE = ['zoom', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'toImage']


def timestamp():
    return int(time.time())


def crop_image(selected_image, place_id, x0, x1, y0, y1):
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = selected_image.size
    left = x0
    top = y0
    right = width - x1
    bottom = height - y1
    # Coordinate System
    border = (left, top, right, bottom)
    cropped_image = ImageOps.crop(selected_image, border)
    assertion_folder = assertions.get_assertion_folder(place_id)
    file_name = f'{place_id}_{timestamp()}.png'
    file_path = f'{assertion_folder}/{file_name}'
    cropped_image.save(file_path)
    return file_name
