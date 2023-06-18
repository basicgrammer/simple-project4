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
            data=json.dumps(create_user_data5),
            content_type="application/json",
        )

        origin_res = res.data

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## --------------- 등록된 유저를 통해 작업 등록 테스트

        url = "/api/task/"

        custom_data = task_create_data1
        custom_data["create_user"] = origin_res["id"]
        custom_data["team"] = origin_res["team"]
        print(custom_data)

        res = self.client.post(
            url,
            data=json.dumps(custom_data),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

    def test_taskcreate_api_phase2(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data6),
            content_type="application/json",
        )

        origin_res = res.data

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## ------------------ 작업 등록 시 유저 정보 체크 확인
        url = "/api/task/"

        custom_data = task_create_data2
        custom_data["create_user"] = origin_res["id"]

        res = self.client.post(
            url,
            data=json.dumps(custom_data),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict

    def test_taskcreate_api_phase3(self):
        ## ------------------- 작업 등록 시 필드가 빠진 경우 에러 발생 확인

        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data7),
            content_type="application/json",
        )

        origin_res = res.data

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        url = "/api/task/"

        custom_data = task_create_data3
        custom_data["create_user"] = origin_res["id"]
        custom_data["team"] = origin_res["team"]
        custom_data.pop("content")

        res = self.client.post(
            url,
            data=json.dumps(custom_data),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict

    # def test_taskcreate_api_phase4(self):
    #     ## ------------------- 작업 등록  KeyError 확인

    #     url = "/api/signup"

    #     res = self.client.post(
    #         url,
    #         data=json.dumps(create_user_data8),
    #         content_type="application/json",
    #     )

    #     origin_res = res.data

    #     assert res.status_code == 201
    #     assert type(dict(res.data)) == dict

    #     url = "/api/task"

    #     custom_data = task_create_data4
    #     custom_data["create_user"] = origin_res["id"]
    #     custom_data["team"] = origin_res["team"]
    #     custom_data.pop("team")

    #     res = self.client.post(
    #         url,
    #         data=json.dumps(custom_data),
    #         content_type="application/json",
    #     )

    #     assert res.status_code == 400
    #     assert type(dict(res.data)) == dict
