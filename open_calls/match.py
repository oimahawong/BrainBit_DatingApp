from flask import request, g, redirect

from app import matches
from tools.logging import logger

def handle_request():
    logger.debug("Display Matches Handle Request")
    
    # SQL database cursor
    cur = g.db.cursor()
    
    # Final version should fetch this from current user somehow
    userid = 2
    
    # Extract data for current user from database
    cur.execute("select name, email, img from users where id=?", (userid, ))
    thisname = cur.fetchone()[0]
    thisemail = cur.fetchone()[1]
    thisimg = cur.fetchone()[2]
    cur.execute("select path from images where id=?", (thisimg, ))
    thisimg = cur.fetchone()[0]
    
    # Determine current user's best match
    cur.execute(f"select id, match_{userid} from matches where match_{userid} = ( select max(match_{userid}) from matches );")
    matchid = cur.fetchone()[0]
    matchpercent = cur.fetchone()[1]
    # And fetch their data as well
    cur.execute("select name, email, img from users where id=?", (matchid, ))
    matchname = cur.fetchone()[0]
    matchemail = cur.fetchone()[1]
    matchimg = cur.fetchone()[2]
    cur.execute("select path from images where id=?", (matchimg, ))
    matchimg = cur.fetchone()[0]
    
    # Tuple contains: Name, email, profile pic path, (match percentage)
    userdata = thisname, thisemail, thisimg
    matchdata = matchname, matchemail, matchimg, matchpercent
    
    return matches(userdata=userdata, matchdata=matchdata)
