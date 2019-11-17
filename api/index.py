from flask import Flask, request, jsonify
from controllers import user, list

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

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

@app.route('/user/edit/', methods=['PUT'])
def edit_user():
  req_data = request.get_json()
  return user.update(req_data)

@app.route('/list/', methods=['GET','POST','PUT','DELETE'])
def handle_list():
  if request.method == 'GET':
    return list.get()
  req_data = request.get_json()
  if request.method == 'POST':
    return list.create(req_data)
