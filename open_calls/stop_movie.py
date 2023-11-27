from flask import request, g
from tools.logging import logger
from neurosdk.cmn_types import *
from tools.eeg import all_my_data
from tools.bucket import upload_to_bucket
import pickle


def handle_request():    
    # Placeholder, demonstrates that the proper user ID was received
    logger.debug(request.form['userid'])
    
    # If headband library is not installed or headband is not connected
    if 'hb' not in g or g.hb == None:
        return ["Stop, no HB"]

    g.hb.exec_command(SensorCommand.CommandStopSignal)
    with open('output_pickle.pkl', 'wb') as file:
        pickle.dump(all_my_data, file)

    bucket_name = 'brainbit_bucket'
    source_file_path = r'output.pkl'
    destination_blob_name = 'test2.txt'  # Name it will have in the bucket
    upload_to_bucket(bucket_name, source_file_path, destination_blob_name)



    return ["Data Ended"]
