import streamlit  as st
import pandas as pd
from copy import deepcopy



@st.cache_data
def load_data( path):
    df = pd.read_csv(path)
    return df
st.write('hello 1')
# First some MPG Data Exploration
mpg_df_raw = load_data(path="./data/orders.csv")
mpg_df = deepcopy(mpg_df_raw)

st.table(data=mpg_df)

st.write('hello 3')