from flask import request, g
from tools.logging import logger
from neurosdk.cmn_types import *



def handle_request():
    # If headband library is not installed or headband is not connected
    if 'hb' not in g or g.hb == None:
        return ["Pause, no HB"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)

    return ["Data Paused"]
