#  Created by nphau on 10/22/22, 7:48 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 10/22/22, 7:48 PM

import dash
from components import not_found

dash.register_page(__name__, path="/404", title='404')

layout = not_found.create_404_content()
