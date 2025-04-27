from llmada import BianXieAdapter
from .prompt import PyEngineer,AiSheller

def edit(task:str,docs:str)->str:
    bianxie = BianXieAdapter()
    bianxie.set_model('gemini-2.0-flash-thinking-exp-1219')
    result = bianxie.chat(messages=[{'role': 'system', 'content': PyEngineer.format(task = task,docs=docs)}])

    return result


def shell(task:str):
    bianxie = BianXieAdapter()
    bianxie.set_model('gemini-2.0-flash-thinking-exp-1219')
    result = bianxie.chat(messages=[{'role': 'system', 'content': AiSheller.format(task = task)}])



