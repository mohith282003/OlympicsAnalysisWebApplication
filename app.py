import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://th.bing.com/th?id=OIP.NSFMTYUwkqCYP5Jwyiwk2wHaE8&w=306&h=204&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2")
User_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athelete-wise Analysis')
)


if User_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("select year",years)
    selected_country = st.sidebar.selectbox("select country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year =='Overall' and selected_country =='Overall':
        st.title("Overall Tally")
    if selected_year !='Overall' and selected_country =='Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year =='Overall' and selected_country !='Overall':
        st.title(selected_country +" Overall Performance")
    if selected_year !='Overall' and selected_country !='Overall':
        st.title(selected_country+" performance in "+str(selected_year)+" Olympics")
    st.table(medal_tally)

if User_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Atheletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x='Year', y='count')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(event_over_time, x='Year', y='count')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athelete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athelete_over_time, x='Year', y='count')
    st.title("Athelets over the years")
    st.plotly_chart(fig)
    st.title("Number of events over time(Every Sport")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successfull Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox(df,sport_list)

    x=helper.sucess(df,selected_sport)
    st.table(x)
if User_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)


    country_df = helper.year(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+" Medal Tally Over The Years")
    st.plotly_chart(fig)
    st.title(selected_country+" excels over the years")
    pt  = helper.country_event(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)

    st.pyplot(fig)
    st.title("Top 10 atheletes of"+selected_country)
    top_df = helper.sucess_region(df,selected_country)
    st.table(top_df)

if User_menu == 'Athelete-wise Analysis':

    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.show()
    fig.update_layout(autosize = False,width = 1000,height = 600)
    st.title("Distribution of age")
    st.plotly_chart(fig)

    x = []
    name = []
    y = ['Basketball', 'Judo', 'Athletics', 'Swimming', 'Badminton', 'Gymnastics', 'Wrestling', 'Shooting',
         'Volleyball', 'Rugby', 'Ice Hockey']
    for sport in y:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution og age wrt Sports")
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)
    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


