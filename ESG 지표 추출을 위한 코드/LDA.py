import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# 토큰화된 데이터 불러오기
with open('C:/Users/rhksa/Documents/output-E.txt', 'r', encoding='utf-8') as file:
    # 각 라인을 별도의 문서로 취급하고, 각 라인을 공백 기준으로 토큰화
    documents = [line.strip().split() for line in file]

# 단어 사전 생성
dictionary = corpora.Dictionary(documents)

# 문서-단어 행렬 생성
corpus = [dictionary.doc2bow(text) for text in documents]

# LDA 모델 훈련
lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)

# 결과 출력
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))