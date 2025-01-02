import sys
sys.path.append("C:\\code\\data-analysis-llm\\data-analysis-llm")
import cv2
import tempfile
import numpy as np
import streamlit as st
from src.utils import convert_video_to_ascii, convert_video_to_color_ascii

def main():
    st.set_page_config(page_title="🎬 Convert GIF To Ascii", layout="centered")
    st.title("🎬 Convert GIF To Ascii")
    uploaded_video = st.file_uploader("Upload your GIF here!", type=['gif'])

    if uploaded_video:
        # create temp file to store uploaded video
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        tab1, tab2, tab3 = st.tabs(["Original", "Black & White", "Color"])
        with st.spinner():
            with tab1:
                st.image(uploaded_video)
            with tab2:
                ascii_video  = convert_video_to_ascii(tfile.name)
                st.image(ascii_video)
            with tab3:
                color_ascii_video = convert_video_to_color_ascii(tfile.name)
                st.image(color_ascii_video)


if __name__ == "__main__":
    main()