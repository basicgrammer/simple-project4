### 버전 정보

- ![python](https://img.shields.io/badge/Python:3.8-03776AB?style=flat&logo=Python&logoColor=white)
- ![Django](https://img.shields.io/badge/Django:4.2.1-092E20?style=flat&logo=Django&logoColor=white)
- ![Postgres](https://img.shields.io/badge/Postgres:13-4169E1?style=flat&logo=Postgres&logoColor=white)

## pip library list

```shell

asgiref             3.7.2
bcrypt              4.0.1
coverage            7.2.7
Django              4.2.1
django-environ      0.10.0
djangorestframework 3.14.0
drf-writable-nested 0.7.0
drf-yasg            1.21.6
exceptiongroup      1.1.1
inflection          0.5.1
iniconfig           2.0.0
packaging           23.1
pip                 23.0.1
pluggy              1.0.0
psycopg             3.1.9
psycopg-binary      3.1.9
pytest              7.3.1
pytest-cov          4.0.0
pytest-django       4.5.2
pytz                2023.3
PyYAML              6.0
setuptools          58.1.0
sqlparse            0.4.4
tomli               2.0.1
typing_extensions   4.6.3
uritemplate         4.1.1
wheel               0.40.0

```

---

### 구동 환경

- OS : Ubuntu 22.04 LTS
- CPU : 8 vCPU
- Memory : 16G
- Docker Engine : Docker version 23.0.3, build 3e7cbfd
- docker-commpose : Docker Compose version v2.13.0

---

### 컨테이너 환경 구동 명령어셋

- 참고 : 원만한 구동을 위해 env 파일을 포함해서 첨부합니다.

#### 컨테이너 기동

```shell
# docker-compose.yml 명세를 활용할 수 있는 디렉토리 위치에서 아래 명령을 실행해주세요.

# 명세 기반 다중 컨테이너의 빌드 및 백그라운드 구동
$ sudo docker-compose up --build -d

# 명세 기반 다중 컨테이너의 이미지 신규 빌드 및 백그라운드 구동
$ sudo docker-compose up --build -d --force-recreate
```

#### 컨테이너 기동 중지 및 일시 정지

```shell
# 명세 기반 다중 컨테이너 정지
$ sudo docker-compose down

# 일부 컨테이너 일시 정지
$ sudo docker-compose stop {container_name}
```

#### 컨테이너 로그 확인

```shell
# 컨테이너 로그 모니터링
$ sudo docker logs {container_name}

# 컨테이너 지속적인 로그 모니터링
$ sudo docker logs --tail 1000 -f {container_name}
```

#### 컨테이너 환경 접속

```shell
# django
$ sudo docker exec -it {container_name} /bin/bash

# mysql
$ sudo docker exec -it {container_name} /bin/bash
```

#### docker-compose 명세 보기

```shell
$ sudo docker-compose config
```

#### 컨테이너 자원 활용 모니터링

```shell
$ sudo docker stats
```

---

### API Document

- URL : http://{IP}/swagger

### 변경 및 도입 정보

- psycopg2가 desperated가 될 수 있다는 문장이 언급되므로 psycopg[binary]에서 3버전을 설치한다.
- psycopg2 vs psycopg3의 성능 차이는 아래 링크를 참고하자 (3 초기 버전의 벤치마크라서 성능 최적화가 덜 되었다는 말이 있으나 3.1 버전에서 성능 최적화가 되었을 것이라고 본다.)
- URL : https://www.spherex.dev/psycopg-2-vs-psycopg3/

- django-environ 라이브러리 도입

  - django setting의 환경 변수 관리를 위한 env를 도입

- drf-writable-nested 라이브러리 도입
  - 중첩 구조의 데이터 저장을 위해 해당 라이브러리를 도입
  - 기존 Serializer은 중첩 구조 저장이 아닌 읽기 작업만을 허용함 (read only)

---

### 제약 사항

- 개발환경

  - Python 3.9 이상
  - django 3.2 이상
  - DRF 3.0 이상

- Django 및 DRF를 이용해서 구현할 것
- Database는 자유롭게 이용 가능
- Restful API로 구현할 것
- 테스트 코드를 작성할 것

### 고려중

- 기본으로 제공되는 Auth 기능을 사용할 필요가 있을까?

  - 기본으로 제공되는 Auth를 사용하면 간단하게 로그인, 로그아웃 등을 고려할 수 있지만, 요구사항을 살펴보면 Auth 기능을 사용하기 위해 활성화하는 테이블들을 죽이는 것이 더 효율적일 수 도 있다.
  - Auth 모델을 베이스로 확장하는 AbstractUser을 꼭 사용하지 않는 방식으로 고려한다.

- Auth를 사용하지 않는 경우 기본으로 지원되었던 createsuperuser 같은 커맨드 방식은 어떻게 할 것인가?

  - Django도 얼마든지 커스텀 커맨드를 만들 수 있으므로 해당 방식을 적용하는 것이 좋다고 본다.
  - https://geminihoroscope.tistory.com/142

- Team이라는 구성 단위가 있으나, 요구사항 명세서에는 Team에 대한 추가적인 테이블 구조가 언급된 부분이 없다.

  - Team이라는 테이블을 생성하거나, 다른 방법을 고려해야한다.
  - Team이 7개로 정해졌으며 테이블을 추가로 생성하기 보다, 유저 테이블에 병합하는것이 DB의 성능을 고려했을때 더 좋다고 판단된다.
  - 최종결정 : Team 테이블을 생성하지 않고 choices 기능을 기반으로 활용해서 팀 컬럼을 추가하기로 결정

- Github Action을 활용한 테스트 수행

- 테스트 코드의 커버리지 검사를 위한 Codecov 도입

- Pytest를 활용한 테스트코드 수행

### 해결해야하는 문제

- 로그인 API Query 캐싱 문제

  - evaluate 같은 all()이 아닌 filter로 가져오는 특수한 경우에는 어떤식으로 캐싱을 해서 DB Hit 수를 줄여야함.
  - queryset[0].id & queryset[0].password를 가져오는 부분이 있기에 둘은 같은 쿼리를 호출하지만, 값을 재활용하는 캐싱이 되지 않기 때문에 DB에 호출을 2번을 하게 된다.
  - 캐시가 잘못되어 잘못된 데이터가 나오는 위험성을 감수하고 적용할 필요가 있는지 고려가 필요함

- 팀 체크 로직 추가 필요
  - ~~팀을 추가하는 영역이 테이블로 구성된 방식이 아니기 때문에, 팀 추가 시 팀이름 유효성에 대해 검증하는 기능이 필요함~~
  - 해당 문제를 해결하기 위해 7개의 팀으로 구성된 리스트와 그에 1:1 매핑되는 리스트의 원소의 초기값을 0으로 지정하여 카운트 하는 방식으로 유효성 검사 진행

### API 목록

- 회원가입
- 로그인
- 업무 등록 (REST API로 등록 ~ 조회까지 묶어서 하나의 URL로 처리)
- 업무 수정 and 삭제 (소프트 삭제를 사용할 예정이므로, 수정 기능에서 삭제 기능을 함께 구현함)
- 업무 조회

### 테스트코드 커버리지

<img width="1271" alt="image" src="https://github.com/basicgrammer/simple-project4/assets/55322993/ecde6275-d60b-4102-a5c8-1ecdb6271d2f">

### Github Action을 활용한 테스트코드 자동화

<img width="929" alt="image" src="https://github.com/basicgrammer/simple-project4/assets/55322993/7f117230-8f81-4af0-ae70-39268d34f95c">

### Pytest 자동화

```shell
  # pytest.ini
  [pytest]
  DJANGO_SETTINGS_MODULE = config.pytest_settings
  # DJANGO_SETTINGS_MODULE = config.settings
  python_files = test_*.py
```

- GitHub Action에서 Pytest를 수행하는 경우 가상환경을 고려하여 DJNAGO_SETTINGS_MODULE을 config.pytest_settings로 해야한다.
- 컨테이너 구동 환경에서는 DJANGO_SETTINGS_MODULE을 config.settings로 전환하면 된다.

### 현행 문제

- 업무 수정 (patch)의 버그가 수정되지 않았기에 업무 수정 API가 정상적으로 동작하지 않음
- Pytest에서도 업무 수정 API에 관련된 테스트는 배제하도록 처리해둠
- 추후 고려하여 코드를 개편할 예정
