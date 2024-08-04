import sys
import os
import gradio as gr
import random
import time
from ansi2html import Ansi2HTMLConverter
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from bollama import BOAgent, BOTools

from dotenv import load_dotenv

load_dotenv()


gr.close_all()
custom_css = """
<style>
  .fixed-size-box {
    color: #00ff00 !important;
    width: 100%;
    height: 600px;
    overflow: auto;
    padding: 10px;
  }
</style>
"""

os.environ["LANGCHAIN_HANDLER"] = "langchain"
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def isatty(self):
        return False

sys.stdout = Logger("output.log")



memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

llm = ChatOpenAI(temperature=0)

carlos = BOAgent(
    tools = BOTools().botools,
    memory = memory,
    model = "gpt-4"
)


with gr.Blocks(theme=gr.themes.Soft(primary_hue=gr.themes.colors.green,secondary_hue=gr.themes.colors.green),css=custom_css) as demo:
    with gr.Row():
        with gr.Column():

            gr.Markdown("## This is what the model is thinking 👀")
            def read_logs():

                def convert_ansi_to_html(ansi_text):
                    converter = Ansi2HTMLConverter()
                    html = converter.convert(ansi_text)
                    return html

                # Read the ANSI formatted text from the file
                with open('output.log', 'r') as f:
                    ansi_text = f.read()[102:]

                # Convert ANSI to HTML
                html_text = convert_ansi_to_html(ansi_text)
                sys.stdout.flush()

                wrapped_html_text = custom_css + f'<div class="fixed-size-box">{html_text}</div>'

                return wrapped_html_text

            logs = gr.HTML()
            demo.load(read_logs, None, logs, every=1)



        with gr.Column():

            gr.Markdown(
                "# Welcome to BOLLaMa!🦙😎\n"
                "## Your AI sidekick for sustainable chemical optimization! ♻️🧪🌱"
            )

            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            def user(user_message, history):
                return "", history + [[user_message, None]]

            def bot(history):
                bot_message = carlos.run(history[-1][0])
                history[-1][1] = bot_message
                return history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )
            clear.click(lambda: None, None, chatbot, queue=False)


    with gr.Row():
        gr.Markdown("## Built with [Langchain](https://python.langchain.com/en/latest/modules/llms/getting_started.html) 🦜️🔗️ at [LIAC, EPFL](https://schwallergroup.github.io/).")



demo.queue().launch(
    server_port=5467
)
