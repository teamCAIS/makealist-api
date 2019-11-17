import query
from flask import request, jsonify

def put_items(list):
  id_user = list['id_user']
  list['user'] = query.raw(f"select id, name, email, photo from public.user where id={id_user}", False)
  list['items'] = []
  id_list = list['id']
  queryString = f'select * from public.item where id_list={id_list}'
  items = query.raw(queryString, True)
  for item in items:
    list['items'].append(item)
  return list

def get():
  queryString = "select * from public.list"
  lists = query.raw(queryString, True)
  result = map(put_items,lists)
  return jsonify(list(result))

def create(data):
  return jsonify(request.method)