import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random

def NaverArticle(search, start_date, end_date):
    # csv 파일 쓰기
    f = open("news.csv", "w", newline="", encoding="utf-8")
    wr = csv.writer(f)
    index = ["기사날짜", "기사제목", "네이버 뉴스 url", "기사내용"]
    wr.writerow(index)

    page = 1 # 기사 페이지
    while True:
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds={}&de={}&cluster_rank=46&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20211001to20230930,a:all&start=1'.format(search, start_date, end_date)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        csv_value = []
        title = soup.select('div.news_contents > a.news_tit')
        if len(title) == 0: # 이 경우 기사가 검색되지 않고, 검색결과가 없다는 검색결과가 표시됨
            break # 크롤링이 막힌경우 아무것도 표시되지 않을 것임
        else:
            title_list = [] # 기자제목 리스트
            for i in title:
                title_list.append(i['title'])
            naver_article = soup.select('div.info_group')
            article_list = []
            for i in naver_article:
                article_list.append(i)
            # 네이버 기사 링크 리스트로 정리
            naver_article_url = []
            for i in article_list:
                try:
                    naver_article_url.append(i.select('a')[1]['href'])
                except:
                    naver_article_url.append('url없음')
            # 기사 날짜 설정
            date = soup.select('div.info_group > span')
            date_list = []
            for i in date:
                date_list.append(i.text)
            # 날짜형식(xxxx.xx.xx.)이 나오게 수정
            article_date = []
            for i in date_list:
                p = re.compile('[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9].')
                t = re.compile('[0-9가-힣]* 전')
                if p.match(i) != None or t.match(i) != None:
                    article_date.append(i)
            # 기사 내용 크롤링
            content_list = [] # 기사 내용이 담길 리스트
            for i in naver_article_url:
                if i == 'url없음':
                    content_list.append('<네이버 기사 없음>')
                else:
                    time.sleep(random.uniform(1,5)) # 접속차단을 최대한 방지하기 위해 1초~5초 사이에 랜덤으로 지연
                    content_url = i # 해당 기사 링크로 진입
                    content_res = requests.get(content_url, headers=headers)
                    content_soup = BeautifulSoup(content_res.text, 'html.parser')
                    content = content_soup.select_one('article.go_trans') # 대부분의 기사 내용 구조가 이러함
                if len(content_soup.select('article.go_trans')) != 0: # 해당 기사 내용이 있다면
                    content_list.append(content.text.strip().replace('\n',''))
                else: # 위의 구조에도 하나도 포함되지 않다면! => 해당 기사에 대한 내용 구조를 찾아야 할 수 있음!
                    content_list.append('<구조 다름>')
            for i in range(len(title_list)):
                temp = []
                temp.append(article_date[i])
                temp.append(title_list[i])
                temp.append(naver_article_url[i])
                temp.append(content_list[i])
                csv_value.append(temp)
            print('기사 페이지: ', page)
            print('=================================================================')
            for i in csv_value:
                wr.writerow(i)
        page += 1
    f.close()

# 검색 키워드, 시작날짜, 마지막 날짜 입력받기
search = str(input('검색할 키워드 입력: '))
start_date = str(input('기사 시작날짜 입력 (형식예시 => 2021.10.01): '))
end_date = str(input('기사 마지막날짜 입력 (형식예시 => 2023.09.30): '))
NaverArticle(search, start_date, end_date)