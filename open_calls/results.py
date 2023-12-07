from flask import request, g, redirect

from app import results
from tools.logging import logger

def handle_request():
    logger.debug("Display Matches Handle Request")
    
    # SQL database cursor
    cur = g.db.cursor()
    
    # Fetch ID from current user
    userid = request.form['userid']
    
    # Extract data for current user from database
    cur.execute("select name, email, img from users where id=?", (userid, ))
    thisuser = cur.fetchone()
    cur.execute("select path from images where id=?", (thisuser[2], ))
    thisimg = f"static/images/{cur.fetchone()[0]}"
    
    # Determine current user's best match
    cur.execute(f"select id, match_{userid} from matches where match_{userid} = ( select max(match_{userid}) from matches );")
    match = cur.fetchone()
    # And fetch their data as well
    cur.execute("select name, email, img from users where id=?", (match[0], ))
    thatuser = cur.fetchone()
    cur.execute("select path from images where id=?", (thatuser[2], ))
    thatimg = f"static/images/{cur.fetchone()[0]}"
    
    # Tuple contains: Name, email, profile pic path, (match percentage)
    userdata = thisuser[0], thisuser[1], thisimg
    matchdata = thatuser[0], thatuser[1], thatimg, match[1]
    
    return results(userdata=userdata, matchdata=matchdata)
