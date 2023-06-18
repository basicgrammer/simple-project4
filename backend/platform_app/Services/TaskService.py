from platform_app.models import *
from auth_app.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
import copy


__all__ = ("TaskService",)


class TaskService:
    def info_match_check(self, user_pk: int, user_team: str) -> bool:
        query = User.objects.filter(id=user_pk, team=user_team)

        if query.exists():
            result = True
            message = None

        else:
            result = False
            message = "ID와 TEAM이 일치하지 않습니다."

        return result, message

    def get_user_data(self, user_pk: int = None) -> list:
        if user_pk is not None:
            collect_list = []
            ## 업무 조회 시 하위업무에 자신의 팀이 있는 경우에도 호출하게 해달라 ~
            query = User.objects.filter(id=user_pk)

            include_query = Task.objects.filter(create_user=user_pk)

            for index in include_query:
                collect_list.append(index)

            data = query[0].team
            # query2 = User.objects.all().exclude(id=user_pk)

            exclude_query = Task.objects.prefetch_related("sub_set").exclude(
                create_user=user_pk
            )

            # print(exclude_query.sub_set.filter(team=data))

            for index in exclude_query:
                if index.sub_set.filter(team=data).values_list():
                    collect_list.append(index)

            return collect_list

        else:
            # print("전체 쿼리 호출")
            query = Task.objects.all().prefetch_related(
                "sub_set"
            )  ## 전체 쿼리를 미리 호출해서 캐싱

            return query

    def condition_check(self, user_pk: int, data: dict) -> list:
        # print(data.get("pk", None))

        if data.get("pk", None) is None:
            res_code = 400
            message = "작업 수정을 위해서는 상위 업무의 고유값(PK)이 필요합니다."

        res_code = 200
        message = "None"

        return res_code, message

    def user_pair_check(self, user_pk: int, data: dict) -> int:
        query = User.objects.filter(id=user_pk)

        if query.exists():
            user_team = query[0].team

            if int(user_pk) != int(data["create_user"]):
                fix_data = copy.deepcopy(data["sub_set"])

                for num, index in enumerate(data["sub_set"]):
                    if index["team"] != user_team:
                        if len(fix_data) == len(data["sub_set"]):
                            fix_data.pop(num)

                        else:
                            fix_data.pop(num - 1)

                    else:
                        if index.get("pk", None) is None:
                            ## 하위 업무를 수정하는 경우 상위 업무가 아니기 때문에
                            ## 새로운 하위 업무를 추가하는 것은 불가능하고 수정만 가능하다.
                            return 0

                return 2, fix_data[0]

            else:  ## user_pk와 data['pk'] 가 동일한 경우이므로
                data["modified_date"] = timezone.now()

                ## is_delete 체크가 True가 되는 경우 하위 업무도 모두 True로 변경한다.

                if data["is_delete"]:
                    for index in data["sub_set"]:
                        index["is_delete"] = True

                if data["is_complete"] and data["is_delete"] == False:
                    for index in data["sub_set"]:
                        index["is_complete_date"] = True
                        index["complete_date"] = timezone.now()
                        index["modified_date"] = timezone.now()
                ## is_complete는 하위 업무가 모두 True인 경우 True로 변경된다.

                return 1, data
                ##상위 및 하위 업무에 관련된 작업을 모두 수행할 수 있음

        else:
            return 0, None

        ## return은 3가지
        ## 1 : 상위업무 수정, 2 : 하위 업무 수정, 3 : 둘다 수정 가능한 상태

        return True

    def task_update(self, fix_data: dict) -> dict:
        query = Task.objects.filter(id=fix_data["pk"])

        return fix_data, query[0]

    def subtask_update(self, fix_data: list) -> dict:
        fix_data["modified_date"] = timezone.now()

        query = SubTask.objects.filter(id=fix_data["pk"])

        if fix_data["is_complete"] and query[0].is_complete == False:
            fix_data["complete_date"] = timezone.now()

        elif fix_data["is_complete"] and query[0].is_complete:
            ## 둘다 True인 경우 추가 작업을 할 필요는 없음
            pass

        else:
            fix_data["complete_date"] = None

        return fix_data, query[0]

    def team_count(self, data: list) -> bool:
        team_list = [
            "danbi",
            "darae",
            "blah",
            "rail",
            "sloth",
            "ddang",
            "supi",
        ]
        count_list = [0] * len(team_list)

        for index in data["sub_set"]:
            if index["team"] and index["is_delete"] == False:
                count_list[team_list.index(index["team"])] += 1

                if count_list[team_list.index(index["team"])] > 1:
                    return False

        return True
