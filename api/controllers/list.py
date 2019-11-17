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
  id_user = data['id_user']
  title = data['title']
  private = data['private']
  ordered = data['ordered']
  queryString = f'''INSERT INTO public.list(
	id_user, title, private, ordered)
	VALUES ({id_user}, '{title}', {private}, {ordered}) returning id'''
  result = query.raw(queryString, False)
  id_list = result['id']
  items = data['items']
  if ordered:
    for item in items:
      queryString = f'''INSERT INTO public.item(
      id_list, item_order, text)
      VALUES ({id_list}, {item['item_order']}, '{item['text']}') returning id'''
      print(queryString)
      result = query.raw(queryString, False)
      
    return jsonify('success creating ordered list')
  else:
    for item in items:
      queryString = f'''INSERT INTO public.item(
      id_list, text)
      VALUES ({id_list}, '{item['text']}') returning id'''
      result = query.raw(queryString, False)
    return jsonify('success creating list')

def delete(id):
  try:
    queryString = f"delete from public.item where id_list={id} returning id"
    result = query.raw(queryString, True)
    queryString = f"delete from public.list where id={id} returning id"
    result = query.raw(queryString, False)
    return jsonify("Lista excluída com sucesso")
  except:
    return jsonify("Não foi possível excluir a lista")
