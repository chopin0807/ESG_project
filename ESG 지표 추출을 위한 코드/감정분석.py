import pandas as pd
# df = pd.read_csv('/content/drive/MyDrive/esg 프로젝트/combined_file.csv')
df = pd.read_csv('./기사데이터/우리은행/combined_file.csv') # 프로젝트 폴더(ESG_PROJECT) 내의 최상위 폴더에서 VSCode로 실행해서 파이썬 파일을 실행하면 됩니다.
df2 = df[~df['기사내용'].isin(['<구조 다름>', '<네이버 기사 없음>'])]
df2 = df2[['기사제목','네이버 뉴스 url','기사내용']]

from tqdm import tqdm, tqdm_pandas

tqdm.pandas()
import json

# JSON 파일로부터 감정 사전 로드
with open("./SentiWord_info.json", "r", encoding="utf-8") as file: # 프로젝트 폴더(ESG_PROJECT) 내의 최상위 폴더에서 VSCode로 실행해서 파이썬 파일을 실행하면 됩니다.
    sentiment_data = json.load(file)

# JSON 데이터를 토큰-감정 점수 사전으로 변환
sentiment_dict = {item['word']: int(item['polarity']) for item in sentiment_data}

import MeCab

# MeCab 초기화
mecab = MeCab.Tagger()

# 한글 토큰 추출 함수
def filter_korean(parsed_text):
    lines = parsed_text.split('\n')
    tokens = [line.split('\t')[0] for line in lines if line.strip() != 'EOS' and line.strip() != '']
    return [token for token in tokens if len(token) >= 2 and re.match('[가-힣]+', token)]

import os

# 감정 분석 함수 수정
def analyze_korean_sentiment(text):
    # 결측치 제거
    if pd.isnull(text):
        return "중립", []

    # 텍스트를 파일로 저장
    with open("temp.txt", "w", encoding="utf-8") as temp_file:
        temp_file.write(text)

    # MeCab을 사용하여 파일을 분석
    parsed_text = mecab.parse(text)

    # 파일 삭제
    os.remove("temp.txt")

    # 한글 토큰 추출
    korean_tokens = filter_korean(parsed_text)

    scores = [sentiment_dict.get(token, 0) for token in korean_tokens]
    overall_score = sum(scores) / len(scores) if scores else 0

    sentiment = "중립"
    if overall_score > 0:
        sentiment = "긍정"
    elif overall_score < 0:
        sentiment = "부정"

    return sentiment, korean_tokens

import re
# 감정 분석 결과와 토큰을 데이터프레임에 저장
df2[['sentiment', 'tokens']] = df2['기사내용'].progress_apply(lambda x: pd.Series(analyze_korean_sentiment(x)))

