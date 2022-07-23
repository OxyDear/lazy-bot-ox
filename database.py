import sqlite3

bd = sqlite3.connect('cows.sqlite')
cur = bd.cursor()

cur.execute('''
CREATE TABLE if not exists poopsiki
(raccoon text, poops integer, time text)
''')
