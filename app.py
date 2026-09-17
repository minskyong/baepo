import pandas as pd 
import streamlit as st
import numpy as np

from pathlib import Path
#배포 준비 

st.set_page_config(
    page_title = '판매 대시보드',
    page_icon = '🤔​',
    layout = 'wide'
)

TARGET_DIR = 'data'
TARGET_CSV = 'data.csv'

BASE_DIR = Path(__file__ ).resolve().parent
DATA_PATH = BASE_DIR / 'data'/'data.csv'   
# = DATA_PATH = BASE_DIR / TARGET_DIR / TARGET_CSV

df = pd.read_csv(DATA_PATH)


st.title('판매 대시보드')

with st.sidebar:
    st.header('조회조건')

    region = st.selectbox(
        label = '지역',
        options = ['전체',
               '대전',
              
               '부산',
               '서울',
               
               
               
               ]




)

    minimum_sales = st.slider(
    label = '최소매출',
    min_value = 0,
    max_value = int (df['sales'].max()),
    step = 500_000,
)


filtered = df[df['sales'] >= minimum_sales].copy()

if region != '전체' :
    filtered = filtered[filtered['region'] == region ]


#kpi 설정

# 1. 총 매출
# 2. 총 판매량
# 3. 총 조회수 
total_sales = filtered['sales'].sum()
total_amount = filtered['quantity'].sum()
total_rows = len(filtered)

if  total_rows > 0 :
      average_sales = filtered['sales'].mean()

else : 
     average_sales = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
        st.metric(
            label = '총매출',
            value = f'{total_sales:,}원'
  
        )

with col2:
      st.metric(
            label  = '총판매량',
            value = f'{total_amount:,}개'
      )

with col3:
      st.metric(
            label  = '총 조회수',
            value = f'{total_rows:,}건'
      )


with col4:
      st.metric(
            label  = '평균매출',
            value = f'{average_sales:,}원'
      )

st.divider()
if filtered.empty:
      st.warning('조건 맞는 데이터 없음')
else :
 monthly_sales = filtered.groupby('month',as_index=False)['sales'].sum()

left, right = st.columns([2, 1])

with left :
        st.subheader('월별매출')

st.line_chart(
      monthly_sales,
      x= 'month',
      y = 'sales'
    )




with right:
        st.subheader('조회 데이터')

        st.dataframe(
            filtered,
            hide_index=True,
            column_config={
                'quantity': st.column_config.NumberColumn(
                    '판매량',
                    format='%,d개'
                ),
                'sales': st.column_config.NumberColumn(
                    '매출',
                    format='%,d원'
                )
            }
        )



# uv pip freeze > requirement.txt로 파일 생성 후 pip install -requirement.txt로 다운 가능
