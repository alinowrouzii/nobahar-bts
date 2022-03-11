from tokenize import group
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from decouple import config
from django.contrib.auth import authenticate
import jwt
from app1.models import User, Group, UserJoinRecord, GroupConnectionRecord
from app1.decorator import check_bearer
from app1.models import *
from django.db.models import Q

from app1.api.serializer import GroupSerializer, GroupPartialSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def loginAPI(request):

    try:
        email = request.POST["email"]
        password = request.POST["password"]
        # user = User.objects.get(username=user.username, password=password)
        user = authenticate(username=email, password=password)
        if not user:
            return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)
        refreshToken = RefreshToken.for_user(user)
        accessToken = refreshToken.access_token

        decodeJTW = jwt.decode(
            str(accessToken), config("SECRET_KEY"), algorithms=["HS256"]
        )

        # add payload here!!
        decodeJTW["email"] = user.username
        decodeJTW["userId"] = user.pk

        # encode
        encoded = jwt.encode(decodeJTW, config("SECRET_KEY"), algorithm="HS256")

        return Response(
            data={
                "message": "successful",
                "token": str(encoded),
            },
            status=200,
        )
    except Exception:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def signupAPI(request):
    try:
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]

        user = User.objects.create(username=email, name=name)
        user.set_password(password)

        user.save()

        refreshToken = RefreshToken.for_user(user)
        accessToken = refreshToken.access_token

        decodeJTW = jwt.decode(
            str(accessToken), config("SECRET_KEY"), algorithms=["HS256"]
        )

        # add payload here!!
        decodeJTW["email"] = user.username
        decodeJTW["userId"] = user.pk

        # encode
        encoded = jwt.encode(decodeJTW, config("SECRET_KEY"), algorithm="HS256")

        return Response(
            data={"token": str(encoded), "message": "successful"}, status=200
        )
    except Exception:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    print(request.user.username)
    
    # from random import randint
    # rand = randint(0,1000000)
    # group = Group(owner=request.user, name=f"shit{rand}", description="hello shit")
    
    # group.save()
    
    group = Group.objects.get(owner=request.user)
    
    print(group.created_at.timestamp())
    return Response(
        {
            "code": "you are authenticated",
        }
    )


# JOIN requests


def getJoinRequestsAPI(request):

    user = request.user

    join_records = user.records.order_by("-timestamp")

    payload = []
    # There's no time to use serializer ;)
    for record in join_records.all():
        payload.append(
            {
                "id": record.pk,
                "groupId": record.group.pk,
                "userId": record.user.pk,
                "date": record.timestamp.timestamp(),
            }
        )
    return Response(data={"joinRequests": payload}, status=200)


def createJoinRequestAPI(request):
    try:

        user = request.user

        if (
            user.records.filter(invitation_status=True).exists()
            or Group.objects.filter(owner=user).exists()
        ):
            return Response({"error": {"enMessage": "Bad request!"}})

        group_id = request.POST["groupId"]
        group = Group.objects.get(pk=group_id)

        newRecord = UserJoinRecord(user=user, group=group)
        newRecord.save()

        return Response(data={"message": "successful"}, status=200)
    except Exception as e:

        print(e)
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def joinRequestAPI(request):
    if request.method == "GET":
        return getJoinRequestsAPI(request)
    else:
        return createJoinRequestAPI(request)


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def joinRequestsGroupAPI(request):
    # check user is owner of group or not
    user = request.user

    try:
        group = Group.objects.get(owner=user)

        group_join_records = group.records.order_by("-timestamp")

        payload = []
        # There's no time to use serializer ;)
        # TODO sort by newest
        for record in group_join_records.all():
            payload.append(
                {
                    "id": record.pk,
                    "groupId": record.group.pk,
                    "userId": record.user.pk,
                    "date": record.timestamp.timestamp(),
                }
            )
        return Response(data={"joinRequests": payload}, status=200)
    except Exception as e:
        print(e)
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def joinRequestsAcceptAPI(request):
    # check user is owner of group or not
    user = request.user

    try:
        joinRequestId = request.POST["joinRequestId"]
        group = Group.objects.get(owner=user)

        group_join_record = group.records.get(pk=joinRequestId)

        # check that user is already memebr of group or owner of group or not
        user_to_join = group_join_record.user
        if (
            user_to_join.records.filter(invitation_status=True).exists()
            or Group.objects.filter(owner=user_to_join).exists()
        ):
            return Response({"error": {"enMessage": "Bad request!"}})

        group_join_record.invitation_status = True

        group_join_record.save()

        return Response(data={"message": "successful"}, status=200)

    except Exception as e:
        print(e)
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