keywords = {
    "E": ['친환경', '물질', '기후', '발생', '요인', '화학', '배출', '생물', '온실가스', '오염', '보전', '생태', '탄소', '유해', '용수', '순환', '산림', '사용량', '부자재', '해양', '설비', '자연', '수자원', '폐수', '녹색', '사슬', '재생', '정량', '지역', '폐기', '배출권', '저탄소', '건강', '플라스틱', '인벤토리', '보호', '피해', '원료', '저감', '신재'],
    "S": [ '위험', '규준', '모범', '공개', '참고', '문화', '의사', '요인', '체계', '개인', '안전', '공급', '발생', '제도', '효과', '피해', '가치', '소통', '파악', '구축', '리더십', '보건', '사항', '침해', '보장', '점검', '실사', '결과', '보상', '역할', '결함', '공유', '성장', '방침', '자유', '경제', '생활', '상호', '고용', '관계', '예방', '정기', '달성', '창출', '주체', '범위', '동반성', '부당', '균형', '형성', '규제', '보안', '강령', '연계', '감독', '저해', '권익', '부합', '표명', '자발', '개정', '안전성', '고충', '임금', '업무', '자율', '긍정', '증진', '이익', '정의', '특성', '투입', '근거', '유도', '적절', '해소', '조성', '인지', '뒷받침', '노사', '구조', '산업', '국내외', '근무', '수단', '남용', '관여', '건강', '차별', '기반', '수집', '전달', '협의', '유형', '인력', '대내외', '상이', '정량', '모델', '중대', '계층', '완화', '정당', '관점', '선택', '금지', '선제', '방지', '전문', '잠재', '중심', '질서', '조건', '합리', '비용', '이용', '생산', '조사', '확립', '가격', '메커니즘', '대책', '접근성', '취약', '성별', '조치', '사고', '우려', '실질', '불공정', '시행', '비율', '재해', '기업지배구조', '경영진', '변화', '채널', '자사', '절차', '부정', '행위', '외부', '가이드라인', '임직원', '부서', '구성', '사례', '프로그램', '목적', '처리', '구체', '기본', '설정', '측면', '부여'],
    "G": [ '감사', '이사', '주주', '위원회', '지배', '모범', '규준', '사외', '기업지배구조', '총회', '선임', '규정', '중대', '내용', '관계', '직무', '재무', '후보', '기능', '경영자', '결의', '보수', '독립성', '전문', '의사', '권고', '주식', '금지', '행사', '회계', '위원', '소통', '이익', '승계', '이사회', '공개', '법령', '의결권', '보상', '임원', '보호', '사유', '환경', '지배주', '추천', '다양', '부서', '노력', '자본', '정기', '참석', '개최', '책임자', '포함', '임직원', '윤리', '대표', '설치', '의견', '투명', '제도', '행위', '공정', '권리', '변화', '정관', '마련', '정책', '회의', '유지', '이용', '영업', '반대', '보고', '자격', '보장', '타당', '제정', '영향', '매수', '제한', '안건', '일반', '판단', '개정', '과도', '사전', '보고서', '적정', '직접', '정확', '투자', '비밀', '교육', '의안', '목적', '승인', '자신', '과정', '해임', '자료', '집행', '자기', '독립', '이해관계', '상충', '합병', '분리', '내역', '담당', '방법', '침해', '발생', '합리', '자산', '설명', '활용', '의미', '관행', '근거', '회의록', '제시', '용이', '방향', '작성', '전문가', '위임', '집단', '의장', '예측', '요청', '활성', '자문', '훼손', '인수', '지급', '상정', '존중', '지정', '일치', '자기거래', '양수', '상장', '지식', '시장', '법인', '투표', '부여', '논의', '용역', '소유', '추구', '주의', '특수', '이상', '지양', '영향력', '계열사', '법률', '조성', '인과', '사내', '연간', '손해', '부당', '전원', '개별', '토의', '명문화', '상세', '보유', '공유', '신속', '수단', '가진', '접근', '전자', '적시', '기재', '장소', '방안', '우려', '보험', '투입', '실효', '원활', '외국인', '전체', '개인', '명확', '일정', '성장', '가입', '채권자', '항목']
}

# ESG 카테고리를 분류하여 'ESG' 열에 가장 근접한 카테고리를 넣는 함수 정의
def classify_esg(text, keywords):
    category_scores = {category: sum(keyword in text for keyword in keywords[category]) for category in keywords}
    # 최대 점수를 가진 카테고리를 찾음 (점수가 같은 경우 여러 카테고리를 반환할 수 있음)
    max_score = max(category_scores.values())
    closest_categories = [category for category, score in category_scores.items() if score == max_score]

    # 가장 근접한 카테고리를 반환 (여러 개일 경우 쉼표로 구분)
    return ', '.join(closest_categories) if closest_categories else 'None'

# ESG 카테고리 분류 적용
df2['ESG'] = df2['tokens'].progress_apply(lambda x: classify_esg(x, keywords))

df2 = df2[['기사제목','네이버 뉴스 url','tokens','sentiment','ESG']]
df2 = df2[~df2['sentiment'].isin(['중립'])]

# df2.to_csv('./기사 감정분석.csv', index = False)
df2.to_excel('./기사 감정분석.xlsx', index = False)
print(df2)
