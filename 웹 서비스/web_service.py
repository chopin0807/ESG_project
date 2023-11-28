import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os

# 터미널에서 실행(이 파이썬 파일에 속해 있는 디렉터리로 이동해서) -> streamlit run web_service.py

with st.sidebar: # 참고 url: https://luvris2.tistory.com/121
    choose = option_menu("ESG 평가 서비스", ["개요", "ESG 서비스", "참고자료"],
                         icons=['pen', 'boxes','database'],
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

if choose == "개요":
    tab1, tab2, tab3 = st.tabs(['인사이트', '서비스 목적', '프로세스'])

    with tab1:
        st.header("Find Insight in the ESG Keyword")
        st.image("./ESG그림.png")
        st.image("./ESG개요.png")
    with tab2:
        # '서비스 목적'을 누르면 표시되는 내용
        st.write('각 기업별로 ESG지표를 산출하여 평가함으로써...')
    with tab3:
        # '프로세스'를 누르면 표시되는 내용
        st.write('ESG관련 논문 및 ISO자료로 부터 ESG요소별 키워드 추출 => 기사데이터 추출 => 기사데이터에서 ESG 요소 판단 => 기사데이터에서 긍/부정 판단....')

elif choose == "ESG 서비스":
    st.write("각 기업별로 ESG평가 지표 측정 후 ESG 각 요소에 대한 점수와 등급산출 결과를 확인할 수 있습니다.")

elif choose == "참고자료":
    st.header("ESG 관련 논문 자료 및 ISO 표준 관련 참고자료")
    tab1, tab2 = st.tabs(['ESG 논문', 'ISO 표준'])

    with tab1:
        ESG_report_list = os.listdir("./ESG 논문")
        select_ESG = st.selectbox("다운받을 ESG 관련 pdf 파일을 선택하세요.", ESG_report_list)
        with open("./ESG 논문/{}".format(select_ESG), "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="pdf 다운로드",
                    data=PDFbyte,
                    file_name=select_ESG,
                    mime='application/octet-stream')
    with tab2:
        ISO_report_list = os.listdir("./ISO 자료")
        select_ISO = st.selectbox("다운받을 ISO 관련 파일을 선택하세요.", ISO_report_list)
        with open('./ISO 자료/{}'.format(select_ISO), 'rb') as f:
            st.download_button('Download Docx', f, file_name='./ISO 자료/{}'.format(select_ISO))