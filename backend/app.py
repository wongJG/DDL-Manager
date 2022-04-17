from urllib import response
from click import password_option
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
import random
from matplotlib import use
from sympy import re

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


def get_all_deadline():

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select id, name, time, set_reminder as reminder from deadline where time > DATE() order by time;')
    result = [dict(i) for i in c.fetchall()]

    c.execute('select id, name as title, time as date from deadline where time > DATE() order by time;')
    result2 = [dict(i) for i in c.fetchall()]

    conn.close()

    return result, result2

def add_deadline(name,time,set_reminder):

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO deadline (name,time,from_bb,set_reminder,user_id) VALUES ('%s', '%s', 0, %s, 10)" % (name,time,set_reminder))
    conn.commit()
    conn.close()

def remove_deadline(deadline_id):
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM deadline WHERE id = %s;" % deadline_id)
    conn.commit()
    conn.close()


@app.route('/deadlines', methods=['GET', 'POST'])
def all():

    # Add deadlines
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        add_deadline(post_data.get('name'),post_data.get('time'),post_data.get('reminder'))
        response_object['message'] = 'Deadline added'
    
    # Get deadlines
    else:
        Deadlines,Deadlines_events = get_all_deadline()
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
        add_deadline(post_data.get('name'),post_data.get('time'),post_data.get('reminder'))
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
    syncDeadlines(post_data.get('username'),post_data.get('password')) 
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

    print(response_object['message'])

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

    return True


@app.route('/sentCode', methods=['POST'])
def handlesentVerifyCode():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    username = post_data.get('username')

    if sentCode(username): response_object['message'] = 'Verification Code Sent'
    else: response_object['message'] = 'Account Already Registered'

    print(response_object['message'])

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


    if (int(ver_code) != verifycode): return "Wrong Verification Code",id

    else:
        c.execute("INSERT INTO user (username,password) VALUES ('%s', '%s');" % (username, password))
        conn.commit()
        c.execute("select id from user where username = '%s';" % username )
        id = [dict(i) for i in c.fetchall()][0]['id']
        return "Registration Success", id


@app.route('/register', methods=['POST'])
def handleRegister():
    
    response_object = {'status': 'success'}
    post_data = request.get_json()

    response_object['message'], response_object['id'] = register(post_data.get('username'), post_data.get('password'), post_data.get('verifyCode'))
    

    print(response_object['message'])

    return jsonify(response_object)



if __name__ == '__main__':
    app.run()