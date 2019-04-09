import requests
import re
import config
from bs4 import BeautifulSoup
from PIL import Image

username_, password = config.main()

class login(object):
    def __init__(self):
        self.headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.130 Safari/537.36 OPR/45.0.2257.46",
        }
        self.base_url = "https://www.v2ex.com/"
        self.login_url = "https://www.v2ex.com/signin"
        self.post_url = "https://www.v2ex.com/signin"
        self.session = requests.Session()
        self.part_page_url = "https://www.v2ex.com/recent?p={}"
    
    def basic_info(self):
        response = self.session.get(self.login_url, headers=self.headers)
        html = response.text
        #print(html)查看登录 IP 是否被封锁
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all("input", class_="sl")
        username = items[0]["name"]
        passwd = items[1]["name"]
        captcha = items[2]["name"]

        captcha_url = "https://www.v2ex.com" + str(re.search("background-image: url\(\'(.*?)\'\);", html).group(1))
        #captcha_url = url.replace("=", "\=").replace("?", "\?")
        once_value = captcha_url[-5:]
        return captcha_url, username, passwd, captcha, once_value

    def get_captcha_image(self, captcha_url):
        response = self.session.get(captcha_url, headers=self.headers)
        if response.status_code == 200:
            with open("captcha.jpg", "wb") as f:
                f.write(response.content)
                f.close()
            image = Image.open("captcha.jpg")
            image.show()
        else:
            print(response.status_code, "failed to get captcha pic.")

    def try_login(self, username, passwd, captcha, once_value):
        headers = {
            "User Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "origin": "https://www.v2ex.com",
            "referer": "https://www.v2ex.com/signin",
        }
        post_data = {
            username: username_,
            passwd: password,
            captcha: input("Captcha Code:"),
            "once": once_value,
            "next": "/"
        }
        response = self.session.post(self.post_url, data=post_data, headers=headers, allow_redirects=True)
        response = self.session.get(self.base_url, headers=self.headers)
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        try:
            item = soup.find("a", class_="balance_area").text
            if item:
                print("登录成功")
        except:
            print("登录失败")
        #仅用作查看 cookie，但脚本之间直接传递 session 即可，无需使用 cookie
        #print(response.cookies)
        return self.session

#测试登录是否成功，本次并不需要调用
    def get_pages(self):
        page_url = "https://www.v2ex.com/recent?p=3"
        response = self.session.get(page_url, headers=self.headers)
        print(response.text)

    def run(self):
        captcha_url, username, passwd, captcha, once_value = self.basic_info()
        self.get_captcha_image(captcha_url)
        self.session = self.try_login(username, passwd, captcha, once_value)
        #self.get_pages()测试能否请求更多网页  
        return self.session

if __name__ == "__main__":
    login = login()
    login.run()