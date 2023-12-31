import pandas as pd
import os

# 디렉토리 경로 설정
directory_path = "C:/Users/rhksa/OneDrive/바탕 화면/새 폴더/"
output_directory = directory_path + "엑셀파일/"

# '엑셀파일' 출력 디렉토리가 없으면 생성합니다.
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 디렉토리 내의 모든 CSV 파일을 찾습니다.
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# 분석할 키워드를 설정합니다.
keywords = [ '환경', '탄소배출', '기후변화', '재생에너지', '에너지효율', '생물다양성', '지속가능농업', '친환경', '에코프렌들리', '환경보호', '저탄소경제', '에너지전환', '재생가능에너지', '녹색에너지', '환경친화', '기후변화완화', '기후적응', '녹색인프라', '탄소중립', '녹색건물', '환경준수', '환경오염', '친환경제품', '녹색기술', '에너지효율성', '환경가치', '환경보전', '기후정책', '환경보건', '녹색발전', '환경지속가능성', '녹색성장', '탄소감축', '환경경영', '환경개선', '지속가능소비재', '환경법규', '기후변화영향', '녹색정책', '환경인식', '에코농업', '친환경농업', '기후변화행동', '환경산업', '환경적정기술', '환경혁신', '기후변화적응', '지속가능성지표', '환경친화적', '에코라이프', '녹색에너지정책', '환경오염방지', '환경지속가능기업', '환경보호정책', '녹색기술개발', '환경감사', '녹색소비', '환경효율성', '환경보호활동', '녹색사업', '환경지속가능발전', '환경친화적사업', '지속가능성평가기준', '환경보호투자', '녹색건축', '환경친화적제품', '녹색성장전략', '에너지환경정책', '환경보호캠페인', '환경지속가능성평가', '기후변화대응', '지속가능개발', '에너지보존', '자원재활용', '녹색금융', '지구온난화', '에코디자인', '생태계보호', '지속가능에너지', '지속가능패션', '생태학', '환경교육', '지속가능교통', '에너지절약', '지속가능도시', '수자원관리', '환경규제', '기후리스크', '에코시스템', '지속가능투어', '폐기물처리', '에너지자립', '지속가능생산', '유해물질관리', '기후금융', '환경친화적농업', '바이오다이버시티', '기후변화교육', '에너지정책', '환경보호기술', '환경감시', '대기오염', '지속가능성분석', '녹색교통', '지속가능성보고', '환경성과', '녹색에너지전환', '에코투어리즘','거버넌스', '기업지배구조', '윤리경영', '투명성', '리스크관리', '경영책임', '규제준수', '감사기능', '정책결정', '경영효율성', '이사회', '주주권리', '경영투명성', '준법경영', '경영진책임', '회사운영', '경영윤리', '지배구조', '감독체계', '경영감시', '정보공개', '기업윤리', '경영투명', '기업규범', '기업문화', '책임경영', '감사위원회', '주주이익', '윤리기준', '기업통제', '경영진평가', '비즈니스윤리', '내부통제', '기업윤리정책', '리스크평가', '내부감사', '기업규정', '컴플라이언스', '지배구조개선', '회사정책', '기업지배', '주주총회', '경영관리', '회사법', '윤리강령', '정보투명성', '리스크관리정책', '감사제도', '지배구조평가', '기업감사', '경영컨설팅', '경영감독', '기업가치', '주주관리', '회계투명성', '내부규제', '감사위원', '경영조직', '주주대표소송', '기업감시', '기업운영', '경영자문', '리스크컨트롤', '주주권익', '기업투명성', '윤리경영정책', '기업비전', '이사회운영', '지배구조정책', '경영진과의소통', '감사정책', '기업윤리코드', '경영평가', '기업리스크', '감사인', '기업정보공개', '윤리적경영', '이사회구성', '주주가치', '기업감독위원회', '기업투명성증진', '리스크포트폴리오', '지배구조규정', '경영자윤리', '리스크프로파일', '내부통제시스템', '감사프로세스', '회사경영', '회계감사', '기업윤리위원회', '경영전략', '윤리적비즈니스', '기업거버넌스', '주주운영', '윤리감사', '기업규율', '감사활동', '정보관리', '주주관계관리', '경영체계', '경영진검토', '기업경영규칙', '리스크관리시스템', '경영조언', '이사회규정', '회계투명', '주주소통', '경영감독체계', '경영자문위원회','거버넌스', '기업지배구조', '윤리경영', '투명성', '리스크관리', '경영책임', '규제준수', '감사기능', '정책결정', '경영효율성', '이사회', '주주권리', '경영투명성', '준법경영', '경영진책임', '회사운영', '경영윤리', '지배구조', '감독체계', '경영감시', '정보공개', '기업윤리', '경영투명', '기업규범', '기업문화', '책임경영', '감사위원회', '주주이익', '윤리기준', '기업통제', '경영진평가', '비즈니스윤리', '내부통제', '기업윤리정책', '리스크평가', '내부감사', '기업규정', '컴플라이언스', '지배구조개선', '회사정책', '기업지배', '주주총회', '경영관리', '회사법', '윤리강령', '정보투명성', '리스크관리정책', '감사제도', '지배구조평가', '기업감사', '경영컨설팅', '경영감독', '기업가치', '주주관리', '회계투명성', '내부규제', '감사위원', '경영조직', '주주대표소송', '기업감시', '기업운영', '경영자문', '리스크컨트롤', '주주권익', '기업투명성', '윤리경영정책', '기업비전', '이사회운영', '지배구조정책', '경영진과의소통', '감사정책', '기업윤리코드', '경영평가', '기업리스크', '감사인', '기업정보공개', '윤리적경영', '이사회구성', '주주가치', '기업감독위원회', '기업투명성증진', '리스크포트폴리오', '지배구조규정', '경영자윤리', '리스크프로파일', '내부통제시스템', '감사프로세스', '회사경영', '회계감사', '기업윤리위원회', '경영전략', '윤리적비즈니스', '기업거버넌스', '주주운영', '윤리감사', '기업규율', '감사활동', '정보관리', '주주관계관리', '경영체계', '경영진검토', '기업경영규칙', '리스크관리시스템', '경영조언', '이사회규정', '회계투명', '주주소통', '경영감독체계', '경영자문위원회']

# 각 CSV 파일에 대해 처리를 수행합니다.
for file in csv_files:
    df = pd.read_csv(directory_path + file)

    # 키워드를 포함하고, 해당 키워드에 5개 이상의 단어가 있는 행을 필터링합니다.
    # 'column_name'을 검사할 열의 이름으로 바꿉니다.
    filtered_df = df[df['content'].apply(lambda x: sum(keyword in str(x) for keyword in keywords) >= 3)]

    # 필터링된 결과에서 1000개의 행을 샘플링합니다.
    # 샘플링할 행의 수가 DataFrame의 행 수보다 많을 경우 모든 행을 반환합니다.
    result = filtered_df.sample(n=min(100, len(filtered_df)), random_state=1)
    result = result.reset_index(drop=True)

    # 엑셀 파일로 저장합니다.
    result.to_excel(output_directory + f"{file.split('.')[0]}.xlsx")
