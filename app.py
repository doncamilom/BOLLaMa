import os
import gradio as gr
import random
import time
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from bollama import BOAgent, BOTools

os.environ["LANGCHAIN_HANDLER"] = "langchain"

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(temperature=0)
carlos_the_frustrated_chemist = BOAgent(
    tools = BOTools().botools,
    model="gpt-3.5-turbo"
)


with gr.Blocks() as demo:
    with gr.Row():

        with gr.Column():
            gr.Markdown("# This is one example")



        with gr.Column():

            global carlos_the_frustrated_chemist, memory
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            def user(user_message, history):
                return "", history + [[user_message, None]]

            def bot(history):
                bot_message = carlos_the_frustrated_agent.run(msg)
                history[-1][1] = bot_message
                time.sleep(1)
                return history

            msg.submit(
                user,
                [msg, chatbot],
                [msg, chatbot],
                queue=False
            ).then(
                bot, chatbot, chatbot
            )
            clear.click(lambda: None, None, chatbot, queue=False)



demo.launch(
    server_name='0.0.0.0',
    server_port=8090
)
