import json
import copy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils import timezone
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, generics, status, mixins

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


## -------------------------------------------------------------------
class SignUpView(APIView):
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

            deserializer = self.serializer_class(  ## 역직렬화 수행
                data=convert_data,
            )
            deserializer.is_valid(
                raise_exception=True
            )  ## 유효성 검사 및 문제 발생 시 raise_exception
            deserializer.save()

            res_code = 201

            custom_res = custom_response(res_code)

            return Response(custom_res, status=status.HTTP_201_CREATED)

        else:
            res_code = 400
            message = "중복되는 ID가 존재합니다."
            custom_res = custom_response(res_code, message)

            return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)


## -------------------------------------------------------------------
class SignInView(mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = SignInSchema

    @swagger_auto_schema(
        operation_description="유저 로그인",
        request_body=serializer_class,
        responses={
            "200": ErrorCollection().as_md(APPLY_RESPONSE),
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @transaction.atomic
    def patch(self, request):
        convert_data = json.loads(request.body)

        result, target = AuthService().user_sign_in(
            convert_data["username"], convert_data["password"]
        )
        ## 암호 확인 로직 (bcrypt 라이브러리 기반의 암호 체크)
        ## result 결과가 True로 반환되는 경우 암호 확인 성공

        if result:
            # 로그인 시 last_login 업데이트 필요

            # convert_data["id"] = pk_id
            convert_data["last_login"] = timezone.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            convert_data.pop("password", None)  ## 키 제거 시 키가 없는 경우 None 반환

            deserializer = SignInSerializer(
                target, data=convert_data, partial=True
            )
            deserializer.is_valid(raise_exception=True)
            deserializer.save()
            # self.partial_update(deserializer)

            res_code = 200
            custom_res = custom_response(res_code)

            return Response(custom_res, status=status.HTTP_201_CREATED)

        else:
            res_code = 400
            message = "ID 또는 PW가 일치하지 않습니다."
            custom_res = custom_response(res_code, message)

            return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)
