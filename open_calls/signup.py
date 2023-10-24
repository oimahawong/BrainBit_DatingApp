from flask import request, g

from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    
    # Pull user name and email from the signup form
    name_from_form = request.form['name']
    email_from_form = request.form['email']
    
    # Retrieve a cursor for the app database
    cur = g.db.cursor()
    
    # Insert the new user's name and email into the users table
    cur.execute("insert into users values ( 1, \"" + name_from_form + "\", \"" + email_from_form + "\" );")
    g.db.commit()
    
    return "Signup complete"
