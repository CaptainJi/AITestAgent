import os
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.globals import set_debug, set_verbose

set_debug(True)
set_verbose(True)

# 谷歌搜索的Key
os.environ["SERPAPI_API_KEY"] = '2108726363f5df28dc72f46698dcec0a9ec708b0b62de1e6f4569192e09bdba7'


def test_react():
    chat_model = OpenAI(openai_api_base='http://172.16.100.108:20000/v1',openai_api_key='None', model_name='chatglm3-6b', temperature=0.0)
    tools = load_tools(['serpapi', 'llm-math'], llm=chat_model)
    agent = initialize_agent(tools, chat_model, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION)
    agent.run("极视角公司的简介？")