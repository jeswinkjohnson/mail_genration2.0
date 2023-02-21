import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
from googletrans import Translator
import openai


openai.api_key = st.text_input("API KEY",value="sk-cT8DO1ZgwLR9THAyuON3T3BlbkFJ7hcKzyDlXOQ1OAUWA5")

def malayalam_to_english(buffer_audio, language):
    r = sr.Recognizer()
    audio_file = io.BytesIO(buffer_audio)
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=language)
    translator = Translator()
    english_text = translator.translate(text)
    return text, english_text

lan_indentifier = {"English(Indian)":"en-IN", "Malayalam":"ml-IN", "English(British)":"en-GB", "Hindi":"hi-IN", "Kannada":"kn-IN"}

wav_audio_data = audio_recorder()
to = st.radio('Pick one', ['Team', 'a Contractor', "Boss", "Junior"])
mode = st.radio('Pick one', ['saying', 'informing', "ordering", "enquiring"])
lan = st.selectbox('Pick one', ['English(Indian)', 'Malayalam', "English(British)", "Hindi", "Kannada"])


if wav_audio_data:
    st.audio(wav_audio_data, format="audio/wav")
    malyalam_text, english_text = malayalam_to_english(wav_audio_data, lan_indentifier[lan])
    st.write("Transcripted Audio: ", malyalam_text)
    st.write("Translated Audio: ", english_text.text)
    updated = st.text_input("EDIT The text",value=english_text.text)

    if st.button("Genarate"):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"the mail is wrriten by an employee of a huge dairy company called as Almarai to his {to}, write a formal mail {mode}, that\n\n{updated}",
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        st.text(response["choices"][0]["text"])
        print(response)
        genrate = False
