
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
import json
api_key = "AIzaSyCF4LEk9GiPZQbwtRJZCSD_5rCCKJutgEI"
genai.configure(api_key=api_key)
model2 = genai.GenerativeModel('gemini-1.5-flash'
                              )
text=model2.generate_content(r'provide me targeting max and min age Gender in json of students provide nothing else eg {min_age:,max_age:,genders}').text
print(text)
t='''{
  "min_age": 18,
  "max_age": 25,
  "genders": [1, 2]
}'''
print(len(y))
text=text[8:-5]
dict_string = text


# Convert the string to a dictionary
dictionary = json.loads(dict_string)

# Print the resulting dictionary
print(dictionary['max_age'])