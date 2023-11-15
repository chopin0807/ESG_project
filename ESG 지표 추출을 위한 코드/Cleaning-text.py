import MeCab
import re

# Mecab 인스턴스 생성
m = MeCab.Tagger()

# 불용어 리스트
stop_words = ['기자', '지난해', '올해']

def extract_words(text):
    # 텍스트를 Mecab을 사용하여 토큰화합니다.
    tokens = m.parse(text).split('\n')

    # 선택된 단어를 저장할 리스트
    selected_words = []

    for token in tokens:
        if len(token) >= 2:
            # 각 토큰을 탭(\t)으로 분리하여 형태소와 품사 정보를 얻습니다.
            parts = token.split('\t')
            if len(parts) == 2:
                word, pos = parts
                pos = pos.split(',')[0]  # 품사 정보에서 첫 번째 부분만 사용

                # 선택 조건 (명사, 동사, 형용사)을 확인하고 선택된 단어 리스트에 추가
                if len(word) >= 2 and pos in ['NNG', 'VV', 'VA']:
                    selected_words.append(word)

    # 선택된 단어를 공백으로 구분된 문자열로 반환합니다.
    return ' '.join(selected_words)

def preprocess(text):
    text = text.split()
    text = [i for i in text if i not in stop_words]
    return ' '.join(text)

# 파일 읽기
with open('C:/Users/rhksa/Documents/extracted_text-G.txt', 'r', encoding='utf8') as file:
    sample_text = file.read()

# 특수 문자 제거
cleaned_text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]', ' ', sample_text)

# 단어 추출
extracted_words = extract_words(cleaned_text)

# 불용어 제거
final_text = preprocess(extracted_words)

# 결과를 txt 파일로 저장
with open('output-G.txt', 'w', encoding='utf8') as file:
    file.write(final_text)

print("토큰화된 텍스트가 'output.txt' 파일로 저장되었습니다.")