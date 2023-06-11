# all of this is for the two people chat 

import streamlit  as st 
import pandas as pd 
from pandas import *



import time 



import matplotlib.pyplot as plt

import seaborn as sns


import plotly.express as px
import plotly.graph_objects as go

import emoji
from collections import Counter



def process(file):

    df = pd.read_table(file, delimiter='~', error_bad_lines=False)
    df['Date'] = pd.to_datetime(df.iloc[:, 0].str.split(' - ').str[0], format='%m/%d/%y, %H:%M', errors='coerce')
    df['User_Message'] = df.iloc[:, 0].str.split(' - ').str[1]
    df[['User', 'Message']] = df['User_Message'].str.split(': ', 1, expand=True)
    df.drop(columns=['User_Message'], inplace=True)

    df.drop(columns=df.columns[0], inplace=True)

    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month_name()
    df['days'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    df.drop(columns=['Date'],inplace=True)



    st.dataframe(df, use_container_width=True)
    st.sidebar.image(image="whats.app.jpg")

    # Sidebar multiselect for users
    # Get the two most common users
    top_users = df['User'].value_counts().nlargest(2).index.tolist()

    # Create the multiselect sidebar with the top users as options
    selected_users = st.sidebar.multiselect("Selected users", top_users)

    # Filter the DataFrame based on the selected users
    filtered_df = df[df['User'].isin(selected_users)]
    
    ## values and the stats of the dataset
    st.write("Total Rows and Columns:", df.shape)
    df['user'] = df['User'].str.extract(r'\+\d{2}\s\d{10}|([\w\s]+)', expand=False)

    unique_users = df['User'].nunique()

    if unique_users == 2:
        total_users = unique_users
    else:
        total_users = 2  

    st.write("Total Users:", total_users)

    # Concatenate all messages into a single string
    text = ' '.join(df['Message'].dropna())

    # Count the total number of words
    total_word_count = len(text.split())

    # Display the total word count on Streamlit
    st.write("Total Word Count:", total_word_count)

     # Count the occurrences of each emoji in the 'Message' column
    emoji_counts = Counter(emoji.demojize(text) for text in df['Message'] if pd.notnull(text) and emoji.demojize(text) != text)

    # Create a new DataFrame from the emoji counts
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Count'])

    # Replace the emoji names with actual emojis
    emoji_df['Emoji'] = emoji_df['Emoji'].apply(emoji.emojize)

    # Select the top 15 emojis
    top_15_emojis = emoji_df.head(15)

    # Convert the dataframe to HTML
    emoji_df_html = top_15_emojis.to_html(index=False, escape=False)

    # Display the dataframe with emojis in Streamlit
    st.markdown(emoji_df_html, unsafe_allow_html=True)
    
    words = ['fuck', 'stud', 'bow', 'bullshit', 'bs', 'ass', 'motherfucker', 'bsdk']
    df['Contains_Prohibited_Word'] = df['Message'].str.contains('|'.join(words), case=False)

    prohibited_messages = df.loc[df['Contains_Prohibited_Word'].fillna(False), ['User', 'Message']]
    prohibited_messages['Prohibited Words'] = prohibited_messages['Message'].apply(lambda x: [word for word in x.split() if word.lower() in words])

    prohibited_messages = prohibited_messages[prohibited_messages['Prohibited Words'].map(lambda x: bool(x))]

    if not prohibited_messages.empty:
        prohibited_df = prohibited_messages[['User', 'Prohibited Words']]
        st.write(prohibited_df, use_container_width=True)
    else:
        st.write("No prohibited words found.")

    st.markdown("**Please give it a minute, it may take time since you Gossip a lot  😫**")


    # Calculate the count of each unique year in the 'Year' column
    year_counts = df['year'].value_counts()


    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0)
    status_text = st.empty()

    for percent_complete in range(100):
        time.sleep(0.1)
        progress_bar.progress(percent_complete + 1)
        status_text.text(f"{progress_text} {percent_complete + 1}%")

        status_text.text("Operation completed!")

    st.markdown(
    "<p style='font-size: 18px; font-weight: bold; background-color: GREEN padding: 10px;, color: black;'>This is the most commonly used words between you and your Friends</p>",
    unsafe_allow_html=True
)
    
    # Calculate the count of each unique year in the 'Year' column
    year_counts = df['year'].value_counts()

    # Get the unique years and their counts
    years = year_counts.index
    counts = year_counts.values

    # Define a custom color palette
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink', 'lightyellow']

    # Define the explode values to emphasize a slice (optional)
    explode = [0.1] + [0] * (len(years) - 1)  # Explode the first slice

    # Create the pie chart with labels and values
    fig2, ax = plt.subplots(figsize=(10, 7))
    ax.pie(counts, labels=years, colors=colors, explode=explode, shadow=True, startangle=90)

    # Add a title
    ax.set_title('Year Distribution', fontsize=16)

    # Add a legend
    ax.legend(title='Years', loc='best', fontsize=12)

    # Adjust the font size of labels
    plt.rcParams['font.size'] = 12

    # Set an aspect ratio for a circular pie chart
    ax.axis('equal')

    # Display the pie chart in Streamlit
    st.pyplot(fig2)

    num_users = 5
    unique_users = df['User'].unique()
    sampled_users = random.sample(list(unique_users), num_users)

    value_counts = df['User'].value_counts()
    sampled_value_counts = value_counts[value_counts.index.isin(sampled_users)]

    top_users = sampled_value_counts.nlargest(2).index.tolist()
    filtered_sampled_users = [user for user in sampled_users if user in top_users]
    filtered_sampled_value_counts = sampled_value_counts[sampled_value_counts.index.isin(filtered_sampled_users)]

    data = {'names': filtered_sampled_users, 'values': filtered_sampled_value_counts.tolist()}

    fig2 = go.Figure(data=[go.Bar(x=data['names'], y=data['values'], marker_color='blue')])
    fig2.update_layout(title_text='User Value Counts', xaxis_title="User", yaxis_title="Value Count")
    fig2.show() 
    
   
    # progress bar 
    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0)
    status_text = st.empty()

    for percent_complete in range(100):
        time.sleep(0.1)
        progress_bar.progress(percent_complete + 1)
        status_text.text(f"{progress_text} {percent_complete + 1}%")

        status_text.text("Operation completed!")

    values = df['User'].value_counts().nlargest(2).index.tolist()

    # Create a pivot table based on the most common values
    sentiment_heatmap = df.pivot_table(index='User', values='Message', aggfunc='count', fill_value=0)
    sentiment_heatmap = sentiment_heatmap.loc[values]  # Filter the pivot table based on the most common values

    # Plot the sentiment heatmap
    fig3, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(sentiment_heatmap, cmap='coolwarm', annot=True, fmt='d', ax=ax)
    plt.title('Sentiment Heatmap')
    plt.xlabel('Sentiment')
    plt.ylabel('User')
    plt.tight_layout()
    st.pyplot(fig3)


    # Get the two most common values from the 'User' column
    values = df['User'].value_counts().nlargest(2).index.tolist()

    # Filter the DataFrame based on the most common values
    filtered_df = df[df['User'].isin(values)]

    # Plot the histogram using Plotly Express in Streamlit
    fig4 = px.histogram(filtered_df, x='User')
    st.plotly_chart(fig4, use_container_width=True)

    # Create the histogram plot using Plotly Express
    fig5 = px.histogram(df, x='month', template='plotly_white', title='Complaint counts by date')
    fig5.update_xaxes(categoryorder='category descending', title='Date').update_yaxes(title='How Active')

    # Display the histogram plot in Streamlit
    st.plotly_chart(fig5, use_container_width=True)


   # plots by days 
    fig6 = px.histogram(df, x='days', template='plotly_white', title="how active by hour"
                    , color='hour', nbins=6, log_y=True, barmode='group')
    fig6.update_xaxes(categoryorder='category descending', title='Date').update_yaxes(title='how active by hour')
    st.plotly_chart(fig6, use_container_width=True)
    
   # plots by mins 
    fig7 = px.histogram(df, x='days', template='plotly_white', title='how active by mins'
                   , color='minute', nbins=6, log_y=True, barmode='group')
    fig7.update_xaxes(categoryorder='category descending', title='Date').update_yaxes(title='how active by mins ')
    
    st.plotly_chart(fig7, use_container_width=True)   
    # plots by days 
    fig8 = px.histogram(df, x='days', template='plotly_white', title= "how active by days"
                   , color='days', nbins=6, log_y=True, barmode='group')
    fig8.update_xaxes(categoryorder='category descending', title='Date').update_yaxes(title='how active by days')
    st.plotly_chart(fig8, use_container_width=True)
    
