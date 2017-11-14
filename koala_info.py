# coding:utf-8

import json
from get_info import Getinfo


class Koala_info(Getinfo):
    def Koala_parse(self, info_json):
        info_dict = {}
        json_dict = json.loads(info_json)
        Info = json_dict['items'][0]['volumeInfo']

        if "title" in Info:
            info_dict["title"] = Info["title"]
        else:
            return "Nodata"

        if "industryIdentifiers" in Info:
            info_dict["ISBN"] = Info["industryIdentifiers"][0]['identifier']

        if "authors" in Info:
            info_dict["author"] = Info["authors"][0]

        if "publisher" in Info:
            info_dict["publisher"] = Info["publisher"]

        return info_dict

    def Koala_search(self, ISBN13):
        book_data = super().getBookInfo(str(ISBN13))
        book_list = self.Koala_parse(book_data)

        return book_list


if __name__ == "__main__":
    k = Koala_info()
    print(k.Koala_search("9784822284763"))
