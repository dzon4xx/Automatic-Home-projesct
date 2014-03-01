import sqlite3
from datetime import datetime

class Client():

    def __init__(self, ):
        self.db = sqlite3.connect('automatic_home', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = db.cursor()

    def update_database(meters_data):

        print metes_data
        #command = 'INSERT INTO energy_consumption(id, time_stamp,  {0})VALUES(?,?,?,?)'.format(name)
                  

        #cursor.execute(command, (name1,phone1, email1, password1))
        