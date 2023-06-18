import json
import pytest

from rest_framework.test import APIClient, APITestCase

from component import *


class TaskCreateTestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)

    ## 테스트 시나리오 1 : 유저 ID 등록 and 작업 등록
    def test_taskcreate_api_pase1(self):
        ## --------- 유저 ID 등록 ---------------
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data1),
            content_type="application/json",
        )

        origin_res = res

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## --------------- 등록된 유저를 통해 작업 등록 테스트

        url = "/api/task/"

        custom_data = task_create_data1
        custom_data["create_user"] = origin_res.data["id"]
        custom_data["team"] = origin_res.data["team"]

        res = self.client.post(
            url,
            data=json.dumps(custom_data),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## ------------------ 작업 등록 시 유저 정보 체크 확인
        url = "/api/task/"

        custom_data2 = task_create_data2
        custom_data2["create_user"] = origin_res.data["id"]

        res = self.client.post(
            url,
            data=json.dumps(custom_data2),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict

        ## ------------------- 작업 등록 시 필드가 빠진 경우 에러 발생 확인
        url = "/api/task/"

        custom_data3 = task_create_data2
        custom_data3["create_user"] = origin_res.data["id"]
        custom_data3["team"] = origin_res.data["team"]
        custom_data3.pop("content")

        res = self.client.post(
            url,
            data=json.dumps(custom_data3),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict

        ## ------------------- 작업 등록  KeyError 확인
        url = "/api/task/"

        custom_data2 = task_create_data2
        custom_data2["create_user"] = origin_res.data["id"]
        custom_data2["team"] = origin_res.data["team"]
        custom_data2.pop("team")

        res = self.client.post(
            url,
            data=json.dumps(custom_data2),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict
