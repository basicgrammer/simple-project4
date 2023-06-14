

### 버전 정보
- Python : 3.8
- Django : 4.2.1
- Postgres : 13 


### 수정 정보 

- psycopg2가 desperated가 될 수 있다는 문장이 언급되므로  psycopg[binary]에서 3버전을 설치한다.
- psycopg2 vs psycopg3의 성능 차이는 아래 링크를 참고하자 (3 초기 버전의 벤치마크라서 성능 최적화가 덜 되었다는 말이 있으나 3.1 버전에서 성능 최적화가 되었을 것이라고 본다.)
- URL : https://www.spherex.dev/psycopg-2-vs-psycopg3/