from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
# from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI

from src.agent.web_auto_framework import WebAutoFrameWork
from src.untils.langchain_debug import langchain_debug

langchain_debug()

# https://smith.langchain.com/hub/hwchase17/react?organizationId=21ed1ddc-867d-59f9-b850-7903509d5c47
# https://smith.langchain.com/hub/captain/react?organizationId=21ed1ddc-867d-59f9-b850-7903509d5c47
prompt = hub.pull("captain/react")

web = WebAutoFrameWork()


@tool
def open(url: str):
    """
    使用浏览器打开指定url，并返回网页内容
    :param url:网址信息
    :return:网页源码
    """
    r = web.open(url)
    return r


@tool
def find(css: str):
    """
    从网页的源代码中分析出要寻找的元素的css定位符，输入网页元素的css定位符，定位到元素，用于执行后续的操作
    :param locator:定位信息
    """
    return web.find(css)


@tool
def click(arg: str = None):
    """
    点击网页元素，需要提前执行find操作定位到对应的网页元素
    :param arg:
    :return:
    """
    return web.click()


@tool
def send_keys(text: str):
    """
    输入文本，需要提前执行find操作定位到对应的网页元素
    :param text:
    :return:
    """
    return web.send_keys(text)


tools = [open, find, click, send_keys]

llm = OpenAI(
        streaming=True,
        verbose=True,
        callbacks=[],
        openai_api_key="EMPTY",
        openai_api_base='http://172.16.100.108:20000/v1',
        model_name='chatglm3-6b',
        temperature=0.0,
        max_tokens=4096
    )
agent = create_react_agent(llm, tools, prompt)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)


def test_open():
    executor.invoke(
        {
            "input": "每次只返回一个action或者tool"
                     ""
                     "打开https://www.baidu.com网页"
                     "在搜索框输入清明节放假安排"
                     "点击'搜索一下'按钮"
                     "返回搜索后的结果"
        }
    )
