import requests
import json
import matplotlib.pylab as plt
import matplotlib.image as mpimg
import numpy as np
from lxml import etree


url = 'http://jxgl.wyu.edu.cn/new/login'
url_info = 'http://jxgl.wyu.edu.cn/xjkpxx!xjkpxx.action'

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',

}

# 保持cookie会话
session = requests.Session()

# 获取验证码
def yzm():
    url = "http://jxgl.wyu.edu.cn/yzm"
    response = session.get(url,headers=Headers)
    with open("wyu_login_verifycode.jpg","wb") as f:
        f.write(response.content)

    # 读取和代码处于同一目录下的 wyu_login_verifycode.jpg
    lena = mpimg.imread('wyu_login_verifycode.jpg')
    # 显示图片
    plt.imshow(lena)
    # 不显示坐标轴
    plt.axis('off')
    plt.show()

# 登录教务管理系统
def wyu_login():
    # 输入账号 密码
    account = input("账号:")
    pwd = input("密码:")
    # 输入验证码
    yzm()
    verifycode = input("验证码:")
    # 保存账号 密码 验证码
    Data = {
        'account': account,
        'pwd': pwd,
        'verifycode': verifycode
    }
    html = session.post(url, headers=Headers,data=Data)
    res = json.loads(html.text)
    print(res['message'])

# 获取个人基本信息
def get_info():
    response = session.post(url_info, headers=Headers)
    xmlContent = etree.HTML(response.content)
    sno = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[1]/td[2]/label/text()"))
    name = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[1]/td[4]/label/text()"))
    year = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[1]/td[6]/label/text()"))
    yard = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[2]/td[2]/label/text()"))
    major = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[2]/td[4]/label/text()"))
    # 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    major = major.strip()
    _class = ''.join(xmlContent.xpath("//*[@id='p']/table/tr[3]/td[2]/label/text()"))
    # 输出
    print("学号：%s" % sno)
    print("姓名：%s" % name)
    print("年级：%s" % year)
    print("院系：%s" % yard)
    print("专业：%s" % major)
    print("班级：%s" % _class)

# 其他py import 此py时，下面的函数将不会被调用
if __name__=="__main__":
    wyu_login()
    get_info()
