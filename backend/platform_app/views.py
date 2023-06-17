import json
import copy

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema

from platform_app.serializers import *
from platform_app.models import *

from .Services.TaskService import *

from custom.custom_response import *


APPLY_RESPONSE = {
    "message": "상태 응답 메시지",
    "data": "응답에 대한 반환 데이터가 있는 경우 null을 대신하는 데이터 출력",
}


class BasicViewSet(viewsets.ModelViewSet):
    ## 일반 GET 조회 시 아래 로직이 동작함?
    queryset = Task.objects.all()
    serializer_class = TaskSchema

    @swagger_auto_schema(
        operation_description="Task 업무 생성",
        request_body=serializer_class,
        responses={
            "201": TaskSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    @transaction.atomic
    def create(self, request):
        data = json.loads(request.body)

        check, res_message = TaskService().info_match_check(
            data["create_user"], data["team"]
        )

        if check:
            serializer_class = TaskSerializer(data=json.loads(request.body))
            serializer_class.is_valid(raise_exception=True)
            task = serializer_class.save()

            new_serializer = TaskSerializer(instance=task)

            return Response(
                new_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        else:
            res_code = 400
            message = res_message

            custom_res = custom_response(res_code, message)

            return Response(
                custom_res,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_description="Task 업무 전체 조회",
        # request_body=serializer_class,
        responses={
            "200": TaskRetrieveSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    def list(self, request):
        result = TaskService().get_user_data()

        serializer = TaskRetrieveSerializer(
            instance=result, read_only=True, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Task 업무 필터 조회",
        # request_body=serializer_class,
        responses={
            "200": TaskRetrieveSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    def retrieve(self, request, pk: int = None):
        # query = User.objects.filter(id = pk)
        result = TaskService().get_user_data(pk)

        if pk is not None and result:  ## 유저 고유 ID가 None이 아닌 경우
            serializer = TaskRetrieveSerializer(
                instance=result, many=True, read_only=True
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def partial_update(self, request):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def destroy(self, request):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def update(self, request):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
