from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import random
import os
from urllib.parse import urljoin
import time


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row
    return conn


# For testing
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def get_all_deadline(id):

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select id, name, time, set_reminder, user_id as reminder from deadline where user_id = %d order by time;' % id)
    result = [dict(i) for i in c.fetchall()]

    c.execute('select id, name as title, time as date, user_id from deadline where user_id = %d order by time;' % id)
    result2 = [dict(i) for i in c.fetchall()]

    conn.close()

    return result, result2

def add_deadline(user_id, name,time,set_reminder):

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO deadline (name,time,from_bb,set_reminder,user_id) VALUES ('%s', '%s', 0, %s, %d)" % (name,time,set_reminder,user_id))
    conn.commit()
    conn.close()

def remove_deadline(deadline_id):
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM deadline WHERE id = %s;" % deadline_id)
    conn.commit()
    conn.close()


@app.route('/add-deadline', methods=['POST'])
def handleaddDeadline():

    # Add deadlines
    response_object = {'status': 'success'}
    # if request.method == 'POST':
    post_data = request.get_json()
    add_deadline(post_data.get('id'),post_data.get('name'),post_data.get('time'),post_data.get('reminder'))
    response_object['message'] = 'Deadline added'
    
    return jsonify(response_object)


@app.route('/deadlines', methods=['POST'])
def handlegetDeadline():

    response_object = {'status': 'success'}
    post_data = request.get_json()
    Deadlines,Deadlines_events = get_all_deadline(post_data.get('id'))
    response_object['deadlines'] = Deadlines
    response_object['deadlines_event'] = Deadlines_events

    return jsonify(response_object)




@app.route('/deadlines/<deadline_id>', methods=['PUT', 'DELETE'])
def single(deadline_id):
    response_object = {'status': 'success'}

    # Update Deadline
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_deadline(deadline_id)
        add_deadline(post_data.get('id'),post_data.get('name'),post_data.get('time'),post_data.get('reminder'))
        response_object['message'] = 'Deadline updated'

    # Delete deadline
    if request.method == 'DELETE':
        remove_deadline(deadline_id)
        response_object['message'] = 'Deadline removed'
    return jsonify(response_object)


@app.route('/deadlines/sync', methods=['PUT'])
def sync():
    from getCalendar import syncDeadlines
    response_object = {'status': 'success'}
    post_data = request.get_json()
    syncDeadlines(post_data.get('id'), post_data.get('username'),post_data.get('password')) 
    response_object['message'] = 'Deadline synced'
    return jsonify(response_object)


'''Login'''


def authinfo(username):
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("select id, username, password from user where username = '%s';" % username )
    result = [dict(i) for i in c.fetchall()]
    conn.close()

    return result


@app.route('/login', methods=['POST'])
def login():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    auth = authinfo(post_data.get('username'))

    if (len(auth)==0):
        response_object['message'] = 'No such User'

    elif (auth[0]['password'] != post_data.get('password')):
        response_object['message'] = 'Wrong Password'

    else: 
        response_object['message'] = 'Logged in'
        response_object['userid'] = auth[0]['id']
        print(response_object['userid'])

    return jsonify(response_object)



'''Verification Code'''

def sentCode(username):

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("select id, username, password from user where username = '%s';" % username )
    result = [dict(i) for i in c.fetchall()]

    if (len(result)!=0): return False

    randomCode = random.randint( 100000, 999999 )

    print(randomCode)

    c.execute("REPLACE INTO verification (username, ver_code) VALUES ('%s', %d)" % (username, randomCode))
    conn.commit()
    conn.close()
    
    from sentEmail import sentCode as sent
    sent(username,randomCode)

    return True


@app.route('/sentCode', methods=['POST'])
def handlesentVerifyCode():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    username = post_data.get('username')

    if sentCode(username): response_object['message'] = 'Verification Code Sent'
    else: response_object['message'] = 'Account Already Registered'

    # print(response_object['message'])

    return jsonify(response_object)




'''Register'''

