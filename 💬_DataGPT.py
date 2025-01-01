import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from google.generativeai import upload_file
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent


load_dotenv()

def get_plot(plt_code, df):
    try:
        local_vars = {"plt": plt, "df" : df}
        complied_code = compile(source = plt_code, filename="<string>", mode="exec")
        exec(complied_code, globals(),local_vars)
        return plt.gcf()
    except Exception as e:
        st.error(f"cannot generate plot\n {e}")
        return None

def process_message(agent, message):
    response = agent(message)
    print(response["intermediate_steps"][-1])
    plt_code = response["intermediate_steps"][-1][0].tool_input["query"]

    if "plt" in plt_code:
        st.write(f"**Message**: {message}")
        st.write(f"**Result**: {response["output"]}")
        figure = get_plot(plt_code, st.session_state.df)
        if figure:
            st.pyplot(figure)
        st.write("**Python:**")
        st.code(plt_code)
        st.session_state.history.append((message, f"{response["output"]}\n Python\n```{plt_code}```"))
    else:
        st.write(f"**Message**: {message}")
        st.write(f"**Result**: {response["output"]}")
        st.session_state.history.append((message, response["output"]))

def display_history():
    st.write("### Chat History")
    for m, r in st.session_state.history[::-1]:
        st.write(f"**Message**: {m}")
        st.write(f"**Result**: {r}")
        st.write("---")


def main():
    st.set_page_config(page_title="💬 DataGPT", layout="wide")

    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, max_tokens=1000)

    st.title("💬 DataGPT")
    st.info("Upload your dataset and you can ask anything about it including generating figures and interact with visualization tool.")

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.get("df") is None:
        uploaded_file = st.file_uploader("Upload your data here!", type="csv")
        if uploaded_file:
            st.session_state.df = pd.read_csv(uploaded_file)

    if st.session_state.get("df") is not None:
        st.write("### Your dataset: ", st.session_state.df.head(10))

        agent = create_pandas_dataframe_agent(
            llm = model,
            df = st.session_state.df,
            allow_dangerous_code = True,
            agent_type = "tool-calling",
            verbose = True,
            return_intermediate_steps= True
        )
        message = st.chat_input("Message DataGPT")
        if message:
            with st.spinner():
                process_message(agent, message)

    if len(st.session_state.history) > 0:
        st.divider()
        display_history()

if __name__ == "__main__":
    main()


