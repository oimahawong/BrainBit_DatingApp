from flask import request, g

from app import video, signup
from tools.logging import logger
from re import match

def handle_request():
    logger.debug("Signup Handle Request")
    
    # Pull user name and email from the signup form
    name_from_form = request.form['name']
    email_from_form = request.form['email']
    
    # Retrieve a cursor for the app database
    cur = g.db.cursor()
      
    # Validate email address
    if not match(r"[^@]+@[^@]+\.[^@]+", email_from_form):
      logger.debug("Invalid email!")
      return signup(error=1)
    
    # Check for duplicate usernames
    cur.execute("select count(1) from users where name = ?", (name_from_form, ))
    if cur.fetchone()[0] == 1:
      logger.debug("Duplicate user!")
      return signup(error=2)
    
    # Check for duplicate email addresses
    cur.execute("select count(1) from users where email = ?", (email_from_form, ))
    if cur.fetchone()[0] == 1:
      logger.debug("Duplicate email!")
      return signup(error=3)
    
    # Determine a user ID for the new user
    cur.execute("select max(id) from users")
    id_num = cur.fetchone()[0] + 1
    
    # Select a default profile image for the new user
    img_num = id_num % 10
    
    # Insert the new user's ID, name, email, and profile image into the users table
    logger.debug(f"Creating user {name_from_form} with id {id_num} and email {email_from_form}")
    cur.execute("insert into users values (?, ?, ?, ?)", (id_num, name_from_form, email_from_form, img_num))
    
    # Create a new row and column in the in the matches table for the new user
    cur.execute("insert into matches (id) values (?)", (id_num, ))
    cur.execute(f"alter table matches add match_{id_num} int")
    g.db.commit()
    
    return video(username=name_from_form, userid=id_num)
