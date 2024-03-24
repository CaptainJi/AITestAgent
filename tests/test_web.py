from src.agent.web_auto_framework import WebAutoFrameWork


def test_edge():
    web=WebAutoFrameWork()
    web.open('http://www.baidu.com')
    web.find('#kw')
    web.send_keys('极视角')
    web.find('#su')
    web.click()