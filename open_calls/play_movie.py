from flask import request, g

from tools.logging import logger   
from neurosdk.cmn_types import *

import sys
import io

def handle_request():
    # If headband library is not installed or headband is not connected
    if 'hb' not in g or g.hb == None:
        return ["Play, no HB"]

    g.hb.exec_command(SensorCommand.CommandStartSignal)

    return ["Data Flowing"]

