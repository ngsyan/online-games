from flask import g, request

from ..service.socket_service import get_user_and_room, login_room_socket, user_get_in_room, user_get_out_room
from ..service.message_service import save_new_message
from .. import socketio

from flask_socketio import disconnect, join_room, leave_room, emit, rooms

import json


@socketio.on('connect')
def connectClient():
	print(">>>>>>>>> Client connected on rooth path with session id " + request.sid)


def update_list_users(list_users, room):
	response_object = {
		'users_in_room': list_users
	}
	emit('users_in_room', response_object, room=room.id, namespace='/rooms')


@socketio.on('disconnect')
def disconnectClient():
	print(">>>>>>>>> Client disconnected on rooth path with session id " + request.sid)
	# Check authenticate session id
	list_user_id = rooms(sid=request.sid, namespace="/user_id")
	list_room_id = rooms(sid=request.sid, namespace="/room_id")

	user, room = get_user_and_room(list_user_id, list_room_id)
	if user is not None and room is not None:
		list_users = user_get_out_room(user, room)
		update_list_users(list_users, room)


@socketio.on('request_login_with_room', namespace='/rooms')
def registerUserRoomID(request_object):
	user, room, response_object = login_room_socket(request_object)
	# Notify sender response result
	emit('response_login_with_room', response_object, broadcast=False, namespace='/rooms')

	if user is not None and room is not None:
		# join room to authenticate
		join_room(room=user.id, namespace='/user_id')
		join_room(room=room.id, namespace='/room_id')
		# join room to get message and event
		join_room(room=room.id, namespace='/rooms')

		list_users = user_get_in_room(user, room)
		update_list_users(list_users, room)


@socketio.on('request_room_message', namespace='/rooms')
def newRoomMessage(request_object):
	# Check authenticate session id
	list_user_id = rooms(sid=request.sid, namespace="/user_id")
	list_room_id = rooms(sid=request.sid, namespace="/room_id")

	user, room = get_user_and_room(list_user_id, list_room_id)

	if user is None:
		response_object = {
            'status': 'false',
            'message': 'Fail to authenticate'
        }
	elif room is None:
		response_object = {
            'status': 'false',
            'message': 'Room not found'
        }
	else:
		response_object = {
			'status': 'success',
			'message': 'Send message successfully'
		}
		# Save new message to database
		content = request_object.get('content')
		new_message = save_new_message(sender_public_id=user.public_id, receiver_public_id=room.public_id, content=content)
		# Send new message to all receiver in that room
		receive_object = new_message.get_message_information()
		emit('receive_message', receive_object, room=room.id, namespace='/rooms')

	# Notify sender response result
	emit('response_room_message', response_object, broadcast=False, namespace='/rooms')
