import streamlit as st
import pandas as pd

# 실행방법
# streamlit run test2.py

st.write("""
# My first app
Hello *world!*
""")
 

if st.button('데이터보기'):
    st.write('버튼이 눌러졌습니다.')
    df=pd.read_csv('/content/sample_data/topic1_newsvolume.csv')
    st.dataframe(df)

name = 't_nv'
if st.button('이름확인'):
    st.write(name.upper())

if st.button('이름확인', key='btn2'):
    st.write(name.lower())

#df = pd.read_csv("my_data.csv")
#t.line_chart(df)