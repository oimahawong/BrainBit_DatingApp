from flask import request, g, redirect

from app import results, video
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
    # If no valid user is found e.g. because page was loaded as guest, direct back to video page
    if thisuser is None or thisuser[0] is None:
        return video(username="Guest", userid=0)
    cur.execute("select path from images where id=?", (thisuser[2], ))
    thisimg = f"static/images/{cur.fetchone()[0]}"
    
    # Determine current user's best match
    cur.execute(f"select id, match_{userid} from matches where match_{userid} = ( select max(match_{userid}) from matches );")
    match = cur.fetchone()
    # If no match is found e.g. because matches have not been recalculated yet, direct back to video page
    if match is None:
        return video(username=thisuser[0], userid=userid)
    # Else, fetch their data as well
    cur.execute("select name, email, img from users where id=?", (match[0], ))
    thatuser = cur.fetchone()
    cur.execute("select path from images where id=?", (thatuser[2], ))
    thatimg = f"static/images/{cur.fetchone()[0]}"
    
    # Tuple contains: Name, email, profile pic path, (match percentage)
    userdata = thisuser[0], thisuser[1], thisimg
    matchdata = thatuser[0], thatuser[1], thatimg, match[1]
    
    return results(userdata=userdata, matchdata=matchdata)
