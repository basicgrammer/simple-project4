from platform_app.models import *
from auth_app.models import *
from django.shortcuts import get_object_or_404


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

            test2 = Task.objects.filter(create_user=user_pk)

            for index in test2:
                collect_list.append(index)

            data = query[0].team
            # query2 = User.objects.all().exclude(id=user_pk)

            new = Task.objects.prefetch_related("sub_set").exclude(
                create_user=user_pk
            )

            # print(new.sub_set.filter(team=data))

            for index in new:
                if index.sub_set.filter(team=data).values_list():
                    collect_list.append(index)

            return collect_list

        else:
            # print("전체 쿼리 호출")
            query = Task.objects.all().prefetch_related("sub_set")

            return query
