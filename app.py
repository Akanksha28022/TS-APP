import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the Streamlit app
st.title('Sustainable Living Tips')

# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'Track Progress', 'Visualize Progress'])

# Sustainable living tips
tips = [
    "Reduce, Reuse, Recycle",
    "Use energy-efficient appliances",
    "Reduce water usage",
    "Use public transportation or carpool",
    "Eat more plant-based meals",
    "Reduce single-use plastics",
    "Compost organic waste",
    "Support renewable energy sources",
    "Buy locally produced goods",
    "Plant a tree or start a garden"
]

# Home Page
if page == 'Home':
    st.header('Welcome to Sustainable Living Tips')
    st.write('Here are some tips to help you live a more sustainable lifestyle:')
    for tip in tips:
        st.write(f"- {tip}")

# Track Progress Page
elif page == 'Track Progress':
    st.header('Track Your Progress')

    # Load or initialize progress data
    if 'progress' not in st.session_state:
        st.session_state.progress = pd.DataFrame(columns=['Tip', 'Date'])

    # Input for tracking progress
    tip = st.selectbox('Select a tip to track', tips)
    date = st.date_input('Date')

    # Button to add progress
    if st.button('Add Progress'):
        st.session_state.progress = st.session_state.progress.append({'Tip': tip, 'Date': date}, ignore_index=True)
        st.success('Progress added!')

    # Display progress
    st.write('Your Progress:')
    st.dataframe(st.session_state.progress)

# Visualize Progress Page
elif page == 'Visualize Progress':
    st.header('Visualize Your Progress')

    if 'progress' not in st.session_state or st.session_state.progress.empty:
        st.write('No progress to visualize.')
    else:
        # Plot progress over time
        progress = st.session_state.progress
        progress['Count'] = 1
        progress_over_time = progress.groupby(['Date', 'Tip']).count().unstack().fillna(0)

        st.write('Progress Over Time:')
        st.line_chart(progress_over_time)

        # Plot distribution of tips
        st.write('Distribution of Tips:')
        tip_distribution = progress['Tip'].value_counts()
        fig, ax = plt.subplots()
        tip_distribution.plot(kind='bar', ax=ax)
        plt.title('Distribution of Tips')
        plt.xlabel('Tip')
        plt.ylabel('Count')
        st.pyplot(fig)
