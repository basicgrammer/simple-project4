import json
import copy
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, generics, status

# from fres_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from .Services.AuthService import *
from .Services.CryptService import *
from custom.custom_response import *


APPLY_RESPONSE = {
    "message": "상태 응답 메시지",
    "data": "응답에 대한 반환 데이터가 있는 경우 null을 대신하는 데이터 출력",
}


class SignUpView(APIView):
    # permissions_classes = [permissions.AllowAny]
    ## Swagger 선언 레벨에서 Permssion 처리를 수행했으므로 보안을 분리할때 선언해서 사용
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        operation_description="회원가입",
        request_body=serializer_class,
        responses={
            "201": ErrorCollection().as_md(APPLY_RESPONSE),
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @transaction.atomic
    def post(self, request):
        convert_data = json.loads(request.body)

        result = AuthService().duplicate_check(convert_data["username"])
        ## result 결과가 True로 반환되는 경우 중복 체크 성공

        if result:
            crypt_pw = CryptService().password_crypt(convert_data["password"])
            ## 패스워드 평문 저장이 아닌 암호화 저장을 위해 암호화 수행
            convert_data["password"] = crypt_pw

            deserializer = self.serializer_class(data=convert_data)
            deserializer.is_valid(raise_exception=True)
            deserializer.save()

            res_code = 201

            custom_res = custom_response(res_code)

            return Response(custom_res, status=status.HTTP_201_CREATED)

        else:
            res_code = 400
            message = "중복되는 ID가 존재합니다."
            custom_res = custom_response(res_code, message)

            return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    serializer_class = SignInSchema
    ## Swagger에서 입력되는 데이터와, 실제로 저장되는 데이터간 차이가 있으므로
    ## Schema & Serializer로 역할을 구분한다.

    @swagger_auto_schema(
        operation_description="유저 로그인",
        request_body=serializer_class,
        responses={
            "200": ErrorCollection().as_md(APPLY_RESPONSE),
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @transaction.atomic
    def post(self, request):
        convert_data = json.loads(request.body)

        result = AuthService().user_sign_in(
            convert_data["username"], convert_data["password"]
        )
        ## 암호 확인 로직
        ## result 결과가 True로 반환되는 경우 암호 확인 성공

        if result:
            # crypt_pw = CryptService().password_crypt(convert_data["password"])
            ## 패스워드 평문 저장이 아닌 암호화 저장을 위해 암호화 수행
            # convert_data["password"] = crypt_pw

            deserializer = SignInSerializer(data=convert_data)
            deserializer.is_valid(raise_exception=True)
            deserializer.save()

            res_code = 200

            custom_res = custom_response(res_code)

            return Response(custom_res, status=status.HTTP_201_CREATED)

        else:
            res_code = 400
            message = "ID 또는 PW가 일치하지 않습니다."
            custom_res = custom_response(res_code, message)

            return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)


# class BasicViewSet(viewsets.ModelViewSet):
#     @csrf_exempt
#     def create(self, request, pk: int = None):
#         response = {"message": "해당 기능은 활성화되지 않았습니다."}
#         return Response(response, status=status.HTTP_403_FORBIDDEN)

#     @csrf_exempt
#     def retrieve(self, request, pk: int = None):
#         response = {"message": "해당 기능은 활성화되지 않았습니다."}
#         return Response(response, status=status.HTTP_403_FORBIDDEN)

#     @csrf_exempt
#     def partial_update(self, request, pk: int = None):
#         response = {"message": "해당 기능은 활성화되지 않았습니다."}
#         return Response(response, status=status.HTTP_403_FORBIDDEN)

#     @csrf_exempt
#     def destroy(self, request, pk: int = None):
#         response = {"message": "해당 기능은 활성화되지 않았습니다."}
#         return Response(response, status=status.HTTP_403_FORBIDDEN)

#     @csrf_exempt
#     def update(self, request, pk: int = None):
#         response = {"message": "해당 기능은 활성화되지 않았습니다."}
#         return Response(response, status=status.HTTP_403_FORBIDDEN)
