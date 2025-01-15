import pandas as pd
import re

def preprocess(data):
    pattern=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message':messages, 'message_date':dates})
    #Converting message_data type 
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    df.rename(columns={'user_message':'Messages By Users','message_date':'Date'},inplace=True)

    users = []
    messages = []

    for message in df['Messages By Users']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])
    
    df['Users'] = users
    df['Messages'] = messages
    df.drop(columns=['Messages By Users'], inplace=True)

    
    df['Year'] = df['Date'].dt.year
    df['Month_Num'] = df['Date'].dt.month

    df['Date_Only'] = df['Date'].dt.date

    df['Day_Name'] = df['Date'].dt.day_name()
    df['Month_Name'] = df['Date'].dt.month_name()

    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day

    df['Hours'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period=[]
    for hr in df['Hours']:
        if hr == 23:
            period.append(str(hr) + "-" + str('00'))
        elif hr == 0:
            period.append(str('00') + "-" + str(hr+1))
        else:
            period.append(str(hr) + "-" + str(hr+1))

    df['Period'] = period
    
    return df