def register(username,password,ver_code):
    
    conn = get_db_connection()
    c = conn.cursor()
    id = 0
    
    c.execute("select id, username, password from user where username = '%s';" % username )
    result = [dict(i) for i in c.fetchall()]
    if (len(result)!=0): return "Account Already Registered",id

    c.execute("select id, username, ver_code from verification where username = '%s';" % username)
    verifycode = int([dict(i) for i in c.fetchall()][0]['ver_code'])

    print(int(ver_code), int(verifycode))

    if (int(ver_code) != int(verifycode)): return "Wrong Verification Code",id

    else:
        c.execute("INSERT INTO user (username,password) VALUES ('%s', '%s');" % (username, password))
        conn.commit()
        c.execute("select id from user where username = '%s';" % username )
        id = [dict(i) for i in c.fetchall()][0]['id']
        conn.close()
        return "Registration Success", id


@app.route('/register', methods=['POST'])
def handleRegister():
    
    response_object = {'status': 'success'}
    post_data = request.get_json()

    response_object['message'], response_object['id'] = register(post_data.get('username'), post_data.get('password'), post_data.get('verifyCode'))
    

    print(response_object['message'])

    return jsonify(response_object)


'''Change Password'''
@app.route('/changePass', methods=['POST'])
def changPass():
    
    response_object = {'status': 'success'}
    post_data = request.get_json()
    id = post_data.get('id')
    oldPass = post_data.get('oldPass')
    newPass = post_data.get('newPass')


    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("select id, password from user where id = %d;" % id )
    fetch_oldPass = [dict(i) for i in c.fetchall()][0]['password']

    if (fetch_oldPass != oldPass):
        response_object['message'] = 'Old Password does NOT match'

    else:
        c.execute("Update user set password='%s' where id = %d;" % (newPass,int(id)) )
        conn.commit()
        response_object['message'] =  'Password Updated'

    conn.close()

    print(response_object['message'])

    return jsonify(response_object)



'''User Management'''

@app.route('/users', methods=['GET'])
def getAllUsers():

    response_object = {'status': 'success'}

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select id, username from user order by id;')
    users = [dict(i) for i in c.fetchall()]
    conn.close()

    response_object['users'] = users

    return jsonify(response_object)

@app.route('/users/<user_id>', methods=['POST', 'DELETE'])
def singleUser(user_id):
    
    response_object = {'status': 'success'}

    # Update User
    if request.method == 'POST':
        post_data = request.get_json()
        newPass = post_data.get('newPassword')
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("Update user set password='%s' where id = %d;" % (newPass,int(user_id)))
        # print("Update user set password='%s' where id = %d;" % (newPass,int(user_id)))
        conn.commit()
        conn.close()
        response_object['message'] = 'User updated'

    # Delete deadline
    if request.method == 'DELETE':
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("Delete From user where id = %d;" % int(user_id))
        conn.commit()
        conn.close()
        response_object['message'] = 'User removed'
    
    return jsonify(response_object)


'''Admin Auth'''
@app.route('/admin', methods=['POST'])
def adminAuth():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    id = post_data.get('id')

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # c.execute('CREATE table admin ( id INTEGER PRIMARY KEY, isAdmin BIT, FOREIGN key (id) REFERENCES user(id) );')
    # c.execute('insert into admin VALUES (5,1);')
    # conn.commit()
    c.execute('select id, isAdmin from admin where id = %d;' % id)
    result = [dict(i) for i in c.fetchall()]
    conn.close()

    if (len(result) == 0): response_object['isAdmin'] = 0
    else: response_object['isAdmin'] = 1

    return jsonify(response_object)


'''pic upload'''

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files.get('file')

    # print(request.form.get('id'))
    filename = request.form.get('id')
    filepath = os.path.join('./image', filename)
    file.save(filepath)

    file_url = urljoin(request.host_url, 'uploads/'+ filename)
    # print(file_url)

    time.sleep(0.1)
    
    return file_url


'''Get photo'''

@app.route('/uploads/<path:filename>')
def get_file(filename):
    time.sleep(0.2)
    return send_from_directory('./image', filename)

if __name__ == '__main__':
    app.run()