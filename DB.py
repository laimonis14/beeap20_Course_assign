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

    def target_table(self):
        
         conn = sqlite3.connect('Users_data.db')
         c = conn.cursor()
         c.execute("""CREATE TABLE IF NOT EXISTS Targets(
           
           Saving INTEGER NOT NULL,
           Spending INTEGER NO NULL,
           Estimated INTEGER NOT NULL,
           Date INTEGER NOT NULL

            )""")
         
         conn.commit()
         conn.close()
         
    def insert_target_table(self, sav_val, spen_val, estim_val):
        
         date = datetime.now()
         date_val = date.strftime('%Y-%m-%d')              
         conn = sqlite3.connect('Users_data.db')
         c = conn.cursor()
         c.execute('SELECT strftime("%m",date) FROM Targets')
         date_result = c.fetchall()
         print(date_result)
         print(date.strftime('%m'))
         c.execute('SELECT EXISTS (SELECT Date FROM Targets WHERE strftime("%m",date) = ?)',
                   (date.strftime('%m'),))
         val = c.fetchone()[0]
         if val == 1:
                 c.execute('UPDATE Targets SET Saving = ?, Spending = ?, Estimated=?, Date=? WHERE strftime("%m",date) = ?',
                           (sav_val, spen_val, estim_val, date_val, date.strftime('%m'),))
                 
         
         else:
             c.execute('INSERT INTO Targets (Saving, Spending, Estimated, Date) VALUES (?,?,?,?)',
                   (sav_val, spen_val, estim_val, date_val))
            
         conn.commit()
         conn.close()
         
    def data_for_edit_page(self, from_date, to_date):
        
         conn = sqlite3.connect('Users_data.db')
         c = conn.cursor()
         c.execute('SELECT EXISTS (SELECT * FROM Income WHERE date BETWEEN ? and ?)',
                   (from_date, to_date,))
         result = c.fetchone()[0]
         if result == 1:
             c.execute('SELECT * FROM Income WHERE date BETWEEN ? and ?',
                   (from_date, to_date,))
             results = c.fetchall()
         else: 
             return None
        

   
        

        
        
      
        