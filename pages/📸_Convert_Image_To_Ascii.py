import sys
sys.path.append("C:\\code\\data-analysis-llm\\data-analysis-llm")

import cv2
import numpy as np
import streamlit as st
from src.utils import convert_image_to_color_ascii, convert_image_to_ascii


def main():
    st.set_page_config(page_title="📸 Convert Image To Ascii", layout="centered")
    st.title("📸 Convert Image To Ascii")

    uploaded_image = st.file_uploader("Upload your image here!", type=['png', 'jpg'])

    if uploaded_image:
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        tab1, tab2, tab3 = st.tabs(["Original", "Black & White", "Color"])
        with st.spinner():
            with tab1:
                st.image(uploaded_image)
            with tab2:
                img = cv2.imdecode(file_bytes, 0)
                ascii_image  = convert_image_to_ascii(img)
                st.image(ascii_image)
            with tab3:
                img = cv2.imdecode(file_bytes, 1)
                color_ascii_image = convert_image_to_color_ascii(img)
                st.image(color_ascii_image)


if __name__ == "__main__":
    main()