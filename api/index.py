from flask import Flask, request, jsonify
from controllers import user

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

""" @app.route('/')
def root_route():
  return jsonify({
    'root': 'test2'
  }) """

  #request.args.get('language') or request.args['language']


@app.route('/user/<int:id>')
def get_user(id=None):
  return user.get(id)

@app.route('/user/register/', methods=['POST'])
def register():
  req_data = request.get_json()
  return user.create(req_data)

@app.route('/login/', methods=['POST'])
def login():
  req_data = request.get_json()
  return user.login(req_data)