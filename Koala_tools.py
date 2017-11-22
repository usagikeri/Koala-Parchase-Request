from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        # 購入依頼の選択してログインページに飛ぶ．
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'opacSideODR_54549')))
            self.driver.find_element_by_id("opacSideODR_54549").click()
        except:
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

