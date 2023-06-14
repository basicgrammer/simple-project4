#!/bin/bash

conf="--settings=config.settings.dev-setting"

echo "===== Create Specification ====="

python manage.py makemigrations auth_app "$conf"
python manage.py makemigrations platform_app "$conf"

echo "===== Create Database By Specification ====="

python manage.py migrate auth_app "$conf"
python manage.py migrate platform_app "$conf"

echo "=====  AppServer Start ====="
python manage.py runserver 0.0.0.0:80 "$conf"  # 개발용 테스트 서버 기동 (Runserver)

# gunicorn --workers=4 --bind 0.0.0.0:80 project_core.wsgi:application \  
#--access-logfile history/access.log --error-logfile history/error.log  # 프로덕션 버전 서버 기동 (Gunicorn)
