# Generated by Django 4.2.1 on 2023-06-15 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='기본키 (자동 증가)')),
                ('team', models.CharField(max_length=32, verbose_name='팀 이름')),
                ('title', models.CharField(max_length=128, verbose_name='업무 제목')),
                ('content', models.CharField(max_length=128, verbose_name='하위 업무 팀')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='업무 생성 날짜')),
                ('modified_date', models.DateTimeField(null=True, verbose_name='업무 수정 날짜')),
                ('is_complete', models.BooleanField(default=False, verbose_name='업무 상태')),
                ('complete_date', models.DateTimeField(null=True, verbose_name='업무 완료 날짜')),
                ('is_delete', models.BooleanField(default=False, verbose_name='삭제 상태')),
                ('create_user', models.ForeignKey(db_column='create_user', on_delete=django.db.models.deletion.CASCADE, to='auth_app.user', verbose_name='업무 생성 유저(외래키)')),
            ],
            options={
                'db_table': 'Task',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='기본키 (자동 증가)')),
                ('team', models.CharField(max_length=32, verbose_name='하위 업무 담당 팀')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='업무 생성 날짜')),
                ('modified_date', models.DateTimeField(null=True, verbose_name='업무 수정 날짜')),
                ('is_complete', models.BooleanField(default=False, verbose_name='업무 상태')),
                ('complete_date', models.DateTimeField(null=True, verbose_name='업무 완료 날짜')),
                ('is_delete', models.BooleanField(default=False, verbose_name='삭제 상태')),
                ('relation_id', models.ForeignKey(db_column='relation_id', on_delete=django.db.models.deletion.CASCADE, to='platform_app.task', verbose_name='FK 외래키')),
            ],
            options={
                'db_table': 'SubTask',
                'managed': True,
            },
        ),
    ]
