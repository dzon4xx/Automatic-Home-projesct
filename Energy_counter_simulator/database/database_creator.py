import sqlite3
from datetime import datetime

class Db_creator():

    def __init__(self, ):
        pass

    def create_db(self, ):

        db = sqlite3.connect('database/automatic_home', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = db.cursor()
        
        cursor.execute('''
                        CREATE TABLE energy_consumption(id INTEGER PRIMARY KEY, time_stamp DATETIME, 
                                                        CALOSC REAL, KUCHNIA REAL, DOM_LEWY REAL, DOM_PRAWY REAL )  ''')

        db.commit()
        db.close()

db_creator = Db_creator()

db_creator.create_db() 