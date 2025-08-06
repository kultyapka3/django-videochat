from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from agora_token_builder import RtcTokenBuilder

from json import load, loads
from random import randint
from time import time

from .models import RoomMember

with open('static/config.json', 'r') as f:
    config = load(f)

def get_token(request):
    app_id = config['APP_ID']
    app_certificate = config['APP_CERTIFICATE']
    channel_name = request.GET.get('channel')
    uid = randint(1, 230)
    role = 1
    expiration_time_in_seconds = 3600 * 24
    current_time_stamp = time()
    privilege_expired_ts = current_time_stamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)

    return JsonResponse({'token':token, 'uid':uid}, safe=False)

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')

@csrf_exempt
def create_member(request):
    data = loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room=data['room']
    )

    return JsonResponse({'name':data['name']}, safe=False)

def get_member(request):
    uid = request.GET.get('UID')
    room = request.GET.get('room')

    member = RoomMember.objects.get(
        uid=uid,
        room=room,
    )

    name = member.name

    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def delete_member(request):
    data = loads(request.body)

    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room=data['room'],
    )

    member.delete()

    return JsonResponse('Member has deleted', safe=False)
