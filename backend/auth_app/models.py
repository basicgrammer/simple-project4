from django.db import models

# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone


__all__ = ("User",)


class User(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="기본키 (자동 증가)",
    )
    username = models.CharField(
        null=False,
        max_length=32,
        verbose_name="유저 ID",
    )
    password = models.CharField(
        null=False,
        max_length=128,
        verbose_name="유저 암호",
    )
    TEAM_CATEGORY = [
        ("danbi", "단비"),
        ("darae", "다래"),
        ("blah", "블라"),
        ("rail", "철로"),
        ("sloth", "해태"),
        ("ddang", "땅이"),
        ("supi", "수피"),
    ]
    team = models.CharField(
        max_length=32,
        chocies=TEAM_CATEGORY,
        default=TEAM_CATEGORY[0][0],
        null=False,
        verbose_name="소속 팀 이름",
    )

    class Meta:
        managed = True
        db_table = "User"

    def __str__(self):
        return self.title
