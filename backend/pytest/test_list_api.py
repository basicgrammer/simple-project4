import json
import pytest

from rest_framework.test import APIClient, APITestCase

from component import *


class TaskListTestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)

    ## 테스트 시나리오 1 : 유저 ID 등록 and 작업 등록
    def test_taskcreate_api_pase1(self):
        ## --------- 유저 ID 등록 ---------------
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data4),
            content_type="application/json",
        )

        origin_res = res

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## --------------- 등록된 유저를 통해 작업 등록 테스트

        url = "/api/task/"

        custom_data = task_create_data2
        custom_data["create_user"] = origin_res.data["id"]
        custom_data["team"] = origin_res.data["team"]

        res = self.client.post(
            url,
            data=json.dumps(custom_data),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        ## ------------ 전체 업무 데이터 호출
        url = "/api/task/"

        res = self.client.get(
            url,
            content_type="application/json",
        )

        assert res.status_code == 200
        assert type(list(res.data)) == list

        ## ------------- 필터링 업무 데이터 호출

        url = "/api/task/"

        res = self.client.get(
            url,
            params=origin_res.data["id"],
            content_type="application/json",
        )

        assert res.status_code == 200
        assert type(list(res.data)) == list
