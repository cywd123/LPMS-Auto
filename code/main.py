#添加控制台标题 
import os
os.system("title LPMS全自动答题工具")

print("\033[1;45mLPMS全自动答题工具\033[0m")

print("\033[1;30mBy 22级临床 凉拌乌贼酱\033[0m")
print("\033[1;30m2024年11月2日\033[0m")
print("\n")
print("\033[1;31m注意：请勿用于非法用途，否则后果自负\033[0m")
print("\n")
print("链接来自于微信公众号，形式如下：")
print("\033[1;31mhttps://lpms.med.stu.edu.cn/weixin/mpaper.php?action=papersendqrcode&id=XXXX&openid=XXXX\033[0m")
print("\n")
print("-----------------------------")
print("\n")
print("接下来会弹出一个Edge浏览器窗口，请勿关闭并在此窗口中输入链接")


#关闭所有的warning
import warnings
warnings.filterwarnings('ignore')
import rapidfuzz.fuzz as fuzz
#bs4
from bs4 import BeautifulSoup
import orjson as json
import gzip
def t(a):
    return BeautifulSoup(a.replace('&nbsp;',''), 'html.parser').get_text().replace('\n','').replace('\t','').replace('\r','').replace(' ','')
def find(a):
    a=t(a)
    idlist=[]
    anslist=[]
    for i in range(0,len(data)):
        tmp=data[i]['ti']
        score=fuzz.ratio(a,tmp)
        if score>70:
            idlist.append(i)
            anslist.append((score,data[i]['ans']))
    idlist=list(set(idlist))
    anslist=list(set(anslist))
    anslist.sort(reverse=True)
    #print(idlist)
    return anslist

def trans(l):
    #如果l是"A,B,C"这种形式的字符串，那么返回["A","B","C"]
    if l.find(',')!=-1:
        return l.split(',')
    #如果l是"A"这种形式的字符串，那么返回["A"]
    else:
        return [l]
    

from cryptography.fernet import Fernet
key = b'这里是data.db的密钥'######################### 请修改这里
cipher = Fernet(key)
with open("data.db", "rb") as f:
    data = json.loads(gzip.decompress(cipher.decrypt(f.read())).decode())

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os


options = Options()
options.add_argument("--disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 设置Edge WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service,options=options)
driver.minimize_window()
try:
    while(1):
        url=input('请输入链接：')
        driver.get(url)
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/h5')))
            print('已经答过题了')
            continue
        except:
            pass
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="myform"]/div')))
        question_list = driver.find_elements(By.CLASS_NAME, 'row')
        for i  in question_list:
            try:
                question=str(i.text)
                ans1=find(question)[0][1]
                for j in trans(ans1):
                    i.find_element(By.XPATH, './/input[@value="'+j+'"]').click()
            except:
                print("部分题目未能识别，请手动选择")
                pass
        #submit = driver.find_element(By.XPATH, '//*[@id="dosubmit"]')
        #submit.click()
        WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/h5')))
        print('已经答完题了')
finally:
    #driver.quit()
    pass

os.system("pause")
