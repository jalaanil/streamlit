import streamlit  as st
import pandas as pd
from copy import deepcopy
from matplotlib import pyplot as plt

import plotly.graph_objects as go



@st.cache_data
def load_data( path):
    df = pd.read_csv(path)
    return df

# First some MPG Data Exploration
mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

years = ["All"] +  sorted(pd.unique(mpg_df['year']))
year = st.selectbox("Choose Year" , years)
if year == 'All':
    df_reduced = mpg_df
else:
    df_reduced = mpg_df[ mpg_df['year'] == year]

st.title("Introduction to Streamlit")
st.header("MPG data exploration")

#st.table(data=mpg_df)
if st.checkbox("Show dataframe"):
    st.subheader('This is the dataframe')
    st.dataframe( data=df_reduced)


plot_types = ["Matplotlib", "Plotly"]
plot_type = st.radio("Choose Plot Type", plot_types)

fig , ax = plt.subplots()

df_grp = df_reduced.groupby(by='year')
colors = ['Red' , 'Green' , 'Yellow']
markers = ['*' , '^' , 'x']

for i, (name,dgp) in enumerate( df_grp):
    #ax.scatter(x=dgp['hwy'] , y=dgp['cty'] , color=colors[i], marker=markers[i] , label=name )
    dgp.plot.scatter(x='hwy' ,y = 'cty' , ax=ax , color=colors[i], marker=markers[i] , label=name )
ax.set_title( "Highway Vs City Fuel usage")
ax.set_ylabel( 'city')
ax.set_xlabel('highway')

if plot_type == 'Matplotlib':
    st.pyplot(fig)