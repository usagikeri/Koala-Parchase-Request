#coding:utf-8
import urllib.request
import json
import ssl

"""
実行結果 リスト型で返ってくる [ISBN13,title+subtitle,author]
['見えないものをさぐる-それがベイズツールによる実践ベイズ統計', '藤田一弥', '9784274218194']
"""

ssl._create_default_https_context = ssl._create_unverified_context

class Getinfo():
    def __init__(self):
        pass

    def getBookInfo(self,isbn13_str):
        with urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn13_str) as res:
           bookInfo_json = res.read().decode("utf-8")
        return bookInfo_json

    def jsonParse(self,info_json):
        info_lst = []
        json_dict = json.loads(info_json)

        Info = json_dict['items'][0]['volumeInfo']
        subtitle = 'subtitle' in Info

        if subtitle == True:

            info_lst.append(Info["industryIdentifiers"][1]['identifier'])
            info_lst.append(Info["title"]+" "+
                            Info["subtitle"])

        else:
            info_lst.append(Info["industryIdentifiers"][1]['identifier'])
            info_lst.append(Info["title"])

        return info_lst

    def check(self,isbn10_str,isbn13_str):
        """
        ISBN13には978で始まるものと，979で始まるものが存在する。
        そのため，書籍のISBN10とISBN13で検索したGoogleBooksデータのISBN10を比較し，
        書籍が合っているかを確かめている．
        ex) Getinfo().check("4274218198","9784274218194")
        """

        info_json = self.getBookInfo(isbn13_str)
        json_dict = json.loads(info_json)
        isbn10 = json_dict["items"][0]["volumeInfo"]["industryIdentifiers"][0]['identifier']
        if isbn10_str == isbn10:
            print("ok")
        else:
            print("no")

    def search(self, ISBN13):
        bookdata = self.getBookInfo(str(ISBN13))
        book_List = self.jsonParse(bookdata)

        return book_List


if __name__ == "__main__":
    g = Getinfo()
    print(g.getBookInfo("9784822284763")) 
