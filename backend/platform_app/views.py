import json
import copy

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from platform_app.serializers import *
from platform_app.models import *


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
