from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3

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



if __name__ == '__main__':
    app.run()