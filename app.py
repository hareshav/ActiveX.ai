# from datacall import pushdata
from pymongo import MongoClient
import pandas as pd
import streamlit as st
import os
import src.AdsetPlot as adsetplot
import src.copyplots as copyplots
import src.insights as insights
import src.timeplot as timeplot
import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
import uuid
import facebook
from PIL import Image
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from facebook_business.api import FacebookAdsApi
l=["com_adset_df.csv","plots_adset_df.csv","res_less_than_1_adset_df.csv","res_more_than_1_adset_df.csv"]
st.set_page_config(layout="wide")
st.sidebar.title("Sidebar")
def load_data(collection_name):
    df=pd.read_csv('data/'+collection_name+'.csv')
    return df
if 'data_fetched' not in st.session_state:
    with st.spinner("Initializing Data in Session States"):
        st.session_state["campaign_platform"]=load_data(f"campaign_platform")
        st.session_state["campaign_targeting"]=load_data(f"campaign_targeting")
        st.session_state["campaign_age_gender"]=load_data(f"campaign_age_gender")
        st.session_state["campaign_title"]=load_data(f"campaign_title")
        st.session_state["campaign_body"]=load_data(f"campaign_body")
        st.session_state["main_campaigns"]=load_data(f"main_campaigns")
        st.session_state["default_df"]=load_data(f"default_df")
        st.session_state["campaign_hourly"]=load_data(f"campaign_hourly")
        st.session_state["campaign_daily"]=load_data(f"campaign_daily")
        st.session_state["adset_targeting"]=load_data(f"adset(targeting)")
        st.session_state["adset_platform"]=load_data(f"adset_platform")
        st.session_state["adset_age_gender"]=load_data(f"adset_age_gender")
        st.session_state["adset_title"]=load_data(f"adset_title")
        st.session_state["adset_body"]=load_data(f"adset_body")
        st.session_state["adset_hourly"]=load_data(f"adset_hourly")
        st.session_state["adset_daily"]=load_data(f"adset_daily")
        st.session_state['data_fetched']=True

