import json
import copy

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from platform_app.serializers import *
from platform_app.models import *


class BasicViewSet(viewsets.ModelViewSet) :

    @csrf_exempt    
    def create(self, request) -> "Res Code, Res Data(JSON)" :  # 생성을 위해서 선언
        
        data = json.loads(request.body)  # 1. 입력 데이터 파싱
        
        serializer_class = ProductSerializer(data = data)  # 2. 직렬화를 위한 데이터 주입
        serializer_class.is_valid(raise_exception = True)
        product = serializer_class.save()   

        new_serializer = ProductSerializer(instance = product)  # 3. 역직렬화를 위한 데이터 주입

        return Response(new_serializer.data, status = 201)


    @csrf_exempt
    def retrieve(self, request, pk:int=None) -> "Res Code, Res Data(List)" :  # 조회를 위해 선언

        try : 
            if pk is not None :  # pk 값이 존재하는 경우 필터링된 정보만 반환
                queryset = Product.objects.filter(id = pk)
                serializer = ProductSerializer(queryset[0])

            else : 
                serializer = ProductSerializer(queryset[0])  # pk 값이 존재하지 않는 경우 모든 정보 반환

            return Response(serializer.data, status = 200)
        
        except :

            message = {
                    "message" : "업데이트 할 수 있는 데이터가 없습니다."
            }

            return Response(message, status = 200)


    @csrf_exempt
    def partial_update(self, request, pk:int) -> "res code, res data(json)" :  # 부분 업데이트를 위해 선언

        data = json.loads(request.body)
        queryset = Product.objects.filter(id = pk)

        if queryset.exists() :

            serializer_class = ProductSerializer(queryset[0], data = data, partial = True)
            serializer_class.is_valid(raise_exception = True)
            serializer_class.save()

            product = serializer_class.save()
            new_serializer = ProductSerializer(instance = product)

            return Response(new_serializer.data, status = 200)

        else :
            
            message = {
                "message" : "업데이트가 가능한 데이터가 존재하지 않습니다."
            }

            return Response(message, status = 400)
    @csrf_exempt
    def create(self, request, pk:int=None):
        response = {'message': '해당 기능은 활성화되지 않았습니다.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def retrieve(self, request, pk:int=None):
        response = {'message': '해당 기능은 활성화되지 않았습니다.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def partial_update(self, request, pk:int=None):
        response = {'message': '해당 기능은 활성화되지 않았습니다.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    

    @csrf_exempt
    def destroy(self, request, pk:int=None):
        response = {'message': '해당 기능은 활성화되지 않았습니다.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def update(self, request, pk:int=None):
        response = {'message': '해당 기능은 활성화되지 않았습니다.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)