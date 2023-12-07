#Use sqllite
import sqlite3
from sys import argv

def get_db():
    return sqlite3.connect("users.sqlite3")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )
    return db, cur 

if __name__ == "__main__":
    db, cur = get_db_instance()

    # User table should include fields for user ID, name, email, and profile image
    cur.execute("create table users ( id int not null, name varchar(255), email varchar(255), img int );")
    # Also create a dummy user at ID 0 to keep the table from being called while empty
    cur.execute("insert into users values (0, null, null, null);")
    
    # Matches table should include field for user IDs
    # As users are added, more fields will be added to store each user pair's match percentage
    cur.execute("create table matches ( id int not null );")
    
    # Finally create a table to store profile images
    cur.execute("create table images ( id int not null, path varchar(255) );")
    # The first ten entires are reserved for the placeholder set
    for i in range(10):
      imgpath = f"profiles/{i}.png"
      cur.execute("insert into images values( ?, ? )", (i, imgpath))
    
    if len(argv) > 1 and argv[1] == "full":
      cur.execute("insert into users values (1, \"user1\", \"soulfinders.match@gmail.com\", 1)")
      cur.execute("insert into matches (id) values (1)")
      cur.execute("alter table matches add match_1 int")
      
      cur.execute("insert into users values (2, \"user2\", \"soulfinders.match@gmail.com\", 2)")
      cur.execute("insert into matches (id) values (2)")
      cur.execute("alter table matches add match_2 int")
      
      cur.execute("insert into users values (3, \"user3\", \"soulfinders.match@gmail.com\", 3)")
      cur.execute("insert into matches (id) values (3)")
      cur.execute("alter table matches add match_3 int")
      
      cur.execute("insert into users values (4, \"user4\", \"soulfinders.match@gmail.com\", 4)")
      cur.execute("insert into matches (id) values (4)")
      cur.execute("alter table matches add match_4 int")
      
    db.commit()
