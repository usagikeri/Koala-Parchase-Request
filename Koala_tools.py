from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
from getpass import getpass

class KoalaTools:
    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        self.url = "http://opac.lib.kansai-u.ac.jp/?page_id=13"
        self.driver.get(self.url)
        # driverの初期設定（サイズ，待機時間，ページ読み込み待機時間，wait)
        self.driver.set_window_size(800, 800)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 30)

    def login_kandai(self,kandai_user,kandai_password):

        print("ログインページに移動...")
        # MyLibraryの選択
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'opacSideAsk_54549')))
            self.driver.find_element_by_id("opacSideAsk_54549").click()
        except:
            print("ページの移動に失敗しました")
            self.driver.quit()
        
        # 入力フォーム，ログインボタンの場所の取得
        username = self.driver.find_element_by_name("IDToken1")
        password = self.driver.find_element_by_name("IDToken2")
        login_button = self.driver.find_element_by_name("Login.Submit")
        
        # ログイン情報の入力
        username.send_keys(kandai_user)
        password.send_keys(kandai_password)
        login_button.click()

        try:
            self.wait.until(EC.title_is("関西大学図書館"))
            print("ログイン完了") 
        except:
            print("ログインに失敗しました")
            self.driver.quit()

    def get_loan_period(self,kandai_user,kandai_password):
        self.login_kandai(kandai_user,kandai_password)

        print("貸出情報の取得中")
        
        # MyLibraryの選択
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'opacSideAsk_54549')))
            self.driver.find_element_by_id("opacSideAsk_54549").click()
        except:
            print("ページの移動に失敗しました")
            self.driver.quit()
            sys.exit()

        try:
            # 新規タブで立ち上がるため，タブの移動．
            self.wait.until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to_window(self.driver.window_handles[1])
        except:
            print("タブの移動に失敗しました")
            self.driver.quit()
            sys.exit()

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[1]/form/div/div[3]/div[2]/div/button')))
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[1]/form/div/div[3]/div[2]/div/button").click()
        except:
            print("貸出一覧クリックエラー")
            self.driver.quit()
            sys.exit()

        try:
            self.wait.until(lambda x:self.driver.find_element_by_tag_name("tbody").is_displayed())
            tbody = self.driver.find_element_by_tag_name("tbody")
        except:
            print("tbodyを取得できないエラー")
            self.driver.quit()
            sys.exit()

        tags = self.get_text(tbody,"th")
        if tags:
            print(" ".join(tags))
        else:
            print("タグ検索エラー")
            self.driver.quit()
            sys.exit()

        try:
            books = tbody.find_elements_by_tag_name("tr")
            for i in range(1,len(books)):
                print(" ".join(self.get_text(books[i],"td")))
        except:
            print("タグ検索エラー")
            self.driver.quit()
            sys.exit()

        self.driver.quit()

    def get_text(self,tag_list,tag):
        """
        find.elementsの結果からtextを取り出す
        """
        try:
            info = list(map(lambda x:x.text,tag_list.find_elements_by_tag_name(tag)))
            return info[0],info[3],info[4],info[7]
        except IndexError:
            return None

if __name__ == "__main__":
    k = KoalaTools()
    kandai_name = input("Please input username >>")
    kandai_pass = getpass("Please input Passsword >>")

    k.get_loan_period(kandai_name,kandai_pass)
