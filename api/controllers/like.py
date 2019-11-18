import query
from flask import request, jsonify

def get_likes(id_list):
  queryString = f"select * from public.like where id_list={id_list}"
  result = query.raw(queryString, True)
  return jsonify(result)

def create(data):
  try:
    id_user = data['id_user']
    id_list = data['id_list']
    queryString = f"insert into public.like(id_user, id_list) values ({id_user}, {id_list}) returning id"
    result = query.raw(queryString, False)
    result = query.raw(f"update public.list set likes = likes + 1 where id={id_list} returning id", False)
    return jsonify('Curtido com sucesso')
  except:
    return jsonify('Ocorreu uma falha ao curtir a lista')

def delete(data):
  try:
    id_user = data['id_user']
    id_list = data['id_list']
    queryString = f"delete from public.like where id_user={id_user} and id_list={id_list} returning id"
    result = query.raw(queryString, False)
    if result == None:
      return jsonify('Não é possível descurtir uma lista que não foi curtida')
    result = query.raw(f"update public.list set likes = likes - 1 where id={id_list} returning id", False)
    return jsonify('Lista descurtida')
  except:
    return jsonify('Ocorreu uma falha ao descurtir a lista')

def delete_from_list(id_list):
  try:
    queryString = f"delete from public.like where id_list={id_list} returning id"
    result = query.raw(queryString, True)
    return jsonify({'success': True})
  except Exception as e:
    print(e)
    return jsonify({'success': False})