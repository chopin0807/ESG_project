import warnings
import pandas as pd
import MeCab
import re
import os

warnings.filterwarnings(action = 'ignore')
# 대상 기사데이터 파일 목록
path = "./기사데이터"
file_list = os.listdir(path)
data = pd.DataFrame({"기사날짜":[],"기사제목":[],"네이버 뉴스 url":[],"기사내용":[]})

for i in file_list:
    df = pd.read_csv("./기사데이터/" + i)
    data = pd.concat([data, df], ignore_index = True)

# 네이버 기사가 없거나, 스포츠 연예 기사 등 구조가 다른 기사 삭제
data.drop(data[(data['기사내용'] == '<네이버 기사 없음>') | (data['기사내용'] == '<구조 다름>')].index, inplace = True)
data = data.reset_index()
data.drop(columns = ["index", "네이버 뉴스 url"], inplace = True)
print(data)