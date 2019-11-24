import query
from flask import request, jsonify

def put_user(comment):
  queryString = f"select name, photo from public.user where id={comment['id_user']}"
  result = query.raw(queryString, False)
  comment['user'] = result
  return comment

def get(id_list):
  queryString = f"select id, comment_text, id_user, comment_date from public.comment where id_list={id_list} order by id desc"
  comments = query.raw(queryString, True)
  if comments == None:
    return []
  result = map(put_user,comments)
  return list(result)

def create(data):
  try:
    id_user = data['id_user']
    id_list = data['id_list']
    comment_text = data['comment_text']
    queryString = f'''INSERT INTO public.comment(
    id_user, id_list, comment_text)
    VALUES ({id_user}, {id_list}, '{comment_text}') returning id'''
    result = query.raw(queryString, False)
    return jsonify(result)
  except Exception as e:
    print(e)
    return jsonify('Não foi possível salvar seu comentário')

def delete(id):
  try:
    queryString = f"delete from public.comment where id={id} returning id"
    result = query.raw(queryString, False)
    if result == None:
      return jsonify('Não é possível excluir um comentário inexistente')
    return jsonify('Comentário excluído')
  except Exception as e:
    print(e)
    return jsonify('Não foi possível excluir o comentário')

def delete_from_list(id_list):
  try:
    queryString = f"delete from public.comment where id_list={id_list} returning id"
    result = query.raw(queryString, True)
    return jsonify({'success': True})
  except Exception as e:
    print(e)
    return jsonify({'success': False})