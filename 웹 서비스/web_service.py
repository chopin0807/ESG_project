import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import pandas as pd

# 터미널에서 실행(이 파이썬 파일에 속해 있는 디렉터리로 이동해서) -> streamlit run web_service.py

# 사용할 ESG 데이터
df = pd.read_csv("./ESG샘플.csv")
# 필요한 행 추출
df = df[['날짜', '기업', '제목', '구분(ESG)', '점수']]
# 전체 점수에 대한 평균
avg_all = round(df["점수"].mean(), 1)
# ESG 각 요소별 평균점수 구하기
# E에 대한 점수
df_E = df[df["구분(ESG)"] == "E"]['점수']
# E에 대한 평균
avg_E = round(df_E.mean(), 1)
# S에 대한 점수
df_S = df[df['구분(ESG)'] == "S"]['점수']
# S에 대한 평균
avg_S = round(df_S.mean(), 1)
# G에 대한 점수
df_G = df[df['구분(ESG)'] == "G"]['점수']
# G에 대한 평균
avg_G = round(df_G.mean(), 1)

# 게이지 차트 그리기
import plotly.graph_objects as go

def create_gauge_chart(value, title, range_min, range_max):
    fig = go.Figure()

    # Add gauge chart
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [range_min, range_max]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [range_min, range_max], 'color': "lightgray"}
            ],
        }
    ))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_size=16)
    fig.write_image("{}.png".format(title))

# 모든 ESG요소별 게이지 차트
create_gauge_chart(value=avg_all, title="전체", range_min=0, range_max=100)
create_gauge_chart(value=avg_E, title="E(환경)분석", range_min=0, range_max=100)
create_gauge_chart(value=avg_S, title="S(사회)분석", range_min=0, range_max=100)
create_gauge_chart(value=avg_G, title="G(지배)분석", range_min=0, range_max=100)
with st.sidebar: # 참고 url: https://luvris2.tistory.com/121
    choose = option_menu("ESG 평가 서비스", ["ESG 소개", "ESG 서비스", "참고자료"],
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

if choose == "ESG 소개":
    tab1, tab2, tab3 = st.tabs(['ESG 인사이트', '서비스 목적', '프로세스'])

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
    col1, col2, col3, col4 = st.columns([10, 5, 5, 5])
    with col1:
        st.image("전체.png")
    with col2:
        st.image("E(환경)분석.png")
    with col3:
        st.image("S(사회)분석.png")
    with col4:
        st.image("G(지배)분석.png")

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