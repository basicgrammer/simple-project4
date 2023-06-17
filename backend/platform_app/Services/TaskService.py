from platform_app.models import *
from auth_app.models import *

__all__ = ("TaskService",)


class TaskService:
    def info_match_check(user_pk: int, user_team: str) -> bool:
        query = User.objects.filter(id=user_pk, team=user_team)

        if query.exists():
            result = True
            message = None

        else:
            result = False
            message = "ID와 TEAM이 일치하지 않습니다."

        return result, message

    def get_user_data(self, user_pk: int = None) -> list:
        print("GET USER DATA")
        if user_pk is not None:
            query = User.objects.filter(id=user_pk)

            # print("필터 쿼리 호출")

            if query.exists():
                return query

            else:
                return None

        else:
            # print("전체 쿼리 호출")
            query = User.objects.all()

            return query
