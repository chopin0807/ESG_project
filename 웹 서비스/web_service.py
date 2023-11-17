import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# 터미널에서 실행(이 파이썬 파일에 속해 있는 디렉터리로 이동해서) -> streamlit run web_service.py

with st.sidebar: # 참고 url: https://luvris2.tistory.com/121
    choose = option_menu("ESG 평가 서비스", ["홈", "개요", "관련 논문"],
                         icons=['house', 'pen', 'book'],
                         menu_icon="bi bi-menu-up", default_index=0,
                         styles={
                         # default_index = 처음에 보여줄 페이지 인덱스 번호
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    } # css 설정
    )