import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS


Deadlines = [
    {
        'id': uuid.uuid4().hex,
        'name': 'Assignment-1',
        'date': '2022-03-01',
        'time': '17:00',
        'Reminder': False,
    },
]


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


def remove_deadline(deadline_id):
    for deadline in Deadlines:
        if deadline['id'] == deadline_id:
            Deadlines.remove(deadline)
            return True
    return False


@app.route('/deadlines', methods=['GET', 'POST'])
def all():

    # Add deadlines
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        Deadlines.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'date': post_data.get('date'),
            'time': post_data.get('time'),
            'reminder': post_data.get('reminder')
        })
        response_object['message'] = 'Deadline added'
    
    # Get deadlines
    else:
        response_object['deadlines'] = Deadlines
    
    
    return jsonify(response_object)


@app.route('/deadlines/<deadline_id>', methods=['PUT', 'DELETE'])
def single(deadline_id):
    response_object = {'status': 'success'}

    # Update Deadline
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_deadline(deadline_id)
        Deadlines.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'date': post_data.get('date'),
            'time': post_data.get('time'),
            'reminder': post_data.get('reminder')
        })
        response_object['message'] = 'Deadline updated'

    # Delete deadline
    if request.method == 'DELETE':
        remove_deadline(deadline_id)
        response_object['message'] = 'Deadline removed'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()