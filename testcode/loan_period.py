from Koala_tools import KoalaTools
from getpass import getpass 
k = KoalaTools()

kandai_name = input("Please input username >>")
kandai_pass = getpass("Please input Passsword >>")

k.get_loan_period(kandai_name,kandai_pass)
