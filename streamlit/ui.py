import json

import pyperclip as pyperclip
import requests

import streamlit as st

# взаимодействие с сервисом Fast API
backend = 'http://127.0.0.1:8000/short/'


def get_short_url(url):
    data = {
        'url': url
    }
    response = requests.post(backend, json=data, timeout=20)
    return response


st.set_page_config(
    page_title='URL Shortener',
    page_icon='🔐',
    layout='centered',
    initial_sidebar_state='expanded',
)

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title('URL Shortener', anchor=False)
text = st.text_input('Enter your link', max_chars=100, key=str, help='Enter your link here, max 100 characters.')
if text:
    request = get_short_url(text)
    short_url = request.json()['url']

    st.info(short_url)
    pyperclip.copy(short_url)
    st.success('Copied to clipboard')
