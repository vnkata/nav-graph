#  Created by nphau on 11/12/22, 4:55 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/12/22, 4:55 PM
import base64


def encode_url(url):
    message_bytes = url.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


def decode_url(base64_message):
    if base64_message:
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('ascii')
    else:
        return ""
