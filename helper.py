from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extractor = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
        
    # Fetching Total No. of Messages
    Number_of_Messages = df.shape[0]
        
    # Fetching Total No. of Words
    words = []
    for message in df['Messages']:
        words.extend(message.split(" "))

    # Fetching Total No. of Media shared
    Number_of_Media = df[df['Messages'] == '<Media omitted>\n'].shape[0]  

    # Feteching Total No. of Links Shared in the Group
    Links = []
    for message in df['Messages']:
        Links.extend(extractor.find_urls(message))

    return Number_of_Messages,len(words),Number_of_Media,len(Links)

def most_busy_users(df):
    x = df['Users'].value_counts().head()
    df = round((df['Users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'Users':'Names','count':'Percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    
    f = open('StopWords_Hinglish.txt','r')
    Stop_Words = f.read()
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]

    temp = df[df['Users'] != 'Group Notification'] 
    temp = temp[temp['Messages'] != '<Media omitted>\n']
    
    def remove_stop_words(Messages):
        y = []
        for word in Messages.lower().split():
            if word not in Stop_Words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=800, height=800, min_font_size=10,background_color='white')
    temp['Messages'] = temp['Messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Messages'].str.cat(sep=" "))
    return df_wc

def Most_Common_Words(selected_user,df):
    
    f = open('StopWords_Hinglish.txt','r')
    Stop_Words = f.read()

    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    temp = df[df['Users'] != 'Group Notification'] 
    temp = temp[temp['Messages'] != '<Media omitted>\n']
    
    common_words = []
    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in Stop_Words:
                common_words.append (word)

    Common_Words_df = pd.DataFrame(Counter(common_words).most_common(25))
    return Common_Words_df

def emoji_helper(selected_user, df):

    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common())
    return emoji_df

def monthly_timeline(selected_user,df):
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    Timeline = df.groupby(['Year','Month_Num','Month']).count()['Messages'].reset_index()

    time=[]
    for i in range(Timeline.shape[0]):
        time.append(Timeline['Month'][i]+ " - " + str(Timeline['Year'][i]))

    Timeline['Time'] = time

    return Timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]

    Daily_Timeline = df.groupby('Date_Only').count()['Messages'].reset_index()
    return Daily_Timeline

def weekly_activity_map(selected_user,df):
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    return df['Day_Name'].value_counts()

def Monthly_activity_map(selected_user,df):
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    return df['Month_Name'].value_counts()

def activity_heatmap(selected_user,df):
    
    if selected_user != 'Overall Analysis':
        df = df[df['Users'] == selected_user]
    
    activity_heatmap =  df.pivot_table(index='Day_Name',columns='Period',values='Messages',aggfunc='count').fillna(0)
    return activity_heatmap