import query
from flask import request, jsonify
from controllers import like, comment

def put_items(list, id_viewer):
  #put user
  id_user = list['id_user']
  list['user'] = query.raw(f"select id, name, email, photo from public.user where id={id_user}", False)
  #put items
  list['items'] = []
  id_list = list['id']
  queryString = f'select * from public.item where id_list={id_list}'
  items = query.raw(queryString, True)
  for item in items:
    list['items'].append(item)
  #put liked
  queryString = f'select * from public.like where id_list={id_list} and id_user={id_viewer}'
  liked = query.raw(queryString, False)
  if liked == None:
    liked = False
  else:
    liked = True
  list['liked'] = liked
  #put comments
  list['comments'] = comment.get(id_list)
  return list

def get(id_viewer):
  queryString = "select * from public.list where private=false"
  lists = query.raw(queryString, True)
  if lists == None:
    return jsonify([])
  result = map(lambda list: put_items(list, id_viewer) ,lists)
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
    result = like.delete_from_list(id)
    result = comment.delete_from_list(id)
    queryString = f"delete from public.list where id={id} returning id"
    result = query.raw(queryString, False)
    
    return jsonify("Lista excluída com sucesso")
  except Exception as e:
    print(e)
    return jsonify("Não foi possível excluir a lista")
