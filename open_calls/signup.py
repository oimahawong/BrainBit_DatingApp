from flask import request, g, redirect

from app import video, signup
from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    
    # Pull user name and email from the signup form
    name_from_form = request.form['name']
    email_from_form = request.form['email']
    
    # Retrieve a cursor for the app database
    cur = g.db.cursor()
    
    # Check for duplicate email addresses
    cur.execute("select count(1) from users where email = ?", (email_from_form, ))
    if(cur.fetchone()[0] == 1):
      logger.debug("Duplicate user!")
      return signup(error=1)
    
    # Determine a user ID for the new user
    cur.execute("select max(id) from users")
    id_num = cur.fetchone()[0] + 1
    
    # Insert the new user's ID, name, and email into the users table
    logger.debug(f"Creating user {name_from_form} with id {id_num} and email {email_from_form}")
    cur.execute("insert into users values (?, ?, ?)", (id_num, name_from_form, email_from_form))
    g.db.commit()
    
    return video(username=name_from_form, userid=id_num)
