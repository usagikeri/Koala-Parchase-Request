from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from koala_info import Koala_info
from getpass import getpass

kandai_name = input("Please input username >>")
ldap_pass = getpass("Please input Passsword >>")
isbn13 = input("Please input ISBN13 >>")

print("書籍データ取得中...")

book_dict = Koala_info().Koala_search(isbn13)

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

driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
url = "http://opac.lib.kansai-u.ac.jp/?page_id=13"
driver.get(url)


# driverの初期設定（サイズ，待機時間，ページ読み込み待機時間，wait)
driver.set_window_size(800, 800)
driver.implicitly_wait(10)
driver.set_page_load_timeout(30)
wait = webdriverwait(driver, 30)

# 購入依頼の選択
try:
    wait.until(EC.element_to_be_clickable((By.ID, 'opacSideODR_54549')))
    driver.find_element_by_id("opacSideODR_54549").click()
except:
    driver.quit()

print("ログインページに移動...")

# 入力フォーム，ログインボタンの場所の取得
username = driver.find_element_by_name("IDToken1")
password = driver.find_element_by_name("IDToken2")
login_button = driver.find_element_by_name("Login.Submit")

# ログイン情報の入力
username.send_keys(kandai_name)
password.send_keys(ldap_pass)
login_button.click()

print("ログイン完了")
print("購入依頼ページに移動...")

# 購入依頼の選択
try:
    wait.until(EC.element_to_be_clickable((By.ID, 'opacSideODR_54549')))
    driver.find_element_by_id("opacSideODR_54549").click()
except:
    driver.quit()

# 購入依頼は新規タブで立ち上がるため，タブの移動．
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])


print("書籍データの入力...")
# 本情報の入力
driver.find_element_by_name("bibtr").send_keys(title)  # Title
driver.find_element_by_name("auth").send_keys(author)  # Author
driver.find_element_by_name("bibpb").send_keys(publisher)  # Publisher
driver.find_element_by_name("isbn").send_keys(isbn)  # ISBN10 or ISBN13

# radio buttonの選択．配架希望館を高槻にしている．if文で分ける...予定
driver.find_element_by_class_name("value").find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[4]/td/form[1]/table/tbody/tr[26]/td[2]/div/input[1]").click()

#  受取希望館の選択 （高槻キャンパスに設定）
place = driver.find_element_by_name("hopar")
Select(place).select_by_index(2)

driver.save_screenshot("./Purchase_request_log.png")

print("書籍データの入力完了")

print("""
Title:{0}
Author:{1}
publisher:{2}
ISBN:{3}
配架希望館:高槻キャンパス図書館
予約依頼:はい
受取希望館:高槻キャンパス図書館
""".format(title, author, publisher, isbn))

while True:
    choice = input("以上の内容でよろしいですか．（Yes/No）")
    if choice == "Yes":
        # 申し込みボタンのクリック
        driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[4]/td/form[1]/table/tbody/tr[39]/td/div/div/a").click()

        # 決定ボタンのクリック
        driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/form/table/tbody/tr[13]/td/div/div/a[1]").click()

        print("購入依頼手続きが完了しました")
        driver.quit()
        exit()

    elif choice == "No":
        print("プログラムを終了します")
        driver.quit()
        exit()

    else:
        pass
