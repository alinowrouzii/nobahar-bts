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
from app1.api.serializer import GroupSerializer, GroupPartialSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def loginAPI(request):
    
    try:
        print("hey")
        email = request.POST["email"]
        password = request.POST["password"]
        # user = User.objects.get(username=user.username, password=password)
        user = authenticate(username=email, password=password)
        if not user:
            return Response(data={"error": {"enMessage": "Bad request!"}},  status=400)
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
             status=200
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
    return Response(
        {
            "code": "you are authenticated",
        }
    )

# JOIN requests
@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getJoinRequestsAPI(request):
    pass


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createJoinRequestAPI(request):
    pass


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def joinRequestsGroupAPI(request):
    pass

@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def joinRequestsAcceptAPI(request):
    pass


# CONNECTION requests

@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def connectionRequestGetAPI(request):
    pass


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def connectionRequestPostAPI(request):
    pass


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def connectionRequestAcceptAPI(request):
    pass


# GROUPS API

@check_bearer
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def getAllGroupsAPI(request):
    
    if request.method == 'GET':
        groups = Group.objects.order_by("created_at").all()
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
        groups = Group.objects.order_by("created_at").all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getChatsAPI(request):
    pass


@check_bearer
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMessagesAPI(request):
    pass


@check_bearer
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sendMessageAPI(request):
    pass
