from getpass import getpass

from hgtk.exception import NotHangulException
import mysql.connector
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import hgtk
from datetime import date

today = date.today()
"""
mydb = mysql.connector.connect(
        host="localhost",
        user="Max",
        password="max123")
my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE our_users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
"""
"""
mydb = mysql.connector.connect(
        host="localhost",
        user="Max",
        password="max123")
my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE korean_decks")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
"""
mydb = mysql.connector.connect(
        host="localhost",
        user="Max",
        password="max123",
        database="korean_decks")
my_cursor = mydb.cursor()


'''
my_cursor.execute("INSERT INTO decks (deck_id, title, date_created, admin_user_id) VALUES (%s, %s, %s, %s)",
                  (1, "elementary", today, 3))
mydb.commit()
''' 
'''
url = 'https://learning-korean.com/elementary/20210101-10466/'
# Create object page
page = requests.get(url)
print(page)

soup = BeautifulSoup(page.text, 'html.parser')
table1 = soup.find_all("table")


arr = []
for table in table1:
    for row in table.find_all("tr")[1:]:
        arr.append([cell.get_text(strip=True) for cell in row.find_all("td")])

for i in range(len(arr)):
    kor = arr[i][1]
    ends = ""
    for s in range(len(kor)-1):
        try:
            decomposed = hgtk.letter.decompose(kor[s])
            if decomposed[-1]:
                try:
                    nextDecomposed = hgtk.letter.decompose(kor[s+1])
                    ends += decomposed[-1] + nextDecomposed[0]
                except NotHangulException:
                    """ nothing """
        except NotHangulException:
            print(arr[i])
    arr[i].append(ends)


print(arr[998])
print(arr[1444])
print(arr)
print(hgtk.letter.decompose('감'))



for i in range(len(arr)):
    korean = arr[i][1]
    my_cursor.execute("INSERT INTO vocabulary (deck_id, korean, english, endings) VALUES (%s, %s, %s, %s)",
                      (1, arr[i][1], arr[i][2], arr[i][3]))


mydb.commit()
'''
