import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent


load_dotenv()

# compile plt code to generate plot
def get_plot(code, df):
    try:
        local_vars = {"plt": plt, "df" : df}
        complied_code = compile(source = code, filename="<string>", mode="exec")
        exec(complied_code, globals(),local_vars)
        return plt.gcf()
    except Exception as e:
        st.error(f"cannot generate plot\n {e}")
        return None

# get response from model
def process_message(agent, message):
    # get response from model using agent and message
    response = agent(message)
    print(response)

    # get code in response
    code = response["intermediate_steps"][-1][0].tool_input["query"] if response["intermediate_steps"] else ""

    # generate plot if the code uses plot
    if "plt" in code:
        st.write(f"**Message**: {message}")
        st.write(f"**Result**: {response["output"]}")
        figure = get_plot(code, st.session_state.df)
        if figure:
            st.pyplot(figure)
        st.write("**Python:**")
        st.code(code)

        # store message, response, and python code to session state history
        st.session_state.history.append((message, f"{response["output"]}\n Python\n```{code}"))

    # output response
    else:
        st.write(f"**Message**: {message}")
        st.write(f"**Result**: {response["output"]}")

        # store message, response, and code to session state history
        st.session_state.history.append((message, response["output"]))

# display history in above user's dataset
def display_history():
    st.write("### Chat History")
    for m, r in st.session_state.history:
        st.write(f"**Message**: {m}")
        st.write(f"**Result**: {r}")
        st.write("---")


def main():
    st.set_page_config(page_title="💬 DataGPT", layout="centered")

    # initialize a gpt-4o-mini model
    # temperature : higher = more creative  lower = less creative, we want the answer to be consistent => lower temperature better
    # max_tokens : ~ number of words in message (1000 tokens = 750 words) reduce cost if the message is complicated
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, max_tokens=1000)

    st.title("💬 DataGPT")

    # set history in session state to an empty array
    if "history" not in st.session_state:
        st.session_state.history = []

    # require user to upload dataset before chatting with gpt
    if st.session_state.get("df") is None:
        st.info("Upload your dataset and you can ask anything about it including generating figures and interact with visualization tool.")

        uploaded_file = st.file_uploader("Upload your data here!", type="csv")
        if uploaded_file:
            st.session_state.df = pd.read_csv(uploaded_file)

    if st.session_state.get("df") is not None:
        if len(st.session_state.history) > 0:
            display_history()
            st.divider()

        st.write("### Your dataset: ", st.session_state.df.head(10))

        # create a pandas agent that allows llm to interact with dataframe
        agent = create_pandas_dataframe_agent(
            llm = model,
            df = st.session_state.df,
            allow_dangerous_code = True, # allow compiling outside code
            agent_type = "tool-calling",
            verbose = True,
            return_intermediate_steps= True # return code used to achieve the result
        )

        message = st.chat_input("Message DataGPT")
        if message:
            with st.spinner():
                process_message(agent, message)


if __name__ == "__main__":
    main()