option = st.sidebar.selectbox(
    'Select an option:',
    (['Generation','Dashboard'])
)
if option=='Dashboard':
    campaign_platform=st.session_state["campaign_platform"]
    campaign_targeting=st.session_state["campaign_targeting"]
    campaign_age_gender=st.session_state["campaign_age_gender"]
    campaign_title=st.session_state["campaign_title"]
    campaign_daily=st.session_state['campaign_daily']
    adset_body=st.session_state["adset_body"]
    cam=st.session_state['main_campaigns']
    t=st.selectbox("Choose group:",cam['name'][20:].drop_duplicates())
    id=cam[cam['name']==t]
    campaign_age_gender=campaign_age_gender[campaign_age_gender['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
    adset_body=adset_body[adset_body['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
    campaign_platform=campaign_platform[campaign_platform['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
    campaign_daily=campaign_daily[campaign_daily['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
    campaign_age_gender['spend']=campaign_age_gender['spend'].astype(float)
    campaign_platform['spend']=campaign_platform['spend'].astype(float)
    campaign_platform['clicks']=campaign_platform['clicks'].astype(float)
    campaign_age_gender['clicks']=campaign_age_gender['clicks'].astype(float)
    campaign_platform['cpc']=campaign_platform['cpc'].astype(float)
    campaign_targeting['cpc']=campaign_targeting['cpc'].astype(float)
    columns_to_check = ['name', 'address', 'price', 'size', 'emoji']
    adset_body['attributes'] =  adset_body.apply(
        lambda row: ', '.join([col for col in columns_to_check if row[col] != '']),
        axis=1,
    )
    col1, col2 = st.columns([1,2])
    with col1:
        fixed_scrollable_css = """
        <style>
        .fixed-column {
            height: 4px; /* Adjust height as needed */
            overflow-y: auto;
        }
        </style>
        """

        # Inject CSS into the Streamlit app
        st.markdown(fixed_scrollable_css, unsafe_allow_html=True)

        # Create tabs
        tabs = st.tabs(["Platform Insights", "Age Gender Insights", "Attribute Insights"])

        # Content for Platform Insights
        with tabs[0]:
            st.header('Platform Insights')
            st.markdown('<div class="scrollable">', unsafe_allow_html=True)
            # Replace with your actual function call
            insights.platforminsights(campaign_platform)
            st.markdown('</div>', unsafe_allow_html=True)

        # Content for Age Gender Insights
        with tabs[1]:
            st.header('Age Gender Insights')
            st.markdown('<div class="scrollable">', unsafe_allow_html=True)
            # Replace with your actual function call
            insights.age_gender_insights(campaign_age_gender)
            st.markdown('</div>', unsafe_allow_html=True)

        # Content for Attribute Insights
        with tabs[2]:
            st.header('Attribute Insights')
            st.markdown('<div class="scrollable">', unsafe_allow_html=True)
            # Replace with your actual function call
            insights.attributeinsights(adset_body)
            st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        col1, col2 = st.columns([2,2])
        with col1:
            st.plotly_chart(timeplot.plot_cumulative_leads(campaign_daily))
        with col2:
            st.plotly_chart(timeplot.plot_cumulative_link_clicks(campaign_daily))
    # st.write(insights.generate_adset_json(campaign_platform,campaign_age_gender,adset_body))
    tab1, tab2, tab3 = st.tabs(['Adset insights','Copy insights','Time Insights'])
    with tab1:
        campaign_platform=st.session_state["campaign_platform"]
        campaign_targeting=st.session_state["campaign_targeting"]
        campaign_age_gender=st.session_state["campaign_age_gender"]
        df4=st.session_state["campaign_title"]
        df5=st.session_state["campaign_body"]
        campaign_age_gender=campaign_age_gender[campaign_age_gender['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        df5=df5[df5['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        campaign_platform=campaign_platform[campaign_platform['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        col1, col2, col3, col4 = st.columns(4)
        with col4:
            chart_tab = st.selectbox(
            'Select Chart Tab:',
            ('Leads and Spends', 'Clicks and Spends', 'Link Clicks and Spends', 'Link Clicks and Leads','Leads and Lead_per_link_click')
        )
        campaign_age_gender['spend']=campaign_age_gender['spend'].astype(float)
        campaign_platform['spend']=campaign_platform['spend'].astype(float)
        campaign_age_gender['clicks']=campaign_age_gender['clicks'].astype(float)
        campaign_age_gender['cpl']=campaign_age_gender['spend']/campaign_age_gender['lead']
        campaign_platform['cplc']=campaign_platform['spend']/campaign_platform['link_click']
        campaign_age_gender['cplc']=campaign_age_gender['spend']/campaign_age_gender['link_click']
        #seg1 leads and cpl placement
        #seg2 clicks and cpc placement
        #seg3 leads and cpl gender'
        #seg4 clicks and cpc gender'
        #seg5 link_click and cplc placement
        #seg6 link_clicl and cplc gender

        st.title('Aggregated Charts')
        if chart_tab=='Leads and Spends':
            st.write('### Insights of publisher platform and platform position using leads and spend')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg1df1(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg1df2(campaign_platform), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg1df3(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg1df4(campaign_platform), use_container_width=True)

            st.write('### Insights of age and gender using lead and spend')
            col1, col2,col3 = st.columns(3)
            with col1:
                st.plotly_chart(adsetplot.seg3df1(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg3df2(campaign_age_gender), use_container_width=True)
            with col3:
                st.plotly_chart(adsetplot.seg3df3(campaign_age_gender), use_container_width=True)
            col1, col2,col3 = st.columns(3)
            with col1:
                st.plotly_chart(adsetplot.seg3df4(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg3df5(campaign_age_gender), use_container_width=True)
            with col3:
                st.plotly_chart(adsetplot.seg3df6(campaign_age_gender), use_container_width=True)
        if chart_tab=='Clicks and Spends':        
            st.write('### Insights of publisher platform and platform position using clicks and spend')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg2df1(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg2df2(campaign_platform), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg2df3(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg2df4(campaign_platform), use_container_width=True)

            st.write('### Insights of age and gender using clicks and spend')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg4df1(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg4df2(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg4df3(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg4df4(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg4df5(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg4df6(campaign_age_gender), use_container_width=True)
        if chart_tab=='Link Clicks and Spends':  
            st.write('### Insights of publisher platform and platform position using Link clicks and spend')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg5df1(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg5df2(campaign_platform), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg5df3(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg5df4(campaign_platform), use_container_width=True)
            st.write('### Insights of age and gender using Link Click and spend')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg6df1(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg6df2(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg6df3(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg6df4(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg6df5(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg6df6(campaign_age_gender), use_container_width=True)
        # store it in session state
        # display the behavour and targeting
        # create a code with link_clicks
        if chart_tab=='Link Clicks and Leads':
            st.write('### Insights of Platform positions using lead, Link Click and spend ')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg7df1(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg7df2(campaign_platform), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg7df3(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg7df4(campaign_platform), use_container_width=True)

            st.write('### Insights of age and gender using lead, Link Click and spend ')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg8df1(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg8df2(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg8df3(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg8df4(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg8df5(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg8df6(campaign_age_gender), use_container_width=True)
        if chart_tab=='Leads and Lead_per_link_click':
            st.write('### Insights of Placements Position using linkclick, lead per link click  and spend ')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg9df1(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg9df2(campaign_platform), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg9df3(campaign_platform), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg9df4(campaign_platform), use_container_width=True)
            st.write('### Insights of age and gender using linkclick, lead per link click  and spend ')
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg10df1(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg10df2(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg10df3(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg10df4(campaign_age_gender), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(adsetplot.seg10df5(campaign_age_gender), use_container_width=True)
            with col2:
                st.plotly_chart(adsetplot.seg10df6(campaign_age_gender), use_container_width=True)

    with tab2:    
        campaign_platform=st.session_state["campaign_platform"]
        campaign_targeting=st.session_state["campaign_targeting"]
        campaign_age_gender=st.session_state["campaign_age_gender"]
        campaign_title=st.session_state["campaign_title"]
        adset_body=st.session_state["adset_body"]
        cam=st.session_state['main_campaigns']
        campaign_age_gender=campaign_age_gender[campaign_age_gender['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        adset_body=adset_body[adset_body['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        campaign_platform=campaign_platform[campaign_platform['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        col1, col2, col3, col4 = st.columns(4)
        st.header("Analysis Type")
        with col4:
            analysis_type = st.selectbox(
                "Choose the type of analysis:",
            ["Attributes","First Words", "First 20 Words", "First 4 Words",
            "Payment", "Exclamation Mark",
            "Name", "Address", "Price", "Emoji (Price-based)"]
        )
        def firstword(x):
            return " ".join(x.split()[:2])
        adset_body['word']=adset_body['asset_text'].apply(lambda x:firstword(x))
        adset_body['empty']=1
        adset_body.dropna()
        columns_to_check = ['name', 'address', 'price', 'size', 'emoji']
        # Create the 'non_empty_columns' column with names of non-empty columns for the specified columns
        adset_body['attributes'] =  adset_body.apply(
            lambda row: ', '.join([col for col in columns_to_check if pd.notna(row[col]) and row[col] != '']),
            axis=1
        )

        # Main area based on sidebar selection
        if analysis_type == "First Words":
            st.header("Bigram Word Cloud Analysis - Single Words")
            st.write("Impact of individual words on clicks, link clicks, and spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'word', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'word', "link_click", "spend")
            st.write("Effect of words on clicks and link clicks without considering spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'word', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'word', "link_click", "empty")
            st.write("Labels\nN-Name\nA-Address\nE-Emoji\nP-Price,PaymentAttributes\n")

        elif analysis_type=="Attributes":
            adset_body['attributes'].dropna()
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.attributesLinkclicks(adset_body))
            with col2:
                st.plotly_chart(copyplots.attributesClick(adset_body))
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.attributeslplc(adset_body))
            with col2:
                st.plotly_chart(copyplots.linkclickattributes(adset_body))
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.cplcattributes(adset_body))
            with col2:
                st.plotly_chart(copyplots.clickattributes(adset_body))
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.cpcattributes(adset_body))
            with col2:
                st.plotly_chart(copyplots.lplcattributes(adset_body))

        elif analysis_type == "First 20 Words":
            st.header("Bigram Word Cloud Analysis - First 20 Words")
            st.write("Impact of the first 20 words on clicks, link clicks, and spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'First 20 words', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'First 20 words', "link_click", "spend")
            st.write("Effect of the first 20 words on clicks and link clicks without considering spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'First 20 words', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'First 20 words', "link_click", "empty")

        elif analysis_type == "First 4 Words":
            st.header("Bigram Word Cloud Analysis - First 4 Words")
            st.write("Impact of the first 4 words on clicks, link clicks, and spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'First 4 words', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'First 4 words', "link_click", "spend")
            st.write("Effect of the first 4 words on clicks and link clicks without considering spend.")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'First 4 words', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'First 4 words', "link_click", "empty")

        elif analysis_type == "Payment":
            st.header("Bubble Chart Analysis - Payment")
            st.plotly_chart(copyplots.paymentLinkclick(adset_body))
            st.plotly_chart(copyplots.paymentclick(adset_body))
            st.plotly_chart(copyplots.paymentlplc(adset_body))

        elif analysis_type == "Exclamation Mark":
            st.header("Bubble Chart Analysis - Exclamation Mark")
            st.plotly_chart(copyplots.exclamationLinkclick(adset_body))
            st.plotly_chart(copyplots.exclamationClick(adset_body))
            st.plotly_chart(copyplots.exclamationlplc(adset_body))

        elif analysis_type == "Name":
            st.header("Bubble Chart Analysis - Name")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'name', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'name', "link_click", "spend")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'name', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'name', "link_click", "empty")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.nameLinkclick(adset_body))
            with col2:  
                st.plotly_chart(copyplots.nameClick(adset_body))

        elif analysis_type == "Address":
            st.header("Bubble Chart Analysis - Address")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'address', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'address', "link_click", "spend")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'address', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'address', "link_click", "empty")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.addressLinkclick(adset_body))
            with col2:
                st.plotly_chart(copyplots.addressClick(adset_body))

        elif analysis_type == "Price":
            st.header("Bubble Chart Analysis - Price")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'price', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'price', "link_click", "spend")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'price', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'price', "link_click", "empty")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.priceLinkclick(adset_body))
            with col2:
                st.plotly_chart(copyplots.priceClick(adset_body))

        elif analysis_type == "Emoji (Price-based)":
            st.header("Bubble Chart Analysis - Emoji (Price-based)")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'emoji', "clicks", "spend")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'emoji', "link_click", "spend")
            col1, col2 = st.columns(2)
            with col1:
                copyplots.create_bigram_wordcloud(adset_body, 'emoji', "clicks", "empty")
            with col2:
                copyplots.create_bigram_wordcloud(adset_body, 'emoji', "link_click", "empty")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.exclamationLinkclick(adset_body))
            with col2:
                st.plotly_chart(copyplots.exclamationClick(adset_body))
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(copyplots.emojiLinkclick(adset_body))
            with col2:
                st.plotly_chart(copyplots.emojiClick(adset_body))

    with tab3:
        
        campaign_hourly=st.session_state["campaign_hourly"]
        campaign_hourly=campaign_hourly[campaign_hourly['campaign_id']==id['campaign_id'][id['campaign_id'].index[0]]]
        col1, col2, col3, col4 = st.columns(4)
        with col4:
            yaxis = st.selectbox("Select in Column 1", ["spend","impressions","clicks","lead","link_click","cpm","cpc","cpl"])
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(timeplot.bar_plot_insights(campaign_hourly,yaxis))
            st.plotly_chart(timeplot.line_plot_insights(campaign_hourly,yaxis))
        with col2:
            st.plotly_chart(timeplot.create_heatmap(campaign_hourly,yaxis))
if option=='Generation':
    load_dotenv()

    # Initialize Google Generative AI
    api_key = "AIzaSyCF4LEk9GiPZQbwtRJZCSD_5rCCKJutgEI"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Streamlit app title
    st.title("AI-Powered Ad Content Generator & Facebook Ad Uploader")

    # Initialize session state variables if not already set
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None
    if 'image_description' not in st.session_state:
        st.session_state.image_description = None
        
    def upload_image_and_get_hash(image_file, ad_account_id, access_token):
        # Define the directory and create it if it doesn't exist
        save_directory = 'F:\Projects\hackathon'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        # Create a unique filename for the uploaded image
        unique_filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(save_directory, unique_filename)
        print(file_path)

        # Save the uploaded image to the specified path
        with open(file_path, 'wb') as f:
            f.write(image_file.read())

        try:
            # Initialize Facebook Ads API
            FacebookAdsApi.init(access_token=access_token)

            # Upload the image
            image = AdImage(parent_id=ad_account_id)
            image[AdImage.Field.filename] = file_path  # Path to your image file
            image.remote_create()

            image_hash = image[AdImage.Field.hash]
            return image_hash
        except Exception as e:
            raise Exception(f"Error uploading image: {str(e)}")

    tab1, tab2 = st.tabs(["Ad Generation", "Facebook Ad Upload"])

    with tab1:
        st.header("Generate AI-Powered Ad Content")

        # Input fields for ad content
        prompt = st.text_input("Enter your ad prompt:", placeholder="E.g., A summer sale for fashion products")
        uploaded_image = st.file_uploader("Optional: Upload an image for the ad", type=["jpg", "png", "jpeg"])
        print(uploaded_image)
        user_content = st.text_area("Optional: Provide specific content", placeholder="Leave empty to generate content")
        target_audience = st.text_input("Define your target audience:", placeholder="E.g., young adults, fashion enthusiasts")
        website_link = st.text_input("Enter the website link for your products:", placeholder="https://example.com")

        # Function to generate ad content using AI
        def generate_ad_content(prompt, target_audience, website_link, image_description=None):
            if image_description:
                ai_prompt = f"""Create an engaging and detailed ad with 10-13 lines of content using the following description: '{image_description}'.
                                The target audience is '{target_audience}'. 
                                Include emojis to make the content more attractive and exciting. 
                                Make sure to incorporate a clickable link to purchase: '{website_link}'. 
                                Avoid using any brackets and ensure the ad title is exactly 3 words."""
            else:
                ai_prompt = f"""Create an engaging and detailed ad with 10-13 lines of content for the following prompt: '{prompt}'.
                                The target audience is '{target_audience}'. 
                                Include emojis to make the content more attractive and exciting. 
                                Make sure to incorporate a clickable link to purchase: '{website_link}'. 
                                Avoid using any brackets and ensure the ad title is exactly 3 words."""

            try:
                response = model.generate_content([ai_prompt])
                return response.text.strip() if response else "Error: No response from AI"
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")
                return "Failed to generate content."

        # Function to generate image description from uploaded image
        def describe_image(image):
            image_bytes = image.read()
            image = Image.open(io.BytesIO(image_bytes))

            try:
                response = model.generate_content(["What is in this photo?", image])
                return response.text.strip() if response else "A high-quality image relevant to the prompt"
            except Exception as e:
                st.error(f"Error describing image: {str(e)}")
                return "Error describing image."

        # Generate content button
        if st.button("Generate Ad Content", key="generate_ad_button"):
            if not user_content and uploaded_image:
                st.session_state.image_description = describe_image(uploaded_image)
                st.write("Generating content based on the uploaded image using AI...")
                st.session_state.generated_content = generate_ad_content(prompt, target_audience, website_link, image_description=st.session_state.image_description)
            elif not user_content:
                st.write("Generating content using AI...")
                st.session_state.generated_content = generate_ad_content(prompt, target_audience, website_link)
            else:
                st.session_state.generated_content = user_content

        # Display the generated content and optional image
        st.subheader("Generated Ad Content")
        if st.session_state.generated_content:
            st.write(st.session_state.generated_content)
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    with tab2:
        st.header("Upload Ad to Facebook")

        # Facebook API inputs
        access_token = st.text_input("Facebook Access Token", type="password")
        app_id = st.text_input("Facebook App ID")
        app_secret = st.text_input("Facebook App Secret", type="password")
        ad_account_id = st.text_input("Ad Account ID", placeholder="act_1234567890")
        page_id = st.text_input("Facebook Page ID")

        # Optional fields from the ad generation (image, link, message)
        image_hash = None
        if uploaded_image and access_token and app_id and app_secret and ad_account_id:
            try:
                image_hash = upload_image_and_get_hash(uploaded_image, ad_account_id, access_token)
                st.write(f"Image Hash: {image_hash}")
            except Exception as e:
                st.error(f"Error uploading image: {str(e)}")

        link = st.text_input("Link to your product page", value=website_link)
        message = st.text_area("Generated Ad Message", value=st.session_state.generated_content or "Your ad content will appear here after generation.")
        
        campaign_name = st.text_input("Campaign Name")
        ad_set_name = st.text_input("Ad Set Name")
        ad_creative_name = st.text_input("Ad Creative Name")
        ad_name = st.text_input("Ad name")

        if st.button("Create Facebook Ad Campaign", key="create_facebook_ad"):
            try:
                # Initialize Facebook Ads API
                FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)
                ad_account = AdAccount(ad_account_id)

                # Step 1: Create Campaign
                campaign = ad_account.create_campaign(params={
                    Campaign.Field.name: campaign_name,
                    Campaign.Field.objective: Campaign.Objective.outcome_traffic,
                    Campaign.Field.status: Campaign.Status.paused,
                    'special_ad_categories': ['NONE']
                })
                st.success(f"Created Campaign with ID: {campaign['id']}")

                # Step 2: Create Ad Set
                ad_set = ad_account.create_ad_set(params={
                    AdSet.Field.name: ad_set_name,
                    AdSet.Field.campaign_id: campaign['id'],
                    AdSet.Field.daily_budget: 10000,
                    AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
                    AdSet.Field.optimization_goal: AdSet.OptimizationGoal.link_clicks,
                    AdSet.Field.bid_amount: 500,
                    AdSet.Field.targeting: {
                        'geo_locations': {'countries': ['US']}
                    },
                    AdSet.Field.status: AdSet.Status.paused
                })
                st.success(f"Created Ad Set with ID: {ad_set['id']}")

                image_hash = image_hash
                api_version = 'v20.0'  # Use the API version you intend to use, e.g., 'v20.0'

                # Initialize the Facebook Ads API
                FacebookAdsApi.init(access_token=access_token)

                # Define the object story specification for the ad creative
                object_story_spec = {
                    "page_id": page_id,
                    "link_data": {
                        "image_hash": image_hash,
                        "link": f"https://facebook.com/{page_id}",
                        "message": message
                    }
                }

                # Define the degrees of freedom specification
                degrees_of_freedom_spec = {
                    "creative_features_spec": {
                        "standard_enhancements": {
                            "enroll_status": "OPT_IN"
                        }
                    }
                }

                # Create the ad creative
                ad_creative = AdCreative(parent_id=ad_account_id)
                ad_creative.remote_create(params={
                    'name': "My Test Creative Comeback",
                    'object_story_spec': object_story_spec,
                    'degrees_of_freedom_spec': degrees_of_freedom_spec,
                })

                # Print the created ad creative ID
                st.success(f"Ad Creative ID: {ad_creative.get_id()}")

                # Create the Ad
                ad_params = {
                    'name': ad_name,  # This can also be made user-defined if needed
                    'adset_id': ad_set['id'],
                    'creative': {'creative_id': ad_creative.get_id()},
                    'status': 'PAUSED',
                }
                ad = ad_account.create_ad(params=ad_params)
                st.success(f"Created Ad with ID: {ad['id']}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.subheader("show adpreview")

        # Input field for ad set ID to update
        ad_preview = st.text_input("Enter the AD_Creative ID for seeing preview")
        
        def display_iframes(links, items_per_row=3, spacing=20):
            for i in range(0, len(links), items_per_row):
                row_links = links[i : i + items_per_row]
                cols = st.columns(len(row_links))
                for col, link in zip(cols, row_links):
                    # Construct the iframe HTML string with desired width and height
                    iframe_html = link['body']
                    col.markdown(iframe_html, unsafe_allow_html=True)

                # Add spacing after each row, except after the last one
                if i + items_per_row < len(links):
                    # You can adjust the spacing by changing the number of empty lines in the Markdown
                    st.markdown(
                        f"<div style='margin-bottom: {spacing}px;'></div>",
                        unsafe_allow_html=True,
                )
                
        if st.button("Generate Ad Preview", key="generate_ad_preview"):
            try:
                # Fetch Ad Creative Preview
                FacebookAdsApi.init(access_token=access_token)
                ad_cre = ad_preview
                fields = []
                params = {
                    'ad_format': 'DESKTOP_FEED_STANDARD',
                }
                FacebookAdsApi.init(access_token=access_token)
                preview = AdCreative(ad_cre).get_previews(fields=fields, params=params)
                pre = list(preview)
                st.write("Ad Preview:")
                # if isinstance(ad_preview, str):
                #     # Directly display the raw HTML string if it is a string
                #     st.write("Iframe HTML:", ad_preview)

                #     # Display the Ad Preview in Streamlit using the iframe
                #     st.components.v1.html(ad_preview, height=250)
                # else:
                #     st.error(f"Unexpected ad preview format: {type(ad_preview)}")
                display_iframes(pre)
                
            except Exception as e:
                st.error(f"Error fetching ad preview: {str(e)}")

        # Section for updating the ad set
        st.subheader("Update Ad Set")

        # Input field for ad set ID to update
        adset_id_to_update = st.text_input("Enter the Ad Set ID to update")
        
        if st.button("Update Ad Set", key="update_adset_button"):
            try:
                # Initialize Facebook Ads API with your credentials
                FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)
                fields = []
                
                params = {
                    'name': 'Updated Ad Set Name',                
                    'daily_budget': 10000,                        
                    'bid_amount': 200,                            
                    'status': 'PAUSED',                           
                    'targeting': {                                
                        'geo_locations': {
                            'countries': ['US']
                        },
                        'age_min': 18,
                        'age_max': 45
                    },
                    # Add more parameters as needed
                }

                # Initialize the AdSet object with the specified Ad Set ID
                adset = AdSet(adset_id_to_update)

                # Update the ad set
                adset.api_update(fields=fields, params=params)
                st.success(f"Ad Set {adset_id_to_update} updated successfully.")
                
            except Exception as e:
                st.error(f"Error updating Ad Set: {str(e)}")