# CONNECTION requests


def getGroupConnectionRequestsAPI(request):
    user = request.user

    try:
        group = Group.objects.get(owner=user)

        payload = []
        # all connection_records that are sent to this group
        for record in group.to_connections.order_by("-timestamp").all():
            payload.append(
                {
                    "connectionRequestId": record.pk,
                    "groupId": record.from_group,
                    "sent": record.timestamp.timestamp(),
                }
            )
        return Response(data={"requests": payload}, status=200)
    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


def connectionRequestPostAPI(request):
    user = request.user
    try:
        from_group = Group.objects.get(owner=user)

        groupId = request.POST["groupId"]
        to_group = Group.objects.get(pk=groupId)

        connectionRecord = GroupConnectionRecord(
            from_group=from_group, to_group=to_group
        )

        connectionRecord.save()

        return Response(data={"message": "successful"}, status=200)
    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def connectionRequest(request):
    if request.method == "GET":
        return getGroupConnectionRequestsAPI(request)
    else:
        return connectionRequestPostAPI(request)


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def connectionRequestAcceptAPI(request):
    user = request.user

    try:
        to_group = Group.objects.get(owner=user)

        from_groupId = request.POST["groupId"]
        from_group = Group.objects.get(pk=from_groupId)

        connectionRequest = to_group.to_connections.get(from_group=from_group)
        if connectionRequest.application_status:
            return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)

        connectionRequest.application_status = True
        connectionRequest.save()

        return Response(data={"message": "successful"}, status=200)
    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


# GROUPS API


@check_bearer
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def getAllGroupsAPI(request):
    
    if request.method == 'GET':
        groups = Group.objects.order_by("-created_at").all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print('here')
        if request.user:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['owner'] = request.user.pk
            request.data._mutable = _mutable
            serializer = GroupSerializer(data=request.data)
            print('there')
            if serializer.is_valid():
                group = serializer.save()
                return Response({"group": {"id": group.id}, "message": "successful"}, status=200)
    
    return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def myGroupsAPI(request):
    if request.method == 'GET':
        groups = Group.objects.order_by("-created_at").all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


# CHAT requests
@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getChatsAPI(request):
    user = request.user

    messages = (
        Message.objects.filter(Q(from_user=user) | Q(to_user=user))
        .order_by("-created_at")
        .distinct("from_user")
        .distinct("to_user")
        .all()
    )

    payload = []
    for message in messages:
        payload.append(
            {
                "userId": message.to_user.pk
                if message.from_user == user
                else message.from_user.pk,
                "name": message.to_user.name
                if message.from_user == user
                else message.from_user.name,
            }
        )
    return Response(data={"chats": payload}, status=200)


def getMessagesAPI(request, user_id):
    user = request.user

    try:

        user_2 = User.objects.get(pk=user_id)
        messages = Message.objects.filter(
            (Q(from_user=user) & Q(to_user=user_2))
            | (Q(from_user=user_2) & Q(to_user=user))
        ).order_by("-created_at")

        if messages.count() == 0:
            return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)

        payload = []
        for message in messages.all():
            payload.append(
                {
                    "message": message.text,
                    "date": message.created_at.timestamp(),
                    "sentby": message.from_user.pk,
                }
            )
        return Response(data={"messages": payload}, status=200)

    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


def sendMessageAPI(request, user_id):
    user = request.user

    try:
        message = request.POST["message"]

        user_2 = User.objects.get(pk=user_id)

        group = user.records.get(invitation_status=True).group

        group_2 = user_2.records.get(invitation_status=True).group

        # It will raise an exception if mathing  query does not found
        GroupConnectionRecord.objects.get(
            (
                (Q(from_group=group) & Q(to_group=group_2))
                | (Q(from_group=group_2) & Q(to_group=group))
            )
            & Q(application_status=True)
        )

        # Ye payam daram baraye parsalipe Aziiiiz
        newMessage = Message(text=message, from_user=user, to_user=user_2)
        newMessage.save()

        return Response(data={"message": "successful"}, status=200)
    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def messagesAPI(request, user_id):
    if request.method == "GET":
        return getMessagesAPI(request, user_id)
    else:
        return sendMessageAPI(request, user_id)
