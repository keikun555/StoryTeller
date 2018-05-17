"""
TODO list
Server side input checking (return bad request error on error)
LDAP authentication (perhaps build a LDAP Python library)
Database interface/integration
"""
from STParser import story_to_STGraph
from auth import check_credentials
from STGraph import STGraph
from sys import exit
import uuid
import json
import os

from flask import Flask, request, render_template, jsonify, abort

STORY_FILEPATH = "static/stories/heyjude.story"
app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
session = {}
current_user = {}
story = None


# @app.before_request # uncomment to get cookies to work
def csrf_protect():
    if request.method == "POST" and request.path not in ["/login"]:
        token = session.pop('_csrf_token', None)
        if token is None or token != request.form.get('cookie'):
            abort(401)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid4())
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


@app.route('/', methods=['GET'])
def main():
    global story
    print "user connected with IP {}".format(request.environ['REMOTE_ADDR'])
    story = story_to_STGraph(STORY_FILEPATH)
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    username = data["username"]
    password = data["password"]
    user = check_credentials(username, password)
    if(user is not None):
        for key in user:
            current_user[key] = user[key]
        current_user["user_id"] = db.ldap_get_user_id(current_user)
        print "{} connected with IP {}".format(current_user['name'],
                                               request.environ['REMOTE_ADDR'])
        return jsonify({
            'login_successful': True,
            'token': generate_csrf_token(),
            'user': current_user
        })
    else:
        return jsonify({
            'login_successful': False,
            'errors': ['Unable to login with given credentials!']
        })


@app.route('/next_frame', methods=['POST'])
def get_next_frame():
    """
    gets next frame
    """
    request_data = request.form.to_dict()
    if "choice" in request_data:
        story.choose(request_data["choice"])
    return jsonify({
        'cookie': generate_csrf_token(),
        'text': story.get_current().replace("\n", "<br/>"),
        'choices': story.get_choices()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
