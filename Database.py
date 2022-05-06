import sqlite3


class MainDataBase():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DataBaseName = "DataGame.db"

    def ConectionToDataBase(self):
        print("connecting...")
        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Players(name text, DateCreation int, win int, lost int)
        """)

        conn.commit()
        conn.close()
        print("database connected!")

    def ShowColumnName(self):
        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute("SELECT name FROM Players")

        record = c.fetchall()
        #print(record)
        conn.commit()
        conn.close()
        return record

    def ShowData(self):

        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute("SELECT * FROM Players")

        record = c.fetchall()
        #print(record)
        conn.commit()
        conn.close()
        return record


    def CreateAccount(self, name, date):

        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute("INSERT INTO Players VALUES (:name, :DateCreation, :win, :lost)",

                  {
                      'name': name,
                      'DateCreation': date,
                      'win': 0,
                      "lost": 0

                  }
                  )
        conn.commit()
        conn.close()

    def UpdateWins(self, name, win):

        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute(f"UPDATE Players SET win={win} WHERE name='{name}'")

        conn.commit()
        conn.close()

    def UpdateLoses(self, name, lost):

        conn = sqlite3.connect(self.DataBaseName)

        c = conn.cursor()

        c.execute(f"UPDATE Players SET lost={lost} WHERE name='{name}'")

        conn.commit()
        conn.close()

"""
miky = MainDataBase()

miky.ConectionToDataBase()
miky.CreateAccount("miky", 55)
miky.ShowColumnName()
"""
