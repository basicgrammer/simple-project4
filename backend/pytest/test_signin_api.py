import json
import pytest

from rest_framework.test import APIClient, APITestCase

from component import *


class SignInTestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)

    ## 테스트 시나리오 1 : 회원가입 및 로그인 기능 확인
    def test_signin_api_pase1(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(post_user_data1),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        url = "/api/signin"

        res = self.client.post(
            url,
            data=json.dumps(post_user_data2),
            content_type="application/json",
        )

        assert res.status_code == 200
        assert type(dict(res.data)) == dict

    ## 테스트 시나리오 2 : 회원가입 및 KeyError 핸들링
    def test_signin_api_pase2(self):
        url = "/api/signup"

        res = self.client.post(
            url,
            data=json.dumps(post_user_data3),
            content_type="application/json",
        )

        assert res.status_code == 201
        assert type(dict(res.data)) == dict

        url = "/api/signin"

        res = self.client.post(
            url,
            data=json.dumps(post_user_data4),
            content_type="application/json",
        )

        assert res.status_code == 400
        assert type(dict(res.data)) == dict
