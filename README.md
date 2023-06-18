### 버전 정보

- ![python](https://img.shields.io/badge/Python3.8-03776AB?style=flat&logo=Python&logoColor=white)

- Django : 4.2.1
- Postgres : 13

## pip library 정보

```shell
  asgiref             3.7.2
  bcrypt              4.0.1
  Django              4.2.1
  django-environ      0.10.0
  djangorestframework 3.14.0
  drf-writable-nested 0.7.0
  drf-yasg            1.21.6
  inflection          0.5.1
  packaging           23.1
  pip                 23.0.1
  psycopg             3.1.9
  psycopg-binary      3.1.9
  pytz                2023.3
  PyYAML              6.0
  setuptools          58.1.0
  sqlparse            0.4.4
  typing_extensions   4.6.3
  uritemplate         4.1.1
  wheel               0.40.0

```

### 변경 및 도입 정보

- psycopg2가 desperated가 될 수 있다는 문장이 언급되므로 psycopg[binary]에서 3버전을 설치한다.
- psycopg2 vs psycopg3의 성능 차이는 아래 링크를 참고하자 (3 초기 버전의 벤치마크라서 성능 최적화가 덜 되었다는 말이 있으나 3.1 버전에서 성능 최적화가 되었을 것이라고 본다.)
- URL : https://www.spherex.dev/psycopg-2-vs-psycopg3/

- django-environ 도입
  - django setting의 환경 변수 관리를 위한 env를 도입

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
  - 팀을 추가하는 영역이 테이블로 구성된 방식이 아니기 때문에, 팀 추가 시 팀이름 유효성에 대해 검증하는 기능이 필요함

### API 목록

- 회원가입
- 로그인
- 업무 등록 (REST API로 등록 ~ 조회까지 묶어서 하나의 URL로 처리)
- 업무 수정
- 업무 삭제
- 업무 조회
