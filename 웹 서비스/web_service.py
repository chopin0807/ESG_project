import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import plotly.express as px

# 터미널에서 실행(이 파이썬 파일에 속해 있는 디렉터리로 이동해서) -> streamlit run web_service.py

# 사용할 ESG 데이터
file_list = os.listdir("./기업별데이터")
data_list = [file for file in file_list if file.endswith(".csv")]
df = pd.DataFrame({'날짜' : [], '기업' : [], '기사제목': [], 'ESG_Sentence' : [], 'ESG' : [], '점수' : []})
for i in data_list:
    data = pd.read_csv("./기업별데이터/{}".format(i))
    # 필요한 행 추출
    data = data[['날짜', '기업', '기사제목', 'ESG_Sentence', 'ESG', '점수']]
    df = pd.concat([df, data], ignore_index=True)
# 필요한 행 추출
df = df[['날짜', '기업', '기사제목', 'ESG_Sentence', 'ESG', '점수']]
# ESG 값이 'X'인 것 제거
df.drop(df[df['ESG'] == 'X'].index, inplace=True)
df = df.reset_index()
df.drop('index', axis = 1, inplace=True)

def preprocess(df_company, tab_num):
    avg_all = round(df_company["점수"].mean(), 1)
    df_E = df_company[df_company["ESG"] == "E"]['점수']
    avg_E = round(df_E.mean(), 1)
    df_S = df_company[df_company['ESG'] == "S"]['점수']
    avg_S = round(df_S.mean(), 1)
    df_G = df_company[df_company['ESG'] == "G"]['점수']
    avg_G = round(df_G.mean(), 1)
    E_news = df_company[df_company['ESG'] == 'E'].sort_values(by = '점수', ascending = False)
    S_news = df_company[df_company['ESG'] == 'S'].sort_values(by = '점수', ascending = False)
    G_news = df_company[df_company['ESG'] == 'G'].sort_values(by = '점수', ascending = False)
    date_df = df_company[['날짜', '점수', 'ESG']]
    date_df['date'] = date_df['날짜'].apply(lambda x:x.split(" ")[0])
    date_df_ESG = date_df[['date', '점수']]
    date_df_E = date_df[date_df['ESG'] == 'E'][['date', '점수']] # E에 대한 시계열
    date_df_S = date_df[date_df['ESG'] == 'S'][['date', '점수']] # S에 대한 시계열
    date_df_G = date_df[date_df['ESG'] == 'G'][['date', '점수']] # G에 대한 시계열
    date_avg_ESG = date_df_ESG.groupby('date').mean()
    date_avg_ESG = date_avg_ESG.reset_index()
    date_avg_E = date_df_E.groupby('date').mean()
    date_avg_E = date_avg_E.reset_index()
    date_avg_S = date_df_S.groupby('date').mean()
    date_avg_S = date_avg_S.reset_index()
    date_avg_G = date_df_G.groupby('date').mean()
    date_avg_G = date_avg_G.reset_index()
    create_gauge_chart(value=avg_all, title="기업", range_min=-100, range_max=100)
    create_gauge_chart(value=avg_E, title="E(환경)분석", range_min=-100, range_max=100)
    create_gauge_chart(value=avg_S, title="S(사회)분석", range_min=-100, range_max=100)
    create_gauge_chart(value=avg_G, title="G(지배)분석", range_min=-100, range_max=100)

    if tab_num == 1:
        return [len(E_news), len(S_news), len(G_news)]
    elif tab_num == 2:
        return [E_news, S_news, G_news]
    else:
        return [date_avg_ESG, date_avg_E, date_avg_S, date_avg_G]


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
    tab1, tab2, tab3 = st.tabs(['ESG 인사이트', '서비스 목적', 'ESG 중요성 및 의의'])

    with tab1:
        st.header("Find Insight in the ESG Keyword")
        st.image("./ESG그림.png")
        st.image("./ESG개요.png")
    with tab2:
        # '서비스 목적'을 누르면 표시되는 내용
        st.image("./ESG프로세스.gif")
    with tab3:
        # 'ESG 중요성 및 의의'를 누르면 표시되는 내용
        st.image("./ESG의의.png")

elif choose == "ESG 서비스":
    company_select = ["전체"]
    company_select.extend(df["기업"].unique())
    company = st.selectbox("ESG분석할 기업을 선택해주세요.", company_select)
    tab1, tab2, tab3 = st.tabs(["ESG 전체 지표", "ESG각 요소별 평가지표 및 관련기사", "ESG지표별 시계열 차트"])
    with tab1:
        if company == "전체":
            df_company = df
        else: # 분석 기업을 '전체'를 선택하지 않고, 특정 기업을 선택한 경우
            df_company = df[df['기업'] == company]
        result = preprocess(df_company, 1)
        st.image("./기업.png")
        pie = px.pie(values = result, names = ["Environmental", "Social", "Governance"])
        st.write(pie)
        bar = px.bar(x = ["Environmental", "Social", "Governance"], y = result)
        st.write(bar)
    with tab2:
        if company == "전체":
            df_company = df
        else: # 분석 기업을 '전체'를 선택하지 않고, 특정 기업을 선택한 경우
            df_company = df[df['기업'] == company]
        result = preprocess(df_company, 2)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("E(환경)분석.png")
            st.header("긍정")
            st.dataframe(result[0].reset_index()[['기사제목', 'ESG_Sentence', '점수']])
            st.header("부정")
            st.dataframe(result[0].reset_index()[['기사제목', 'ESG_Sentence', '점수']].sort_values(by = '점수', ascending = True))
        with col2:
            st.image("S(사회)분석.png")
            st.header("긍정")
            st.dataframe(result[1].reset_index()[['기사제목', 'ESG_Sentence', '점수']])
            st.header("부정")
            st.dataframe(result[1].reset_index()[['기사제목', 'ESG_Sentence', '점수']].sort_values(by = '점수', ascending = True))
        with col3:
            st.image("G(지배)분석.png")
            st.header("긍정")
            st.dataframe(result[2].reset_index()[['기사제목', 'ESG_Sentence', '점수']])
            st.header("부정")
            st.dataframe(result[2].reset_index()[['기사제목', 'ESG_Sentence', '점수']].sort_values(by = '점수', ascending = True))
    with tab3:
        if company == "전체":
            df_company = df
        else: # 분석 기업을 '전체'를 선택하지 않고, 특정 기업을 선택한 경우
            df_company = df[df['기업'] == company]
        result = preprocess(df_company, 3)
        ESG_element = st.selectbox("ESG 요소를 선택해주세요.", ["전체", "Environmental", "Social", "Governance"])
        if ESG_element == "전체":
            line = px.line(data_frame= result[0], x="date", y="점수")
            st.write(line)
        elif ESG_element == "Environmental":
            line = px.line(data_frame= result[1], x="date", y="점수")
            st.write(line)
        elif ESG_element == "Social":
            line = px.line(data_frame= result[2], x="date", y="점수")
            st.write(line)
        elif ESG_element == "Governance":
            line = px.line(data_frame= result[3], x="date", y="점수")
            st.write(line)

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