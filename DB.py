import sqlite3
import datetime
import tkinter as tk


class transactions:
    
    def create_table(self):
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Income(
            
           id INTEGER PRIMARY KEY,
           from_where text NOT NULL,
           category text NO NULL,
           Amount real NOT NULL,
           date INTEGER NOT NULL,
           InEx text NOT NULL,
           comments text 
           
          
            )""")
        conn.commit()
        conn.close
        

   
        

        
        
      
        