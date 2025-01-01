import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

def main():
    st.set_page_config(page_title="📈 Interactive Visualization Tool", layout="wide")
    st.header("📈 Interactive Visualization Tool")

    if st.session_state.get("df") is not None:
        StreamlitRenderer(st.session_state.df).explorer()
    else:
        st.info("Please upload your dataset first.")
        uploaded_file = st.file_uploader("Upload your dataset here.", type= "csv")
        if uploaded_file is not None:
            st.session_state.df = pd.read_csv(uploaded_file)
            StreamlitRenderer(st.session_state.df).explorer()

if __name__ == "__main__":
    main()
