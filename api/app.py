from flask import Flask, request, jsonify
from controllers import user, list, like

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

#request.args.get('language') or request.args['language']

@app.route('/')
def test():
  return jsonify('Test index page')

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
    return list.get(request.args.get('user'))
  req_data = request.get_json()
  if request.method == 'DELETE':
    return list.delete(req_data['id'])
  if request.method == 'POST':
    return list.create(req_data)

@app.route('/feed/')
def get_feed():
  return list.feed(request.args.get('user'))

@app.route('/likes/<int:id_list>')
def get_likes_from_list(id_list):
  return list.like.get_likes(id_list)

@app.route('/like/', methods=['POST'])
def like():
  return list.like.create(request.get_json())

@app.route('/deslike/', methods=['POST'])
def deslike():
  return list.like.delete(request.get_json())

@app.route('/comment/', methods=['POST', 'DELETE'])
def handle_comment():
  req_data = request.get_json()
  if request.method == 'DELETE':
    return list.comment.delete(req_data['id'])
  if request.method == 'POST':
    return list.comment.create(req_data)