import requests
import json
import getpass
import msvcrt, sys
import matplotlib.pylab as plt
import matplotlib.image as mpimg
from lxml import etree


xq_list = {'1':'星期一','2':'星期二','3':'星期三','4':'星期四','5':'星期五','6':'星期六','7':'星期日'}

url = 'http://jxgl.wyu.edu.cn/new/login'

Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
}

# 保持cookie
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
    account = input("账号：")
    pwd = input("密码：")
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
    print(res['message']+'\n')

# 获取课程表
def get_curriculum(week):
    # 获取周次
    url_curriculum = "http://jxgl.wyu.edu.cn/xsgrkbcx!getKbRq.action?xnxqdm=201902&zc=" + str(week)
    # 开始获取课程表
    html = session.get(url_curriculum,headers=Headers)
    response = json.loads(html.text)[0]
    for res in response:
        # 获取
        xq = str(res['xq'])
        kcmc = str(res['kcmc'])
        jxcdmc = str(res['jxcdmc'])
        jcdm = str(res['jcdm'])
        jcdm2 = str(res['jcdm2'])
        teaxms = str(res['teaxms'])
        # 显示
        print("星期：%s" % xq_list[xq])
        print("课程：%s" % kcmc)
        print("地点：%s" % jxcdmc)
        print("时间：第%s节" % jcdm2)
        print("教师：%s\n" % teaxms)

# 登录教务管理系统
wyu_login()
# 获取课程表
week = input("请输入周次：")
get_curriculum(week)


