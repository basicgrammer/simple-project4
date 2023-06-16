### 버전 정보

- Python : 3.9
- Django : 4.2.1
- Postgres : 13

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
