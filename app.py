from flask import Flask, render_template, request, redirect, url_for, g, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.eeg import all_my_data
import jwt

import sys
import datetime
import traceback

try: 
    from tools.eeg import get_head_band_sensor_object
    hb_imported = True
except: 
    hb_imported = False

from db_con import get_db_instance, get_db

from tools.logging import logger

ERROR_MSG = "Ooops.. Didn't work!"


#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)

#g is flask for a global var storage 
def init_new_env():
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()

    if hb_imported:
      if 'hb' not in g:
        g.hb = get_head_band_sensor_object()
    else:
      logger.debug(f"WARNING: Running without neurosdk")
      
    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    return render_template('index.html')

# Another redirect to the page containing the movie itself    
@app.route('/video')
def video(username="Guest", userid=0):
    return render_template('video.html', username=username, userid=userid)

@app.route('/signup')
def signup(error=0):
    return render_template('signup.html', error=error)

@app.route('/results')
def results(userdata=(), matchdata=()):
    return render_template('results.html', userdata=userdata, matchdata=matchdata)

@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")

    #setup the env
    init_new_env()

    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)

    return resp

@app.route('/log-timestamp', methods=['POST'])
def log_timestamp():
    data = request.json
    time = data['time']
    clip = data['clip']

    logger.debug(f"Timestamp Logged: {time} - {clip}")
    all_my_data.append(f"Timestamp Logged: {time} - {clip}")

    return jsonify({'status': 'success', 'message': 'Timestamp logged'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

