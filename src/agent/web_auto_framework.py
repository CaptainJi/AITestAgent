from selenium import webdriver
from selenium.webdriver.common.by import By


class WebAutoFrameWork:
    """

    """

    def __init__(self):
        self.driver = None
        self.element = None

    def init(self):
        if not self.driver:
            self.driver = webdriver.Edge()
            self.driver.implicitly_wait(10)

    def open(self, url):
        self.init()
        self.driver.get(url)
        return self.source()

    # def source(self):
    #     """
    #     获取网页源码
    #     原有的selenium的page source方法不合适，因为它只返回html的内容，不包括js动态生成的内容
    #     document.body.outerHTML可以获取整个页面的内容，包括js动态生成的内容，但会消耗巨量token
    #     :return:
    #     """
    #     return self.driver.execute_script(
    #         """
    #         var content="";
    #         document.querySelectorAll('button').forEach(x=> content+=x.outerHTML);
    #         document.querySelectorAll('input').forEach(x=> content+=x.outerHTML);
    #         document.querySelectorAll('a').forEach(x=> content+=x.outerHTML);
    #         document.querySelectorAll('table').forEach(x=> content+=x.outerHTML);
    #         return content;
    #         """
    #     )
    def source(self):
        """
        获取网页源码
        原有的selenium的page source方法不合适，因为它只返回html的内容，不包括js动态生成的内容
        document.body.outerHTML可以获取整个页面的内容，包括js动态生成的内容，但会消耗巨量token
        :return:
        """
        return self.driver.execute_script(
            """
            var content="";
            var maxElements = 10;  // 最大获取元素数量
            var maxContentLength = 500;  // 最大获取元素内容长度
            ['button', 'input', 'a', 'table'].forEach(tag => {
                var elements = document.querySelectorAll(tag);
                for (var i = 0; i < Math.min(elements.length, maxElements); i++) {
                    var outerHTML = elements[i].outerHTML;
                    if (outerHTML.length > maxContentLength) {
                        outerHTML = outerHTML.substring(0, maxContentLength) + '...';
                    }
                    content += outerHTML;
                }
            });
            return content;
            """
        )

    def click(self):
        """
        点击当前元素
        :return:
        """
        self.element.click()
        return self.source()

    def send_keys(self, text):
        """
        输入文本
        :param text:
        :return:
        """
        self.element.send_keys(text)
        return self.source()

    def find(self, locator):
        """
        查找元素
        :param locator:
        :return:
        """
        print(f'find css={locator}')
        element = self.driver.find_element(by=By.CSS_SELECTOR, value=locator)
        self.element = element
        return self.element
