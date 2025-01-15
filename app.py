import streamlit as st
import Preprocessing, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert it to String
    data = bytes_data.decode("utf-8")
    # To preprocess
    df = Preprocessing.preprocess(data)
    # st.dataframe(df) (No need to print our personal messages)

    # Fetching unique users
    user_list = df['Users'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'Overall Analysis')

    # Whatever user will select, will be here in select_user
    selected_user = st.sidebar.selectbox('Show Analysis w.r.t', user_list) 
    
    if st.sidebar.button("Show Analysis"):
        ## For Total No. of Messages, words (THE STATS AREA)
        Number_of_Messages, words, Number_of_Media,Number_of_Links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        Col_1, Col_2, Col_3, Col_4 = st.columns(4)
        
        with Col_1:
            st.header("Total No. of Messages")
            st.title(Number_of_Messages)

        with Col_2:
            st.header("Total No. of Words")
            st.title(words)
        
        with Col_3:
            st.header("Media Shared")
            st.title(Number_of_Media)

        with Col_4:
            st.header("Links Shared")
            st.title(Number_of_Links)

    # Monthly TimeLine
    st.title('Analyzing Monthly Timeline')
    Timeline = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots(figsize=(10, 5))
    ax.plot(Timeline['Time'],Timeline['Messages'],color='green')
    plt.xticks(rotation='horizontal')
    plt.tick_params(axis='x', labelsize=7)
    st.pyplot(fig)

    # Daily Timeline
    st.title('Analyzing Daily Timeline')
    Daily_Timeline = helper.daily_timeline(selected_user,df)
    fig,ax = plt.subplots(figsize=(10, 5))
    ax.plot(Daily_Timeline['Date_Only'],Daily_Timeline['Messages'],color='orange')
    plt.xticks(rotation='horizontal')
    plt.tick_params(axis='x', labelsize=7) 
    st.pyplot(fig)

    # Weekly Activity Map
    st.title('Weekly Activity Map')
    col1,col2 = st.columns(2)

    # Monthly Activity Map
    st.title('Monthly Activity Map')

    
    with col1:
        st.header('Most Busy Day')
        busy_day = helper.weekly_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.tick_params(axis='x', labelsize=7) 
        st.pyplot(fig)

    with col2:
        st.header('Most Busy Month')
        busy_month = helper.Monthly_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color='green')
        plt.tick_params(axis='x', labelsize=6)
        st.pyplot(fig)    

    ## Finding the busiest user in the group (Group Level)
    if selected_user == 'Overall Analysis':
        st.title('Most Active Users')
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        Col1, Col2 = st.columns(2)

        with Col1:
            ax.bar(x.index,x.values,color='navy')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with Col2:
            st.dataframe(new_df, width=550, height=570)

    # WordCloud
    st.title('WordCloud')
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots(figsize=(20, 5))
    ax.imshow(df_wc)
    st.pyplot(fig)

    # Most Common Words
    st.title('Most Common Words')
    Common_Words_df = helper.Most_Common_Words(selected_user,df)
    fig,ax = plt.subplots(figsize=(10, 5))
    ax.barh(Common_Words_df[0],Common_Words_df[1])
    st.pyplot(fig)

    # Emoji Analysis
    emoji_df = helper.emoji_helper(selected_user,df)
    st.title('Emoji Analysis')
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(emoji_df, width= 480, height=550)
    
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels= emoji_df[0].head(), autopct='%0.2f')
        st.pyplot(fig)

    # Activity Heatmap
    st.title('Weekly Activity HeatMap')
    activity_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots(figsize=(10, 5))
    ax = sns.heatmap(activity_heatmap)
    st.pyplot(fig)