from auth_app.models import *
import bcrypt

__all__ = ("AuthService",)


class AuthService:
    def duplicate_check(self, user_id: str) -> bool:
        query = User.objects.filter(username=user_id)

        if query.exists():
            result = False

        else:
            result = True

        return result

    def user_sign_in(self, user_id: str, password: str) -> bool:
        query_set = User.objects.filter(username=user_id)

        # test, test2 = query_set[0].password, query_set[0].id

        if query_set.exists():
            pair_password = query_set[0].password.encode("utf-8")

            result = bcrypt.checkpw(password.encode("utf-8"), pair_password)
            target = query_set[0].id
            # target2 = query_set[0].id ## 캐싱이 되지 않기 때문에 계속해서 SQL을 호출하는 것을 볼 수 있다.
            # target3 = query_set[0].id ## 이러한 영역들을 최소화해서 성능을 최대로 끌어올려야한다.

        else:
            result = False
            target = None

        return result, target
