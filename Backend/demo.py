import psycopg2
import base64
import binascii
from datetime import datetime

ONLINE_DATABASE = "DBMS-mini-project"
ONLINE_OUSERNAME = "dr.king.svit"
ONLINE_PASSWORD = "3A9zPvNGJdxI"
ONLINE_HOST = "ep-white-dust-a1evatup.ap-southeast-1.aws.neon.tech"
ONLINE_PORT = "5432"


conn = psycopg2.connect(
    database = ONLINE_DATABASE, 
    user = ONLINE_OUSERNAME, 
    password = ONLINE_PASSWORD, 
    host = ONLINE_HOST, 
    port = ONLINE_PORT
)
print(conn)
cur = conn.cursor()

def getPhoto(url):
    with open(url, 'rb') as file:
        binary_data = file.read()
    return binascii.hexlify(binary_data).decode("utf-8")


def binaryFromPhotoObject(obj):
    return binascii.hexlify(obj.read()).decode("utf-8")

def newUser(username, loc, bio, mailid, website, fname, lname, photo, dob, password=0):
    joined_from = datetime.today().strftime('%Y-%m-%d')
    cur.execute("insert into users values ('{username}', '{loc}', '{bio}', '{mailid}', '{website}', '{fname}', '{lname}', decode('{photo}', 'hex') , '{dob}','{joined_from}', '{password}')".format())
    print(password)
    conn.commit()

def deleteUser(username):
    query = "delete from users where username = {username}".format()
    cur.execute(query)
    conn.commit()

def newLike(tweet_id, user_id):
    query = "insert into like (tweet_id, user_id) values ({}, {})".format(tweet_id, user_id)
    cur.execute(query)
    conn.commit()

def newComment(tweet_id, user_id, content):
    query = "insert into comments (tweet_id, user_id, content) values ({}, {}, {})".format(tweet_id, user_id, content)
    cur.execute(query)
    conn.commit()


def newFollow(follower, followee):
    query = "insert into followers (follower, followee) values ({}, {})".format(follower, followee)
    cur.execute(query)
    conn.commit()

def newUnlike(tweet_id, user_id):
    query = "delete from like where tweet_id = {} and user_id = {}".format(tweet_id, user_id)
    cur.execute(query)
    conn.commit()


if __name__ == "__main__":

    values = {
        "username" : "actorvijay2",
        "loc" : "Chennai",
        "bio" : "Actor, Singer, Dancer",
        "mailid" : "actorvijay@tweeter.com",
        "website" : "www.actorvijay.com",
        "fname" : "Joseph",
        "lname" : "Vijay",
        "photo" : getPhoto("C:\\Users\\akash\\OneDrive\\Pictures\\akash.jpg"),
        "dob" : "2022-05-02",
        "joined_from" : datetime.today().strftime('%Y-%m-%d'),
        "password" : "a"
    }

    cur.execute("insert into users values ('{username}', '{loc}', '{bio}', '{mailid}', '{website}', '{fname}', '{lname}', decode('{photo}', 'hex') , '{dob}', '{joined_from}')".format(**values))

    conn.commit()
    conn.close()