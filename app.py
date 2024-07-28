import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    data = pd.read_csv('your_dataset.csv')  # Replace with your dataset file
    return data

data = load_data()

# Sidebar for user input
st.sidebar.header('User Input Features')
selected_feature = st.sidebar.selectbox('Feature', data.columns)
selected_value = st.sidebar.slider('Value', float(data[selected_feature].min()), float(data[selected_feature].max()), float(data[selected_feature].mean()))

# Filter data based on user input
filtered_data = data[data[selected_feature] <= selected_value]

# Main dashboard
st.title('Data Dashboard')

st.write('## Dataset')
st.write(data.head())

st.write('## Filtered Data')
st.write(filtered_data.head())

st.write('## Data Description')
st.write(data.describe())

st.write('## Visualizations')

# Histogram
st.write('### Histogram')
fig, ax = plt.subplots()
sns.histplot(filtered_data[selected_feature], bins=30, ax=ax)
st.pyplot(fig)

# Scatter plot
st.write('### Scatter Plot')
x_axis = st.sidebar.selectbox('X-axis', data.columns)
y_axis = st.sidebar.selectbox('Y-axis', data.columns)
fig, ax = plt.subplots()
sns.scatterplot(x=data[x_axis], y=data[y_axis], ax=ax)
st.pyplot(fig)

# Line plot
st.write('### Line Plot')
time_series_feature = st.sidebar.selectbox('Time Series Feature', data.columns)
fig, ax = plt.subplots()
sns.lineplot(data=data, x=data.index, y=time_series_feature, ax=ax)
st.pyplot(fig)
