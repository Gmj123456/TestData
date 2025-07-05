import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyB-nus2-iVGS7GdLK3R1ItY4ZV2_1xc804")

# model = genai.GenerativeModel('models/gemini-1.5-flash-002')
model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp')
response = model.generate_content(
    contents="今年温网冠军是谁？",
    tools='google_search_retrieval'
)
print(response)