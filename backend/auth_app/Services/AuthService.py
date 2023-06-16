from auth_app.models import *

__all__ = ("AuthService",)


class AuthService:
    def duplicate_check(user_id: str) -> bool:
        query = User.objects.filter(username=user_id)

        if query.exists():
            result = True

        else:
            result = False

        return result
