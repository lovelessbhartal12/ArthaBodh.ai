import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("google_api_key"))

prompts="""you are youtube summarizer . you will be taking the transcript text and summarize the entire video in the 200 words. the transcript text will be append here.  """

def youtube_Trasncrpit(youtube_video_url):
    try:

        video_id=youtube_video_url.split("=")[1]
        transcript_Text=YouTubeTranscriptApi.fetch(video_id)

        transcript=" "

        for i in transcript_Text:
            transcript_Text +=" " +i["text"]

        return transcript_Text



    except Exception as e:
        raise e

def generate_gemini(transcript_text):
    model=genai.GenerativeModel("gemini-pro")

    response=model.generate_content(prompts+transcript_text)
    return response.text


#app

st.title("youtube transcript to detailed notes converter")
youtube_link=st.text_input("enter your youtube link")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)

if st.button(" Get Detailed notes"):
    transcript_text=youtube_Trasncrpit(youtube_link)

    if transcript_text:
        summary=generate_gemini(transcript_text ,prompts)

        st.markdown("## Detailed Notes")
        st.write(summary)
