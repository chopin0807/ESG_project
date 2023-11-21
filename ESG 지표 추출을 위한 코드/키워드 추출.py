import MeCab
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Mecab 형태소 분석기 초기화 (한글 처리를 위한 설정 추가 필요)
mecab = MeCab.Tagger()

# 불용어 리스트
stopwords = {'의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다','한다','여야','대한','위한','에서','조직','수립','사항','위하','고려','심사','위해','통해','에게','으로써','어야','아니','미치','거나','또한','인한','따른','따라서','경우','또는','나아가','혹은','특히','으며','구체','아울러','미칠','climate','관한','해당','세부','더불','최종','시키','이나','인지','scope','고자','이러','해야','통한','까지','carbon','이때','보다','climate','on','비롯','는지','므로','scope','으므로','면밀히','함께','대해','된다','갖추','통하','carbon','대해서','따라','도록','면서'}

# 한글과 두 글자 이상인 단어만 추출하는 함수
def is_valid_korean_word(word):
    return len(word) > 1 and re.match(r'^[가-힣]+$', word) is not None

# 토큰화 및 불용어 제거, 한글 필터링 함수
def tokenize(text):
    nodes = mecab.parseToNode(text)
    words = []
    while nodes:
        if nodes.surface not in stopwords and is_valid_korean_word(nodes.surface):
            words.append(nodes.surface)
        nodes = nodes.next
    return words

# 텍스트 파일 읽기
with open("C:/Users/rhksa/Documents/extracted_text-E.txt", "r", encoding="utf-8") as file:
    documents = file.readlines()

# 토큰화 및 불용어 처리, 한글 필터링
processed_docs = [" ".join(tokenize(doc)) for doc in documents]

# TF-IDF 벡터라이저 초기화
vectorizer = TfidfVectorizer(max_features=300)

# 문서에 대한 TF-IDF 매트릭스 계산
tfidf_matrix = vectorizer.fit_transform(processed_docs)

# 각 단어의 TF-IDF 점수 추출 및 상위 300개 키워드 출력
feature_names = vectorizer.get_feature_names_out()
scores = zip(feature_names, np.asarray(tfidf_matrix.sum(axis=0)).ravel())
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:300]
print("상위 300개 키워드:")
for feature, score in sorted_scores:
    print(f"{feature}: {score}")

with open("E-keywords.txt", "w", encoding="utf-8") as file:
    for feature, score in sorted_scores:
        file.write(f"{feature}: {score}\n")

print("키워드가 'keywords.txt' 파일에 저장되었습니다.")
