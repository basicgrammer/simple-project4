## 기본
import json
import copy

## 서드파티
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

## 로컬
from platform_app.serializers import *
from platform_app.models import *
from .Services.TaskService import *
from custom.custom_response import *


APPLY_RESPONSE = {
    "message": "상태 응답 메시지",
    "data": "응답에 대한 반환 데이터가 있는 경우 null을 대신하는 데이터 출력",
}


class BasicViewSet(viewsets.ModelViewSet):  ## REST API 구성을 위해 ModelViewSet 활용
    queryset = Task.objects.all()
    serializer_class = TaskSchema

    ## -------------------------------------------------------------------
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
    def create(self, request):  ## Create API
        data = json.loads(request.body)

        try:
            check, res_message = TaskService().info_match_check(
                data["create_user"], data["team"]
            )

            check2 = TaskService().team_count(data)
            if check2 == False:
                res_code = 400
                message = "하위 업무 설정에서 팀 이름이 중복됩니다."
                custom_res = custom_response(res_code, message)

                return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)

            if check:
                deserializer = TaskSerializer(data=data)
                deserializer.is_valid(raise_exception=True)
                instance = deserializer.save()

                serializer = TaskSerializer(instance=instance)

                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )

            else:
                res_code = 400
                message = res_message

                custom_res = custom_response(res_code, message)

                return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            res_code = 400
            message = "요청 데이터가 누락되었습니다.!!"
            custom_res = custom_response(res_code, message)

            return Response(custom_res, status=status.HTTP_400_BAD_REQUEST)

    ## -------------------------------------------------------------------
    @swagger_auto_schema(
        operation_description="Task 업무 전체 조회",
        responses={
            "200": TaskRetrieveSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    def list(self, request):  ## List API
        result = TaskService().get_user_data()

        serializer = TaskRetrieveSerializer(
            instance=result, read_only=True, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    ## -------------------------------------------------------------------
    @swagger_auto_schema(
        operation_description="Task 업무 필터 조회",
        # request_body=serializer_class,
        responses={
            "200": TaskRetrieveSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    def retrieve(self, request, pk: int = None):  ## Retrieve API
        # query = User.objects.filter(id = pk)
        result = TaskService().get_user_data(pk)

        if pk is not None and result:  ## 유저 고유 ID가 None이 아닌 경우
            serializer = TaskRetrieveSerializer(
                instance=result, many=True, read_only=True
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    ## -------------------------------------------------------------------
    @swagger_auto_schema(
        operation_description="Task 업무 수정",
        request_body=TaskUpdateSchema,
        responses={
            "200": TaskUpdateSerializer,
            "400": ErrorCollection().as_md(APPLY_RESPONSE),
        },
    )
    @csrf_exempt
    @transaction.atomic
    def partial_update(self, request, pk: int):  ##Patch API
        data = json.loads(request.body)

        ## 요청 데이터의 상위 업무에 PK값이 부재하는 경우 에러 발생시킴
        res_code, message = TaskService().condition_check(pk, data)

        if res_code == 400:
            custom_res = custom_response(res_code, message)

            return Response(
                custom_res,
                status=status.HTTP_400_BAD_REQUEST,
            )

        ## 유저 인증 및 수정을 위한 데이터만 따로 적출하는 작업을 수행한다.
        result, fix_data = TaskService().user_pair_check(pk, data)

        if result == 0:
            res_code = 400
            message = "등록되지 않은 유저가 수정할 수 없습니다."

            custom_res = custom_response(res_code, message)

            return Response(
                custom_res,
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif result == 2:
            ## 하위 업무의 경우 하위 업무만 적출해서 처리한다.
            subtask_data, target = TaskService().subtask_update(fix_data)

            deserializer = SubTaskSemiSerializer(
                target,
                data=subtask_data,
                partial=True,
            )
            if deserializer.is_valid():
                instance = deserializer.save()
                serializer = SubTaskSemiSerializer(instance=instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

        elif result == 1:
            print(data)
            team_check = TaskService().team_count(data)
            ## 상위 업무를 포함한 하위 업무를 모두 저장한다.
            task_data, target = TaskService().task_update(fix_data)

            if team_check:
                deserializer = TaskSemiSerializer(
                    target,
                    data=task_data,
                    partial=True,
                )

                if deserializer.is_valid():
                    instance = deserializer.save()
                    serializer = TaskSemiSerializer(instance=target)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                res_code = 400
                message = "하위 업무에서 중복되는 팀이 존재합니다."

                custom_res = custom_response(res_code, message)

                return Response(
                    custom_res,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # serializer = TaskUpdateSerializer(data=data, partial=True)
        # if serializer.is_valid():
        #     print("유효성 검증 확인")

        # response = {"message": "기능 활성화 완료"}
        # return Response(response, status=status.HTTP_200_OK)

    ## -------------------------------------------------------------------
    @swagger_auto_schema(
        operation_description="해당 API Method는 사용하지 않습니다.",
    )
    @csrf_exempt
    def destroy(self, request, pk: int):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    ## -------------------------------------------------------------------
    @swagger_auto_schema(
        operation_description="해당 API Method는 사용하지 않습니다.",
    )
    @csrf_exempt
    def update(self, request, pk: int):
        response = {"message": "해당 기능은 활성화되지 않았습니다."}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
