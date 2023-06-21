import re
import html
from urllib import parse
import requests

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'


def translate(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])


print(translate("Turtlebot入门-创建地图?", "en", "zh-CN"))  # 汉语转英语





# import requests
# from googletrans import Translator
# # 设置Google翻译服务地址
# translator = Translator(service_urls=[
#       'translate.google.cn'
# ])

def ReadFile(filename):
      ff=None
      with open(filename, 'r') as f:
            ff = f.read()
      return ff

def WriteFile(filename,data):
      # 打开一个文件
      fo = open(filename, "w")
      fo.write(data)
      # 关闭打开的文件
      fo.close()


# htmlStr=ReadFile(r"C:\Users\ajz\Desktop\html.txt")
# htmlStr = requests.get('https://www.ncnynl.com/archives/202004/3650.html')
# print(htmlStr.text)
# htmlStr = '你吃饭了吗'
# translation = translator.translate(htmlStr, dest='zh-CN')
# print(translation.text)
# WriteFile(r"/Users/wshuo/Desktop/htmlrlt.html",translation.text)

