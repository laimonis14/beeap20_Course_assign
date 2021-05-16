import tkinter as tk
import random
import sqlite3
from datetime import *

class dices:
    def roll_dice(self):
        global gamble_screen
        
        date = datetime.now()
        
        money_val = 10
        cat_val = 'Gambling'
        dat_value = date.strftime('%Y-%m-%d')
        win_val = 'Income'
        loose_val = 'Expenses'
        
        
        
        
        dice1 = random.randint(1,6)

        dice2 = random.randint(1,6)

        if dice1 == dice2:

          gamble_screen = tk.Toplevel(self)
          gamble_screen.title("Gamble")
          gamble_screen.geometry("150x100")
          tk.Label(gamble_screen, text="Congrats You Won!!!").pack()
          gamble_screen.after(1500, gamble_screen.destroy)
          conn = sqlite3.connect('Users_data.db')
          c = conn.cursor()
          c.execute('INSERT INTO Income (from_where, Amount, category, date, InEx) VALUES(?,?,?,?,?)',
                    (from_where, money_val, cat_val, dat_value, win_val))
          conn.commit()
          conn.close()
        else:

          gamble_screen = tk.Toplevel(self)
          gamble_screen.title("Gamble")
          gamble_screen.geometry("150x100")
          tk.Label(gamble_screen, text="You've Won Nothing").pack()
          gamble_screen.after(1500, gamble_screen.destroy)
          conn = sqlite3.connect('Users_data.db')
          c = conn.cursor()
          c.execute('INSERT INTO Income (from_where, Amount, category, date, InEx) VALUES(?,?,?,?,?)',
                    (from_where, money_val, cat_val, dat_value, loose_val))
          conn.commit()
          conn.close()
