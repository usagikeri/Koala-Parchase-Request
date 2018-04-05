# coding:utf-8

import json
from get_info import Getinfo


class Koala_info(Getinfo):
    def Koala_parse(self, info_json):
        info_dict = {}
        json_dict = json.loads(info_json)
        try:
            Info = json_dict['items'][0]['volumeInfo']
        except KeyError:
            return None

        if "title" in Info:
            info_dict["title"] = Info["title"]
        else:
            info_dict["title"] = ""

        if "authors" in Info:
            info_dict["author"] = Info["authors"][0]
        else:
            info_dict["author"] = ""

        if "industryIdentifiers" in Info:
            info_dict["ISBN"] = Info["industryIdentifiers"][0]['identifier']
        else:
            info_dict["ISBN"] = ""

        if "publisher" in Info:
            info_dict["publisher"] = Info["publisher"]
        else:
            info_dict["publisher"] = ""

        return info_dict

    def Koala_search(self, ISBN13):
        ISBN13 = str(ISBN13).replace("-","")
        book_data = super().getBookInfo(ISBN13)
        book_list = self.Koala_parse(book_data)

        return book_list


if __name__ == "__main__":
    k = Koala_info()
    print(k.Koala_search("978-4822284763"))
