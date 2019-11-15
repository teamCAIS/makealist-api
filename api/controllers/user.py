import query
from flask import request, jsonify
from passlib.hash import pbkdf2_sha256

def get(id):
  queryString = "select id, name, email, bio, birth_date, photo from public.user where id={0}".format(id)
  result = query.raw(queryString, False)
  return jsonify(result)

def email_exists(email):
  queryString = f"select email from public.user where email='{email}'"
  result = query.raw(queryString, False)
  if result == None:
    return False
  return True

def create(data):
  #convert dict to strings of keys and values
  name = data['name']
  email = data['email']
  if email_exists(email):
    return jsonify({
      'message':'O e-mail informado já está cadastrado no sistema'
    })
  password = pbkdf2_sha256.hash(data['password'])
  queryString = f"insert into public.user (name, email, password) values ('{name}', '{email}', '{password}') returning id"
  result = query.raw(queryString, False)
  return get(result['id'])

def login(data):
  email = data['email']
  queryString = f"select id, password from public.user where email='{email}'"
  result = query.raw(queryString, False)
  if result == None:
    return jsonify({
      'message':'O e-mail informado não está cadastrado no sistema'
    })
  password = data['password']
  is_correct = pbkdf2_sha256.verify(password, result['password'])
  if is_correct:
    return get(result['id'])
  return jsonify({
      'message':'A senha está incorreta'
    })

def update(data):
  sets = []
  try:
    sets.append(f"name = '{data['name']}'")
  except:
    print('There is no name')
  try:
    if email_exists(data['email']):
      return jsonify({
        'message':'O e-mail informado já está cadastrado no sistema'
      })
    sets.append(f"email = '{data['email']}'")
  except:
    print('There is no email')
  try:
    password = pbkdf2_sha256.hash(data['password'])
    sets.append(f"password = '{password}'")
  except:
    print('There is no password')
  
  if len(sets) == 0:
    return jsonify({
        'message':'Nenhum campo foi alterado'
      })
  
  sets = ', '.join(sets)
  queryString = f"update public.user set {sets} where id={data['id']} returning id"
  print(queryString)
  result = query.raw(queryString, False)
  return get(result['id'])
  