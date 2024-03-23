from src.agent.web_auto_framework import WebAutoFrameWork


def test_edge():
    web=WebAutoFrameWork()
    web.open('http://www.baidu.com')