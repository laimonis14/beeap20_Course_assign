import sqlite3
import datetime
import tkinter as tk


class transactions:
    
    def create_table(self):
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Income(
           
           Amount real ,
           category text ,
           date textL,
           InEx text  
           
          
            )""")
        conn.commit()
        conn.close
        

        
        
      
        