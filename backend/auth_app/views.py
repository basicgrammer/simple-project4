import json
import copy
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, generics, status

# from fres_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from .Services.AuthService import *
from .Services.CryptService import *


class SignUpView(APIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        request_body=serializer_class, responses={"200": serializer_class}
    )
    def post(self, request):
        convert_data = json.loads(request.body)

        result = AuthService().duplicate_check(convert_data["username"])
        ## result 결과가 True로 반환되는 경우 중복 체크에 문제가 없다는 이야기

        if result:
            crypt_pw = CryptService().password_crypt(convert_data["password"])
            convert_data["password"] = crypt_pw

            deserializer = self.serializer_class(data=convert_data)
            deserializer.is_valid(raise_exception=True)
            deserializer.save()

        else:
            return Response(status=201)


class BasicViewSet(viewsets.ModelViewSet):
    @csrf_exempt
    def create(self, request, pk: int = None):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def retrieve(self, request, pk: int = None):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def partial_update(self, request, pk: int = None):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def destroy(self, request, pk: int = None):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def update(self, request, pk: int = None):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
