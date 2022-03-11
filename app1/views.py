from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from decouple import config
from django.contrib.auth import authenticate
import jwt
from app1.models import User


@api_view(["POST"])
@permission_classes([AllowAny])
def loginAPI(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        print(email)
        print(password)

        # user = User.objects.get(username=user.username, password=password)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": {"enMessage": "Bad request!"}})
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
            {
                "message": "successful",
                "token": str(encoded),
            }
        )
    except Exception as e:
        return Response({"error": {"enMessage": "Bad request!"}})


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
    except Exception as e:
        return Response(data={"error": {"enMessage": "Bad request!"}}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    print(request.user.username)
    return Response(
        {
            "code": "you are authenticated",
        }
    )
