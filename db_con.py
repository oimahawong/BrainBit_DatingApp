#Use sqllite
import sqlite3

def get_db():
    return sqlite3.connect("users.sqlite3")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )
    return db, cur 

if __name__ == "__main__":
    db, cur = get_db_instance()

    # User data databse should include fields for User ID, name, and email
    cur.execute("create table users ( id int, name varchar(255), email varchar(255) );")
    db.commit()
