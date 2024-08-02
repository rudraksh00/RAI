import streamlit as st 
import os
from PIL import Image
# from imference import img2text

st.title('NutriScan')

uploaded_file = st.file_uploader("Choose an image", type= ['jpg', 'png', 'jpeg'])

if st.button('Generate Nutrient Values') and uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_path = 'temp_img.jpg'
    image.save(image_path)


    description, nutrient_value, full_response = img2text(image_path)

    st.markdown(f'**Image Description**{description}')
    st.markdown(f'**Nutrient Value** {nutrient_value}')
    st.markdown(f'**Full Response**{full_response}')
    st.code(full_response, language='json')

    os.remove(image_path)
else:
    st.warning('Please Upload an Image')