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

        if query_set.exists():
            pair_password = query_set[0].password
            pair_password = pair_password.encode("utf-8")

            result = bcrypt.checkpw(password.encode("utf-8"), pair_password)
            target = query_set[0]

        else:
            result = False
            target = None

        return result, target
