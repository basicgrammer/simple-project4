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
            message = "ID와 TEAM 정보가 일치하지 않습니다."

        return result, message

    def get_user_data(self, user_pk: int = None) -> list:
        ## user_pk는 유저의 고유 pk임
        if user_pk is not None:
            collect_list = []
            ## 업무 조회 시 하위업무에 자신의 팀이 있는 경우에도 호출하게 해달라 ~
            query = User.objects.filter(id=user_pk)

            include_query = Task.objects.filter(
                create_user=user_pk, is_delete=False
            )

            for index in include_query:
                collect_list.append(index)

            data = query[0].team
            # query2 = User.objects.all().exclude(id=user_pk)

            exclude_query = Task.objects.prefetch_related("sub_set").exclude(
                create_user=user_pk
            )

            # print(exclude_query.sub_set.filter(team=data))

            for index in exclude_query:
                if index.sub_set.filter(
                    team=data, is_delete=False
                ).values_list():
                    collect_list.append(index)

            return collect_list

        else:
            # print("전체 쿼리 호출")
            query = Task.objects.filter(is_delete=False).prefetch_related(
                "sub_set"
            )  ## 전체 쿼리를 미리 호출해서 캐싱

            return query

    def condition_check(self, user_pk: int, data: dict) -> list:
        if data.get("pk", None) is None:
            res_code = 400
            message = "작업 수정을 위해서는 상위 업무의 고유값(PK)이 필요합니다."

        res_code = 200
        message = "None"

        return res_code, message

    def user_pair_check(self, user_pk: int, data: dict) -> int:
        query = User.objects.filter(id=user_pk)

        ## return은 3가지로 반환받음
        ## 1 : 상위업무 수정, 2 : 하위 업무 수정, 3 : 둘다 수정 가능한 상태

        if query.exists():  ## 유저에 대한 쿼리가 존재하는 경우에만 처리 로직을 수행한다.
            user_team = query[0].team  ## 수정을 진행하는 유저의 팀 정보

            if int(user_pk) != int(data["create_user"]):
                ## 수정을 요청하는 유저와 상위 업무의 유저 정보가 동일하지 않는다면 하위 업무만 수정하게 된다.
                ## 아래 로직은 상위 업무를 배제하고, 하위 업무만을 수행시킨다.
                fix_data = copy.deepcopy(data["sub_set"])

                print

                for num, index in enumerate(fix_data):
                    if index["team"] == user_team:
                        # target_num = num
                        # target_list.append(fix_data[target_num])

                        if index.get("pk", None) is None:
                            return 0

                    else:
                        index.pop("team")
                        index.pop("is_complete")
                        index.pop("is_delete")
                        if index.get("pk", None) is None:
                            return 0

                return 2, fix_data

            else:  ## user_pk와 data['pk'] 가 동일한 경우 (상위와 하위에 모두 업무가 존재할 수 있음)
                query = SubTask.objects
                fix_data = copy.deepcopy(data)
                fix_data["modified_date"] = timezone.now()

                ## is_delete 체크가 True가 되는 경우 하위 업무도 모두 True로 변경한다.

                # if fix_data["is_delete"]:
                #     for index in fix_data["sub_set"]:
                #         index["is_delete"] = True

                # if fix_data["is_complete"] and fix_data["is_delete"] == False:
                #     for index in fix_data["sub_set"]:
                #         index["is_complete_date"] = True
                #         index["complete_date"] = timezone.now()
                #         index["modified_date"] = timezone.now()
                ## is_complete는 하위 업무가 모두 True인 경우 True로 변경된다.

                # fix_data = copy.deepcopy(data["sub_set"])

                for num, index in enumerate(fix_data["sub_set"]):
                    if index["team"] == user_team:
                        if index.get("pk", None) is None:
                            return 0

                    else:
                        query = SubTask.objects.get(id=index["pk"])
                        index["team"] = query["team"]
                        index["modified_date"] = timezone.now()

                        if (
                            query["is_delete"] == False
                            and fix_data["is_delete"]
                        ):
                            index["is_delete"] = True
                        else:
                            index["is_delete"] = query["is_delete"]

                        if (
                            query["is_complete"] == False
                            and fix_data["is_complete"]
                        ):
                            fix_data["complete_date"] = timezone.now()
                            index["is_complete"] = True
                            index["complete_date"] = timezone.now()
                        else:
                            index["is_complete"] = query["is_complete"]

                        if index.get("pk", None) is None:
                            return 0

                # data["sub_set"] = target_list

                return 1, fix_data
                ##상위 및 하위 업무에 관련된 작업을 모두 수행할 수 있음

        else:  ## 유저에 대한정보가 존재하지 않으므로 400 에러를 발생시킨다.
            return 0, None

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
