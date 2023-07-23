import pyperclip as pyperclip
import requests

import streamlit as st

# взаимодействие с сервисом Fast API
backend = 'http://fastapi:8000/get_short_url/'


def get_short_url(url):
    response = requests.get(backend, data=url, timeout=20)
    return response.json()['short_url']


st.set_page_config(
    page_title='URL Shortener',
    page_icon='🔐',
    layout='centered',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
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
    # short_url = get_short_url(text)
    short_url = text

    st.info(short_url)
    pyperclip.copy(short_url)
    st.success('Copied to clipboard')
