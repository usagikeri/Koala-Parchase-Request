# coding:utf-8

import requests
from bs4 import BeautifulSoup as bs
import re
import urllib.parse
import sys

def koala_serarch(searchWord):
    url = "http://opac.lib.kansai-u.ac.jp/index.php"
    headers = {"Accept":"text/javascript, text/html, application/xml, text/xml, */*",
                     "X-Prototype-Version":"1.5.0",
                     "Origin":"http://opac.lib.kansai-u.ac.jp",
                     "X-Requested-With":"XMLHttpRequest",
                     "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
                     "Content-type":"application/x-www-form-urlencoded; charset=UTF-8",
                     "DNT":"1",
                     "Referer":"http://opac.lib.kansai-u.ac.jp/index.php?action=pages_view_main&active_action=v3search_view_main_init&block_id=52175&tab_num=0&op_param=words%java",
                     "Accept-Encoding":"gzip, deflate",
                     "Accept-Language":"ja,en-US;q=0.8,en;q=0.6"
                    }
    payload = {"_header":"0",
                "action":"v3search_action_main_opac",
                "block_id":"52175",
                "module_id":"61",
                "op_param":"words={0}".format(urllib.parse.quote(searchWord)),
                "page_id":"17134",
                "search_mode":"null",
                "tab_num":"0"
              }

    r = requests.post(url,headers=headers,data=payload)
    INPUT = bs(r.content,"lxml").findAll("input")

    for i in range(len(INPUT)):
        try:
            book_name = re.match("^<input name=\"bibbr\"\stype=\"hidden\"\svalue=\"(.*)?\"",str(INPUT[i])).group(1)
            if book_name != "":
                print(book_name)
        except :
            pass


if __name__ == "__main__":
    args = sys.argv
    word = args[1]
    koala_serarch(word)
