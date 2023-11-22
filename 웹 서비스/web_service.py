import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# 터미널에서 실행(이 파이썬 파일에 속해 있는 디렉터리로 이동해서) -> streamlit run web_service.py

with st.sidebar: # 참고 url: https://luvris2.tistory.com/121
    choose = option_menu("ESG 평가 서비스", ["홈", "개요", "ESG 서비스", "자료실"],
                         icons=['house', 'pen', 'boxes','database'],
                         menu_icon="bi bi-menu-up", default_index=0,
                         styles={
                         # default_index = 처음에 보여줄 페이지 인덱스 번호
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    } # css 설정
    )

# 각 메뉴를 선택시 표시되는 내용
if choose == "홈":
    st.header("Find Insight in the ESG Keyword")
    st.image("./ESG그림.png")
    st.image("./ESG개요.png")

elif choose == "개요":
    tab1, tab2 = st.tabs(['서비스 목적', '프로세스'])

    with tab1:
        # '서비스 목적'을 누르면 표시되는 내용
        st.write('각 기업별로 ESG지표를 산출하여 평가함으로써...')
    with tab2:
        # '프로세스'를 누르면 표시되는 내용
        st.write('ESG관련 논문 및 ISO자료로 부터 ESG요소별 키워드 추출 => 기사데이터 추출 => 기사데이터에서 ESG 요소 판단 => 기사데이터에서 긍/부정 판단....')

elif choose == "ESG 서비스":
    st.write("각 기업별로 ESG평가 지표 측정 후 ESG 각 요소에 대한 점수와 등급산출 결과를 확인할 수 있습니다.")

elif choose == "자료실":
    st.header("ESG 관련 자료 및 기업별 관련 기사 내용 및 키워드")
    tab1, tab2, tab3 = st.tabs(['ESG 논문/ISO 표준', '관련 기사', '기사 키워드'])

    with tab1:
        st.write('논문 자료 및 ISO표준에 대한 자료를 포함하는 것에 대해 고려합니다.')
    with tab2:
        st.write('관련 기사 제목을 링크로 담고, 링크를 클릭하면 해당 기사로 들어가게합니다.')
    with tab3:
        st.write('키워드를 뽑아 주요 기업별 이슈를 추출해 내고자 합니다.')