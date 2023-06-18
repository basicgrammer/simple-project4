from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from platform_app.models import *
from auth_app.models import *


__all__ = (
    "TaskSerializer",
    "SubTaskSerializer",
    "TaskSchema",
    "TaskRetrieveSerializer",
    "TaskUpdateSchema",
    "TaskUpdateSerializer",
    "SubTaskSemiSerializer",
    "TaskSemiSerializer",
)


class SubTaskSchema(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "pk",
            # "relation_id",
            "team",
            # "create_date",
            # "modified_date",
            # "is_complete",
            # "complete_date",
            # "is_delete",
        )


class TaskSchema(serializers.ModelSerializer):
    sub_set = SubTaskSchema(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "create_user",
            "team",
            "title",
            "content",
            "sub_set",
        )


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ("pk", "team")


class TaskSerializer(WritableNestedModelSerializer):
    sub_set = SubTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "create_user",
            "team",
            "title",
            "content",
            "sub_set",
        )


class SubTaskRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "pk",
            "team",
            "create_date",
            "modified_date",
            "is_complete",
            "complete_date",
            "is_delete",
        )


class TaskRetrieveSerializer(serializers.ModelSerializer):
    sub_set = SubTaskRetrieveSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "create_user",
            "team",
            "title",
            "content",
            "create_date",
            "modified_date",
            "is_complete",
            "complete_date",
            "sub_set",
        )


# class TaskUpdateSchema(serializers.ModelSerializer):
#     class Meta:
#         # model = Task
#         fields = (
#             "modified_user",
#             "pk",
#             "create_user",
#             "team",
#             "title",
#             "content",
#             "create_date",
#             "modified_date",
#             "is_complete",
#             "complete_date",
#             "sub_set",
#         )
class SubTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "pk",
            "team",
            "is_complete",
            "is_delete",
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    sub_set = SubTaskUpdateSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "team",
            "title",
            "content",
            "is_complete",
            "sub_set",
        )


class TaskUpdateSchema(serializers.ModelSerializer):
    sub_set = SubTaskUpdateSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "create_user",
            "team",
            "title",
            "content",
            "is_complete",
            "sub_set",
        )


class SubTaskSemiSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "pk",
            "team",
            "is_complete",
            "complete_date",
            "modified_date",
            "is_delete",
        )


class TaskSemiSerializer(WritableNestedModelSerializer):
    sub_set = SubTaskSemiSerializer(many=True)

    class Meta:
        model = Task
        fields = (
            "pk",
            "team",
            "is_complete",
            "complete_date",
            "modified_date",
            "is_delete",
            "sub_set",
        )
