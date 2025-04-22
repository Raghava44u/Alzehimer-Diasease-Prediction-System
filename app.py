import base64
import streamlit as st
from config import *
from streamlit_pages._home_page import home_page
from streamlit_pages._predict_alzheimer import prediction_page
from streamlit_pages._team_members import team_members  
# SETTING PAGE CONFIG
st.set_page_config(
    page_title="Alzheimer's Prediction Systems",
    page_icon=":brain:",
)

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

def set_page_background(png_file):
    @st.cache_data()
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            }}
        </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_page_background(BACKGROUND) 

# STREAMLIT APP
st.sidebar.image(SIDE_BANNER)

st.sidebar.markdown('<h1 style="color: orange;">Alzheimer\'s Prediction System</h1>', unsafe_allow_html=True)

app_mode = st.sidebar.selectbox(
    "Please navigate through the different sections of our website from here",
    ["Home", "Predict Alzheimer's", "Team Members"],
)


st.sidebar.markdown("""
<h1 style="color: orange;">Disclaimer</h1>
<p>The predictions provided by this system are for informational purposes only. Consult a healthcare professional for accurate diagnosis and advice.</p>

<h1 style="color: orange;">Contact</h1>
<p>For inquiries, you can mail us <a href="mailto:raghavadasari44@gmail.com">here</a>.</p>
""", unsafe_allow_html=True)



def main():
    if app_mode == "Home":
        home_page()
    if app_mode == "Predict Alzheimer's":
        prediction_page()
    if app_mode=="Team Members":
        team_members()


if __name__ == "__main__":
    main()