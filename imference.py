import requests
from PIL import Image
import google.generativeai as genai
import streamlit as st

# Access API keys from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
HUGGINGFACE_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from image using Hugging Face Inference API
def img2text(image_path):
    # Open the image f
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    # Make request to Hugging Face Inference API
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    
    if response.status_code == 200:
        result = response.json()
        text = result[0]['generated_text']
        print("Image Description:", text)

        prompt = "You are a nutritionist and you are expected to give nutrient values for the following food description: " + text
        response = model.generate_content(prompt)

        print("Full Response:", response)

        try:
            nutrient_values = response.candidates[0].content.parts[0].text
            print("Nutrient Values:", nutrient_values)
            return text, nutrient_values, response
        except AttributeError as e:
            print(f"AttributeError: {e}")
            print("Response Attributes:", dir(response))
            return text, "Error extracting nutrient values", response
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return "Error", response.status_code, response.json()