#!/usr/bin/env python

from Koala_tools import KoalaTools
from koala_search import koala_serarch
from getpass import getpass
import argparse

def input_info():
    kandai_user = input("Please input username >>")
    kandai_pass = getpass("Please input Passsword >>")

    return kandai_user, kandai_pass

def main():
    koala = KoalaTools()
    parser = argparse.ArgumentParser(allow_abbrev=True)

    parser.add_argument("word",
                        help="search word",
                        action="store",
                        nargs=None)

    parser.add_argument("-p",
                        "--purchase_request",
                        help="purchase_request",
                        action="store",
                        nargs="+")

    parser.add_argument("-c",
                        "--check_period",
                        help="check_period",
                        action="store_true")

    arg =  parser.parse_args()

    if arg.purchase_request:
        isbn = arg.purchase_request
        user,password = input_info()
        koala.purchase_request(user,password,isbn)
    elif arg.check_period:
        user,password = input_info()
        koala.get_loan_period(user,password)
    elif arg.word:
        koala_serarch(arg.word)

if __name__ == '__main__':
    main()
