from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from koala_info import Koala_info

import sys
from getpass import getpass
import re

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

        self.re_yes = re.compile("Yes|YES|yes|はい")
        self.re_no = re.compile("No|NO|no|いいえ")

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
            sys.exit()

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

         # 新規タブで立ち上がるため，タブの移動．
        try:
            self.wait.until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to_window(self.driver.window_handles[1])
        except:
            print("タブの移動に失敗しました")
            self.driver.quit()
            sys.exit()

        # 貸出一覧のクリック
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


    def purchase_request(self,kandai_user,kandai_password,isbn):
        book_dict = Koala_info().Koala_search(isbn)
        
        if book_dict is None:
            print("書籍データを取得できませんでした．書籍データを入力してください．")
            title = input("Please input Book-titile >>")
            author = input("Please input Book-author >>")
            isbn = input("Please input Book ISBN >>")
            publisher = input("Please input Book-publisher >>")
        else:
            title = book_dict["title"]
            isbn = book_dict["ISBN"]
            author = book_dict["author"]
            publisher = book_dict["publisher"]
        
        print("書籍データ取得完了")
        print("関大図書館ページにアクセス...")

        self.login_kandai(kandai_user,kandai_password)

        # 購入依頼の選択
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, 'opacSideODR_54549')))
            self.driver.find_element_by_id("opacSideODR_54549").click()
        except:
            self.driver.quit()
            sys.exit()

         # 新規タブで立ち上がるため，タブの移動．
        try:
            self.wait.until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to_window(self.driver.window_handles[1])
        except:
            print("タブの移動に失敗しました")
            self.driver.quit()
            sys.exit()

        print("書籍データの入力...")
        # 本情報の入力
        self.driver.find_element_by_name("bibtr").send_keys(title)  # Title
        self.driver.find_element_by_name("auth").send_keys(author)  # Author
        self.driver.find_element_by_name("bibpb").send_keys(publisher)  # Publisher
        self.driver.find_element_by_name("isbn").send_keys(isbn)  # ISBN10 or ISBN13
        
        # radio buttonの選択．配架希望館を高槻にしている．if文で分ける...予定
        while True:
            choice = input("高槻キャンパスで予約しますか（Yes/No）")
            if self.re_yes.fullmatch(choice ) is not None:
                self.driver.find_element_by_class_name("value").find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[4]/td/form[1]/table/tbody/tr[26]/td[2]/div/input[1]").click()
                choice = "はい"

            elif self.re_no.fullmatch(choice) is not None:
                choice = "いいえ"
                break
        
            else:
                print("YesかNoを入力してください")
                pass


        
        #  受取希望館の選択 （高槻キャンパスに設定）
        place = self.driver.find_element_by_name("hopar")
        Select(place).select_by_index(2)
        
        print("書籍データの入力完了")
        
        print("""
        Title:{0}
        Author:{1}
        publisher:{2}
        ISBN:{3}
        配架希望館:高槻キャンパス図書館
        予約依頼:{4}
        受取希望館:高槻キャンパス図書館
        """.format(title, author, publisher, isbn,choice))
        
        while True:
            choice = input("以上の内容でよろしいですか．（Yes/No）")
            if self.re_yes.fullmatch(choice ) is not None:
                # 申し込みボタンのクリック
                self.driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[4]/td/form[1]/table/tbody/tr[39]/td/div/div/a").click()
        
                # 決定ボタンのクリック
                self.driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/form/table/tbody/tr[13]/td/div/div/a[1]").click()
        
                print("購入依頼手続きが完了しました")
                self.driver.quit()
                exit()
        
            elif self.re_no.fullmatch(choice) is not None:
                print("プログラムを終了します")
                self.driver.quit()
                exit()
        
            else:
                pass

if __name__ == "__main__":
    print("class file")
