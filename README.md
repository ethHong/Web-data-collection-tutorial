# 웹 데이터 수집 튜토리얼(WIP)
### 추후 MD 및 PDF로 된 가이드가 첨부될 예정입니다 (@Documents)
Documents 폴더에 매주차 PPT를 업로드중입니다
* 본 튜토리얼은, 프로그래밍 및 웹 데이터 수집 경험이 많지 않은 분들을 대상으로 합니다.
* 이론적인 내용보다 실제 데이터 수집 및 활용이 필요한 프로젝트 상황에서 실질적인 활용할 수 있는 내용 위주로 다루고자 합니다.  
* 사용 언어 및 라이브러리: python, selenium, bs4

## 환경설정

폴더를 내려받은 후, 디렉토리에 접근 후 아래와 같이 가상환경을 설정해주세요
~~~
#가상환경 생성 및 진입
>> cd Web-data-collection-tutorial
>> pip install pipenv
>> pipenv --three
>> pipenv shell

#Pipfile.lock에서 패키지 설치
>> pipenv install
~~~
virtualenv 사용을 위해 추후 requirements.txt 도 업데이트할 예정입니다. 

## 업데이트 내역
21.08.16
* Part 2 - Documents 에 PPT 업로드
* Selenium_practice : Part 2 의 Selenium tutorial 위한 파일 업로드
* coursera_crawler :  참고를 위한 coursera 크롤링 코드 업로드 - (https://github.com/ethHong/Selenium_Coursera_crawler 와 같은 코드)

21.08.03
* Part 1 - Documents 에 PPT 업로드
* BS4_practice: Part 1 에서 bs4로 html 다루기 ipynb 업로드
* appstore_collection: 크롤링 예시로 앱스토어 평점 수집 코드 업로드 (https://github.com/ethHong/Appstore_rating_collection 와 같은 코드)
