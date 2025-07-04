from flask import *
from chat import *
from flask_cors import CORS, cross_origin
from demo import *
from functions import *
#from embeddedsql import *
import codecs
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'

'''Prelims'''


@app.route('/', methods=['GET'])
def home():
    return '''
    Available methods are :

    GET Requests:
    /
    /feed
    /:user
    /:tweet_id

    POST Requests:
    /new_user
    /new_tweet
    /new_user_2
    /new_comment
    /new_follow
    /new_like
    '''

ONLINE_DATABASE = "DBMS-mini-project"
ONLINE_OUSERNAME = "dr.king.svit"
ONLINE_PASSWORD = "3A9zPvNGJdxI"
ONLINE_HOST = "ep-white-dust-a1evatup.ap-southeast-1.aws.neon.tech"
ONLINE_PORT = "5432"

@app.route('/user/<user>', methods=['GET'])
def user(user):
    conn = psycopg2.connect(
        database = ONLINE_DATABASE,
        user = ONLINE_OUSERNAME,
        password = ONLINE_PASSWORD,
        host = ONLINE_HOST,
        port = ONLINE_PORT
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "select * from users where username = '{}'".format(user)
    cur.execute(query)
    data = [dict(i) for i in cur.fetchall()]
    d = {}
    d['profile'] = data[0]

    query = '''
    select users.username, (users.fname || ' ' || users.lname) as author, users.photo as userphoto, tweet.tweetid, tweet.content_, tweet.photo
    from tweet inner join users on
    tweet.author = users.username  and users.username = '{}'
    '''.format(user)
    cur.execute(query)
    data = cur.fetchall()
    data2 = [dict(i) for i in data]
    d['tweets'] = data2
    d['followers'] = getFollowersOf(user)
    conn.commit()
    conn.close()
    return jsonify(d)


@app.route('/delete_tweet/<tweet_id>', methods=['GET'])
def delete_tweet(tweet_id):
    print("to delete", tweet_id)
    deleteTweetById(tweet_id)
    return jsonify({"statjs": "deleted"})


@app.route('/feed/<user>')
# @cross_origin()
def feed(user):
    data = tweetFeed(user)
    # print(data[1])
    data2 = [dict(i) for i in data]
    return jsonify({"data": data2})


@app.route('/tweets_by_user/<username>')
def tweets_by_user(username):
    conn = psycopg2.connect(
        database=ONLINE_DATABASE,
        user=ONLINE_OUSERNAME,
        password=ONLINE_PASSWORD,
        host=ONLINE_HOST,
        port=ONLINE_PORT
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = '''
    select users.username, (users.fname || ' ' || users.lname) as author, users.photo as userphoto, tweet.tweetid, tweet.content_, tweet.photo
    from tweet inner join users on
    tweet.author = users.username  and users.username = '{}'
    '''.format(username)
    cur.execute(query)
    data = cur.fetchall()
    data2 = [dict(i) for i in data]
    conn.commit()
    conn.close()
    return jsonify(data2)


@app.route('/tweet/<tweetid>', methods=['GET'])
def tweet(tweetid):
    data = single_tweet(tweetid)
    return jsonify(data)


@app.route('/full_tweet/<tweetid>')
@cross_origin()
def full_tweet(tweetid):
    singletweet = single_tweet(tweetid)
    like_data = likesByTweeterId(tweetid)
    comment_data = commentsByTweetId(tweetid)
    liked_users = [i['username'] for i in like_data]
    data = {
        "tweet": singletweet,
        "likes": like_data,
        "comments": comment_data,
        "liked_users": liked_users
    }
    return jsonify(data)


@app.route('/groups/<group>', methods=['GET'])
def group_feed(group):
    data = request.data
    data['group'] = group
    return jsonify({"data": data})


@app.route('/chat', methods=['POST'])
def chat():
    data = dict(request.form)
    print(data)
    data['group'] = 'group'
    return jsonify({"data": data})


@app.route('/likes_by_tweeter_id/<tweet_id>', methods=['GET'])
def likes_by_tweeter_id(tweet_id):
    data = likesByTweeterId(tweet_id)
    return jsonify(data)


@app.route('/new_tweet', methods=['POST'])
@cross_origin()
def new_tweet():
    data = dict(request.form)
    files = request.files
    username = data['username']
    content = data['content']
    if 'photo' not in data:
        if 'photo' in dict(files):
            data['photo'] = dict(files)['photo']
        else:
            data['photo'] = ''
    if data['photo'] == '':
        photo = ''
    else:
        photo = hexToBase64(binaryFromPhotoObject(data["photo"]))
    # print(data)
    # print("image : ", photo[:20])
    newTweet(username, content, photo)
    return jsonify(data)


'''User Table'''


@app.route('/new_user', methods=['POST'])
def new_user():
    data = request.form
    files = request.files
    if "image" not in dict(files):
        out['image'] = ''
    else:
        image = hexToBase64(binaryFromPhotoObject(dict(files)["image"]))
        # print(binaryFromPhotoObject(dict(files)["image"])[:20])
        # username, loc, bio, mailid, website, fname, lname, photo, dob
        out = data.copy()
        out['image'] = image
 
    newUser(**out)

    return redirect(url_for('home'))


@app.route('/new_user_2', methods=['POST'])
def new_user_2():
    data = request.form
    files = request.files
    out = data.copy()
    if "photo" not in dict(files):
        out['photo'] = ''
    else:
        image = hexToBase64(binaryFromPhotoObject(dict(files)["photo"]))
        # print(binaryFromPhotoObject(dict(files)["image"])[:20])
        # username, loc, bio, mailid, website, fname, lname, photo, dob,password
        out['photo'] = image
  
    newUser(**out)

    # print(hexToBase64(image))

    # newUser(**out)
    return jsonify(out)

# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     data = request.form
#     username = data['username']
#     return jsonify({"data":data})


@app.route('/change_photo', methods=['POST'])
def change_photo():
    data = request.form
    files = request.files
    user = data['username']
    image = binaryFromPhotoObject(dict(files)["image"])
    b64_image = hexToBase64(image)
    out = {
        'user': user,
        'image': image,
        "b64_image": b64_image
    }
    changePhoto(user, b64_image)
    return jsonify({"data": out})


'''Follower Table'''


@app.route('/new_follow')
def new_follow():
    data = dict(request.args)
    newFollow(data['curuser'], data['user'])
    return jsonify(data)


@app.route('/new_unfollow')
def new_unfollow():
    data = dict(request.args)
    newUnfollow(data['curuser'], data['user'])
    return jsonify(data)


@app.route('/is_following')
def is_following():
    data = dict(request.args)
    out = isFollowing(data['curuser'], data['user'])
    return jsonify({'is_following': out, 'curuser': data['curuser'], 'user': data['user']})


'''Like Table'''


@app.route("/new_like", methods=['POST'])
def new_like():
    data = dict(request.form)
    tweet_id = data['tweet_id']
    user_id = data['user_id']
    try:
        newLike(tweet_id, user_id)
        # print("Like data", data)
    except:
        print("Post already liked")
    return jsonify({"data": data})


@app.route("/new_unlike", methods=['POST'])
def new_unlike():
    data = request.form
    tweet_id = data['tweet_id']
    user_id = data['user_id']
    try:
        newUnlike(tweet_id, user_id)
    except:
        print("Post already disliked")
    return jsonify({"data": data})


'''Message Table'''


@app.route("/new_message", methods=['POST'])
def new_message():
    data = request.form
    sender = data['sender']
    receiver = data['receiver']
    content = data['message']
    data['time'] = 10
    return jsonify({"data": data})


@app.route("/delete_message", methods=['POST'])
def delete_message():
    data = request.form
    sender = data['sender']
    receiver = data['receiver']
    time = data['time']
    return jsonify({"data": data})


'''Group Member Table'''


@app.route('/new_group', methods=['POST'])
@cross_origin()
def new_group():
    print("new group")
    data = dict(request.form)
    out = data.copy()
    if "groupphoto" not in dict(request.files):
        out['photo'] = ''
    else:
        image = hexToBase64(binaryFromPhotoObject(
            dict(request.files)["groupphoto"]))
        out['photo'] = image
    try:
        newGroup(**out)
    except:
        print("group name exists")
    return jsonify(out)


@app.route('/new_group_member', methods=['POST'])
def new_group_member():
    data = request.form
    group_name = data['group_name']
    username = data['username']
    return jsonify({"data": data})


@app.route('/change_group_photo', methods=['POST'])
@cross_origin()
def change_group_photo():
    data = request.form
    files = request.files
    # print(list(files), list(data))
    groupname = data['groupname']
    # image = binaryFromPhotoObject(data["image"])
    # b64_image = hexToBase64(image)
    image = data["image"]
    b64_image = data['image']
    out = {
        'user': groupname,
        'image': image,
        "b64_image": b64_image
    }

    print(out)
    changeGroupPhoto(groupname, b64_image)
    return jsonify({"data": out})


@app.route('/delete_group_member', methods=['POST'])
def delete_group_member():
    data = request.form
    group_name = data['group_name']
    username = data['username']
    return jsonify({"data": data})


'''Vote Table'''


@app.route('/vote/<pollid>')
@cross_origin()
def vote_by_poll_id(pollid):
    data = getPollDetails(pollid)
    # print(data)
    return jsonify(data)


@app.route('/poll/<pollid>')
@cross_origin()
def vote_by_poll_id_(pollid):
    print("Poll id : ", pollid)
    data = getPollDetails(pollid)
    return jsonify(data)


@app.route('/cast_vote', methods=['POST'])
@cross_origin()
def cast_vote():
    data = dict(request.form)
    # print(dict(request.body))
    print(data)
    username = data['username']
    pollid = data['poll_id']
    option = data['option']
    castVote(username, pollid, option)
    return jsonify(data)


'''Poll Table'''


@app.route('/new_poll', methods=['POST'])
@cross_origin()
def new_poll():
    data = dict(request.form)
    print("New Poll :", data)
    try:
        newPoll(data)
    except:
        print("error occured by creating")
    return jsonify(data)


@app.route('/auth/<username>')
@cross_origin()
def auth(username):
    data = Auth(username)
    return jsonify(data)


@app.route('/poll_feed')
@cross_origin()
def poll_feed():
    data = getPollFeed()
    return jsonify(data)


@app.route("/delete_poll/<poll_id>", methods=['GET'])
def delete_poll(poll_id):
    try:
        deletePollById(poll_id)
    except:
        print("poll id doesn't exist")
    return jsonify({"res": "success"})


@app.route('/new_comment', methods=['POST'])
@cross_origin()
def new_comment():
    data = dict(request.form)
    print("Comment : ", data)
    newComment(data['tweet_id'], data['username'], data['content'])
    return jsonify({"res": "works well"})


@app.route('/comments_by_tweeter_id/<tweetid>')
@cross_origin()
def comments_by_tweeter_id(tweetid):
    data = commentsByTweetId(tweetid)
    #print("Tweetid :", tweetid, data2)
    return jsonify(data)


@app.route('/delete_comment/<comment_id>', methods=['GET'])
def delete_comment(comment_id):
    deleteCommentById(comment_id)
    return jsonify({"res": "comment deleted"})


@app.route('/test')
@cross_origin()
def test():
    arr = (1, 2, 3, 4, 5)
    return jsonify(arr)


@app.route('/all_users')
@cross_origin()
def all_users():
    allusers = getAllUsers()
    return jsonify(allusers)


@app.route('/get_chat/<user1>/<user2>')
@cross_origin()
def get_chat(user1, user2):
    out = getChat(user1, user2)
    return jsonify(out)


@app.route('/new_chat_msg', methods=['POST'])
@cross_origin()
def new_chat_msg():
    data = dict(request.form)
    print("msg : ", data)
    sender = data["sender"]
    receiver = data["receiver"]
    msg = data["msg"]
    putMsg(sender, receiver, msg)


@app.route('/all_groups', methods=['GET'])
@cross_origin()
def all_groups():
    data = getAllGroups()
    return jsonify(data)


@app.route('/group_detail/<group>/<user>')
@cross_origin()
def group_detail(group, user):
    data = getGroupDetail(group, user)
    is_member = isMemberOfGroup(group, user)
    members = getAllGroupMembers(group)
    out = {
        "data": data,
        "isMember": is_member,
        "members": members
    }
    return jsonify(out)


@app.route('/join_group', methods=['POST'])
@cross_origin()
def join_group():
    data = dict(request.form)
    print("Join data", data)
    joinGroup(data['grpname'], data['username'])
    return data


@app.route('/leave_group', methods=['POST'])
@cross_origin()
def leave_group():
    data = dict(request.form)
    leaveGroup(data['grpname'], data['username'])
    return data


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # app.run(host='192.168.31.55', port=5000)
    # app.run()
