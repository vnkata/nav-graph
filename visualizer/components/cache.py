#  Created by nphau on 11/12/22, 10:04 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/12/22, 10:04 AM
import diskcache
from uuid import uuid4
from dash.long_callback import DiskcacheLongCallbackManager
cache = diskcache.Cache('./cache')
launch_uid = uuid4()
long_callback_manager = DiskcacheLongCallbackManager(
    cache, cache_by=[lambda: launch_uid], expire=60,
)