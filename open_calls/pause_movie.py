from flask import request, g
from tools.logging import logger
from neurosdk.cmn_types import *



def handle_request():
    if g.hb == None:
        return ["Pause, no HB"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)

    return ["Data Paused"]