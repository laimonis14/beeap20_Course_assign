import tkinter as tk
from sqlite3 import *

class password():

    def change_password(self):
        global password_screen
        global old_password
        global new_password
        password_screen = tk.Toplevel(self)
        password_screen.title("Change Password")
        password_screen.geometry("400x250")
        
        old_password_label = tk.Label(password_screen, text ='Insert old password')
        old_password_label.grid(row=0, column=0)
        old_password = tk.Entry(password_screen, width=30, show="*")
        old_password.grid(row=0, column=1, padx=20)
        
        new_password_label = tk.Label(password_screen, text ='Insert new password')
        new_password_label.grid(row=1, column=0)
        new_password = tk.Entry(password_screen, width=30, show="*")
        new_password.grid(row=1, column=1, padx=20)
        
        submit_btn = tk.Button(password_screen, text="Submit", 
                               command=self.approve)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
   
    def ch_passw(self):
        
        conn = connect('Users_data.db')
        c = conn.cursor()
        
        
        if len(old_password.get())==0:
            tk.messagebox.showinfo("ERROR", "Insert Old Password")
        # If Password entry box is empty shows message    
        elif len(new_password.get())==0:
            tk.messagebox.showinfo("ERROR", "Insert New Password")
        else:
            password1 = old_password.get()
            with connect("Users_data.db") as db:
                cursor = db.cursor()
            find_user = ('SELECT *, oid FROM users_data WHERE password = ?')    
            cursor.execute(find_user, [(password1)])
            results = cursor.fetchall()
            
            if results:
                for i in results:
                    self.saved_pass()
                    break
                  
            else:
                tk.messagebox.showinfo("ERROR", "Wrong Old Password")

    def saved(self):
        
            conn = connect('Users_data.db')
            c = conn.cursor()
            c.execute('UPDATE users_data SET password = ? WHERE password = ?',
                      (new_password.get(), old_password.get()))
           
            conn.commit()
            conn.close() 
            tk.Label(password_screen, text="Password changed", 
                     fg="black", font=("calibri", 11)).grid(row=3, column=0, columnspan=2)
            old_password.delete(0, tk.END)
            new_password.delete(0, tk.END)
            password_screen.after(1500, password_screen.destroy)