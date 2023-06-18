import json

__all__ = (
    "ClientRequest",
    "create_user_data1",
    "create_user_data2",
    "create_user_data3",
    "create_user_data4",
    "create_user_data5",
    "create_user_data6",
    "post_user_data1",
    "post_user_data2",
    "post_user_data3",
    "post_user_data4",
    "task_create_data1",
    "task_create_data2",
    "task_create_data3",
)


class ClientRequest:
    def __init__(self, client):
        self.client = client

    def __call__(self, type, url, data=None):
        content_type = "application/json"

        if type == "get":
            res = self.client.get(
                url,
                content_type=content_type,
            )

        elif type == "post":
            res = self.client.post(
                url, json.dumps(data), content_type=content_type
            )

        elif type == "patch":
            res = self.client.patch(
                url, json.dumps(data), content_type=content_type
            )

        else:
            pass


## Method [POST] - signup API
## ------------------------------------------------------------------
## 회원가입 시나리오
create_user_data1 = {
    "username": "testuser1",
    "password": "user123!",
    "team": "danbi",
}

## 중복 체크 시나리오
create_user_data2 = {
    "username": "testuser2",
    "password": "user123!",
    "team": "rail",
}

## KeyError 누락 시나리오
create_user_data3 = {
    "username": "testuser3",
    # "password": "user123!",
    "team": "ddang",
}

create_user_data4 = {
    "username": "testuser27",
    "password": "user123!",
    "team": "ddang",
}

create_user_data5 = {
    "username": "testuser117",
    "password": "user123!",
    "team": "danbi",
}


create_user_data6 = {
    "username": "testuser154",
    "password": "user123!",
    "team": "danbi",
}


## Method [POST] - signin API
## ------------------------------------------------------------------
## 회원가입 시나리오
post_user_data1 = {
    "username": "testuser19",
    "password": "user123!",
    "team": "rail",
}

## 로그인 시나리오
post_user_data2 = {
    "username": "testuser19",
    "password": "user123!",
}

## 회원가입 시나리오
post_user_data3 = {
    "username": "testuser23",
    "password": "user123!",
    "team": "darae",
}

## KeyError Handling 시나리오
post_user_data4 = {
    "username": "testuser23",
}

## Method [POST] - TaskCreateAPI
## ------------------------------------------------------------------
## 작업 생성 시나리오
task_create_data1 = {
    "create_user": 1,
    "team": "danbi",
    "title": "테스트 시나리오 1",
    "content": "테스트 시나리오 1",
    "sub_set": [
        {"team": "danbi"},
        {"team": "rail"},
        {"team": "ddang"},
    ],
}

## KeyError 확인 시나리오
task_create_data2 = {
    "create_user": 1,
    "team": "darae",
    "title": "테스트 시나리오 2",
    "content": "테스트 시나리오 2",
    "sub_set": [
        {"team": "danbi"},
        {"team": "rail"},
        {"team": "ddang"},
    ],
}


## 유저 정보가 매칭되지 않는 없는 경우 시나리오

task_create_data3 = {
    "create_user": 1,
    "team": "danbi",
    "title": "string",
    "content": "string",
    "sub_set": [{"team": "danbi"}],
}


## Method [Patch] - TaskPatchAPI
## ------------------------------------------------------------------

## 유저 2명이 필요, 이유는 서로 페어처리를 통해 각자의
task_patch_data1 = {}

## 중복 체크 시나리오
task_user_data1 = {
    "username": "testuser500",
    "password": "user123!",
    "team": "rail",
}

task_user_data2 = {
    "username": "testuser200",
    "password": "user123!",
    "team": "rail",
}
