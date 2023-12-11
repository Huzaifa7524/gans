import streamlit as st
import requests
import json

# Initialize session state
if 'image_aa' not in st.session_state:
    st.session_state.image_aa = []

if 'app' not in st.session_state:
    st.session_state.app = []

# Streamlit app
st.title("Gans Avatar Application")

# URL for the POST requests
base_url = "http://74.235.53.222:8080/finalcombinedimage/"
audio_url = "http://74.235.53.222:8080/postaudiogen/"
video_url = 'http://74.235.53.222:8080/postonlyclick/'

# Function to make POST request
def make_post_request(avatar_image, background_image):
    try:
        data = {
            "avatar_image": avatar_image,
            "background_image": background_image,
        }
        response = requests.post(base_url, data=data)
        img = response.text
        data2 = json.loads(img)
        image_url = data2.get("image_url")
        image_url_aa = data2.get("combined_image")
        st.image(image_url, caption='gans')
        st.session_state.image_aa.append(image_url_aa)
    except requests.RequestException as e:
        st.error(f"Error making POST request: {e}")

def make_post_request_audio(prompt, language, gender):
    try:
        data = {
            "prompt": prompt,
            "language": language,
            "gender": gender
        }
        response = requests.post(audio_url, data=data)
        img = response.text
        data2 = json.loads(img)
        image_url = data2.get("audio_url")
        image_url_aa = data2.get("audio_filename")
        st.header("Generate Audio")
        st.audio(image_url)
        st.session_state.app.append(image_url_aa)
    except requests.RequestException as e:
        st.error(f"Error making POST request: {e}")

def make_post_request_video(combined_image_name, audio_file_name, filename_slug, filename_lang):
    try:
        data = {
            "combined_image_name": combined_image_name,
            "audio_file_name": audio_file_name,
            "filename_slug": filename_slug,
            "filename_lang": filename_lang
        }
        response = requests.post(video_url, data=data)
        img = response.text
        data2 = json.loads(img)
        image_url = data2.get("final_result_video")
        st.header("Generate Video")
        st.video(image_url)
    except requests.RequestException as e:
        st.error(f"Error making POST request: {e}")

# Input fields and button to make POST request
# Dropdowns for avatar and background images
avatar_images = ["man.png", "woman_5.png", "woman_3"]
background_images = ["bg1.png", "bg2.png", "bg4.png",'bg5.png']

avatar_image = st.selectbox("Select Avatar Image", avatar_images)
background_image = st.selectbox("Select Background Image", background_images)
if st.button("Make POST Request Avatar"):
    make_post_request(avatar_image, background_image)

# create a button for POST request
lang = ["English", "Hindi", "Spanish"]
gen = ["Male", "Female"]
prompt = st.text_input("Enter Prompt")
language = st.selectbox("Enter Language", lang)
gender = st.selectbox("Enter Gender", gen)
if st.button("Make Audio"):
    make_post_request_audio(prompt, language, gender)

combined_image_name = st.selectbox("Enter Combined Image Name", st.session_state.image_aa)
audio_file_name = st.selectbox("Enter Audio File Name", st.session_state.app)
filename_slug = st.text_input("Enter Filename Slug")
filename_lang = st.text_input("Enter Filename Language")

if st.button("Make Video"):
    make_post_request_video(combined_image_name, audio_file_name, filename_slug, filename_lang)
