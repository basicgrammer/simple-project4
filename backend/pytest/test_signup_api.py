import json
import pytest


from rest_framework.test import APIClient, APITestCase

from component import *


class SignUpTestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)

    ## 테스트 시나리오 1 : 회원 가입 기능 확인
    def test_signup_api_pase1(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data1),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

    ## 테스트 시나리오 2 : 중복 ID 체크 기능 확인
    def test_signup_api_pase2(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data2),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data2),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict

    ## 테스트 시나리오 3 : KeyError 에러 핸들링 확인
    def test_signup_api_pase3(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(create_user_data3),
            content_type="application/json",
        )
        assert res.status_code == 400
        assert type(dict(res.data)) == dict
