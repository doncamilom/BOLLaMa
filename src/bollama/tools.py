from langchain import agents
from .bopt import LLMInterface

class BOTools:
    def __init__(self):
        bofuncs = LLMInterface()

        self.botools = [
            agents.Tool(
                name = "Get initial experiments.",
                func = bofuncs.initialize,
                description = (
                    "Useful to propose initial experiments for a new optimization loop. "\
                    "Takes as input a single integer: the number of experiments that the user wants to perform, "
                    "and returns a list of suggested conditions. "
                    "After this, you have to ask the user to perform this experiments and give you the results."
                )
            ),
            agents.Tool(
                name = "Propose next experiment.",
                func = bofuncs.optimize_step,
                description = (
                    "Useful to propose the next experiment on the optimization loop. "\
                    "Takes as input a dictionary. The keys are eperimental conditions "
                    "(for instance individual molecule smiles), and the values are the corresponding experimental output (a number)"
                    "This outputs a suggested next experiment. "
                )
            ),
            agents.Tool(
                name = "Get user input.",
                func = input,
                description = (
                    "Request anything from the user. "
                    "Useful when you want to get the results from an experiment. "
                    "Ask a specific question."
                    "Ask the user if they want to finish the loop before you do it. "
                )
            )
        ]
