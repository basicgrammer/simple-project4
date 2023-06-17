# Generated by Django 4.2.1 on 2023-06-17 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platform_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='relation_id',
            field=models.ForeignKey(db_column='relation_id', on_delete=django.db.models.deletion.CASCADE, related_name='sub_set', related_query_name='sub', to='platform_app.task', verbose_name='FK 외래키'),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='team',
            field=models.CharField(choices=[('danbi', '단비'), ('darae', '다래'), ('blah', '블라'), ('rail', '철로'), ('sloth', '해태'), ('ddang', '땅이'), ('supi', '수피')], default='danbi', max_length=32, verbose_name='하위 업무 담당 팀'),
        ),
        migrations.AlterField(
            model_name='task',
            name='team',
            field=models.CharField(choices=[('danbi', '단비'), ('darae', '다래'), ('blah', '블라'), ('rail', '철로'), ('sloth', '해태'), ('ddang', '땅이'), ('supi', '수피')], default='danbi', max_length=32, verbose_name='팀 이름'),
        ),
    ]
