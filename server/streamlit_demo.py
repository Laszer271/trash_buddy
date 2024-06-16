from time import time
import base64
from io import BytesIO
import re

import streamlit as st
from PIL import Image

from vision import GptVision
from assistant_rag import RAG

import logging
logger = logging.getLogger(__name__)

def _process_answer(answer):
    answer = re.sub('\[\d+\]', '', answer)

    instructions = re.split(r'\d+\.', answer)
    instructions = [s.strip() for s in instructions if s.strip() != '']
    instructions = [f'{i+1}. ' + s for i, s in enumerate(instructions)]
    return instructions

# Define your custom function
def custom_function(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    start_time = time()
    vision = GptVision()
    response = vision.describe_image(img_str)
    print(response)
    logger.info(response)
    print(f"Processing time: {time() - start_time}")
    return _process_answer(response.content)

def main():
    st.title("TrashBuddy")
    st.write("Let's get your trash sorted!")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image to classify...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the image file
        image = Image.open(uploaded_file)
        # resize the image to be at most 524x524 but same aspect ratio
        image.thumbnail((524, 524))

        st.image(image, caption="Uploaded Image.", use_column_width=True)

        # Process the image using the custom function
        result = custom_function(image)

        # Display the results in a text area, each entry on a new line
        result_text = "\n".join(result)
        st.text_area("Instructions", result_text, height=400)

if __name__ == "__main__":
    main()
