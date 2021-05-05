import sqlite3
import datetime
import tkinter as tk


class transactions:
    
    def create_table(self):
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Income(
           
           Amount real NOT NULL,
           category text NOT NULL,
           date text NOT NULL,
           InEx text NOT NULL
           
          
            )""")
        conn.commit()
        conn.close
        

        
        
      
        