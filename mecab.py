import warnings
import pandas as pd
import MeCab
import re
import os
from collections import Counter

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
data['기사내용'] = data['기사내용'].str.replace('\n',' ').replace('\t',' ').replace('\r', ' ') # 뉴스기사의 특수기호 제거

# Mecab 인스턴스 생성
m = MeCab.Tagger()
# '기사내용' 열에 대한 사전작업 결과를 '사전작업' 열에 저장
data['Content'] = data['기사내용'].apply(lambda x: re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', str(x)))

def extract_words(text):
    # 텍스트를 Mecab을 사용하여 토큰화
    tokens = m.parse(text).split('\n')
    # 선택된 단어를 저장할 리스트
    selected_words = []
    for token in tokens:
        if len(token) >= 2:
            # 각 토큰을 탭(\t)으로 분리하여 형태소와 품사 정보를 획득
            parts = token.split('\t')
            if len(parts) == 2:
                word, pos = parts
                pos = pos.split(',')[0]  # 품사 정보에서 첫 번째 부분만 사용
                # 선택 조건 (명사, 동사, 형용사)을 확인하고 선택된 단어 리스트에 추가
                if len(word) >= 2 and pos in ['NNG', 'VV', 'VA']:
                    selected_words.append(word)
    # 선택된 단어를 공백으로 구분된 문자열로 반환
    return ' '.join(selected_words)

#'기사내용' 열에 대해 처리
for i, row in data.iterrows():
    data.at[i, 'Content'] = extract_words(str(row['기사내용']))

result = data[['기사날짜','기사제목','Content']]
words_list = result['Content'].str.split()
all_words = [word for words in words_list for word in words]
word_counts = Counter(all_words)
most_common_words = word_counts.most_common(50)# 확인하고 싶은 갯수 넣기

print("가장 많이 나온 상위 50개 단어:")
for word, count in most_common_words:
    print(f"{word}: {count}")

stop_word = ['기자','지난해','올해'] #불용어 처리 과정

def preprocess(text):
  text = text.split()
  text = [i for i in text if i not in stop_word]
  return text

def make_tokens(df):
  df['tokens'] = ' '
  for i, row in df.iterrows():
    if i%100==0:
      print(i,'/',len(df))
    token = preprocess(df['Content'][i])
    df['tokens'][i] = ' '.join(token)
  return df

token_result = make_tokens(result)

#날짜만 추출
token_result['기사날짜'] = token_result['기사날짜'].str.split(' ').str[0]

#결측값 제거
token_result = token_result.dropna(subset=['tokens'])
print(token_result)

#csv파일 만들기
token_result.to_csv('우리은행_news.csv', index=False)