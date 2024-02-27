#  Created by nphau on 11/11/22, 1:36 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/11/22, 1:36 PM

import re

URL_PATTERN = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


def is_url_valid(url):
    return re.match(URL_PATTERN, url)
