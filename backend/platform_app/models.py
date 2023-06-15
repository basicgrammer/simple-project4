from django.db import models
from auth_app.models import *

# 여기에서 __all__이 의미하는 것은 * 기호를 사용하여 import할 경우 이곳에 정의된 echo 모듈만 import된다는 의미이다.

__all__ = (
    "Task",
    "SubTask",
)


class Task(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="기본키 (자동 증가)",
    )
    create_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="create_user",
        verbose_name="업무 생성 유저(외래키)",
    )
    team = models.CharField(
        max_length=32,
        verbose_name="팀 이름",
    )
    title = models.CharField(
        max_length=128,
        verbose_name="업무 제목",
    )
    content = models.CharField(
        max_length=128,
        verbose_name="하위 업무 팀",
    )
    create_date = models.DateTimeField(  ## 업무 생성은 해당 데이터를 생성하는 과정과 동시에 자동 생성
        auto_now_add=True,
        null=False,
        verbose_name="업무 생성 날짜",
    )
    modified_date = models.DateTimeField(
        null=True,
        verbose_name="업무 수정 날짜",
    )
    is_complete = models.BooleanField(
        default=False,
        verbose_name="업무 상태",
    )
    complete_date = models.DateTimeField(
        null=True,
        verbose_name="업무 완료 날짜",
    )
    is_delete = models.BooleanField(  ## True로 값이 입력된 경우 삭제된것으로 판단함.
        default=False,
        null=False,
        verbose_name="삭제 상태",
    )

    class Meta:
        managed = True
        db_table = "Task"

    def __str__(self):
        return self.title


class SubTask(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="기본키 (자동 증가)",
    )
    relation_id = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        db_column="relation_id",
        verbose_name="FK 외래키",
    )
    team = models.CharField(
        max_length=32,
        verbose_name="하위 업무 담당 팀",
    )
    create_date = models.DateTimeField(  ## 업무 생성은 해당 데이터를 생성하는 과정과 동시에 자동 생성
        auto_now_add=True,
        null=False,
        verbose_name="업무 생성 날짜",
    )
    modified_date = models.DateTimeField(
        null=True,
        verbose_name="업무 수정 날짜",
    )
    is_complete = models.BooleanField(
        default=False,
        verbose_name="업무 상태",
    )
    complete_date = models.DateTimeField(
        null=True,
        verbose_name="업무 완료 날짜",
    )
    is_delete = models.BooleanField(  ## True로 값이 입력된 경우 삭제된것으로 판단함.
        default=False,
        null=False,
        verbose_name="삭제 상태",
    )

    class Meta:
        managed = True
        db_table = "SubTask"

    def __str__(self):
        return self.team
