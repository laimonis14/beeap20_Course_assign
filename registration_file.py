import tkinter as tk
import sqlite3

class registers:
    
           
     def register(self):
         
        global register_screen
        register_screen = tk.Toplevel(self)
        register_screen.title("Register")
        register_screen.geometry("400x250")
        
        # connect to database
        conn = sqlite3.connect('Users_data.db')
        
        # Create a cursor
        c = conn.cursor()
        
        
        #Create a Table
        c.execute("""CREATE TABLE IF NOT EXISTS users_data (
        user_name text NOT NULL,
        first_name text NOT NULL,
        password text NOT NULL,
        city text NOT NULL,
        zipcode text NOT NULL
        ) """)
        
        
        global user_name
        global first_name
        global password
        global city
        global zipcode
        
        # Create Text boxes
        user_name = tk.Entry(register_screen, width=30)
        user_name.grid(row=0, column=1, padx=20)
        first_name = tk.Entry(register_screen, width=30)
        first_name.grid(row=1, column=1, padx=20)
        password = tk.Entry(register_screen, width=30, show="*")
        password.grid(row=2, column=1, padx=20)
        city = tk.Entry(register_screen, width=30)
        city.grid(row=3, column=1, padx=20)
        zipcode = tk.Entry(register_screen, width=30)
        zipcode.grid(row=4, column=1, padx=20) 
        
        #Create Text box Labels
        
        user_name_label = tk.Label(register_screen, text ='Username')
        user_name_label.grid(row=0, column=0)
        first_name_label = tk.Label(register_screen, text ='First Name')
        first_name_label.grid(row=1, column=0)
        password_label = tk.Label(register_screen, text ='Password')
        password_label.grid(row=2, column=0)
        city_label = tk.Label(register_screen, text ='City')
        city_label.grid(row=3, column=0)
        zipcode_label = tk.Label(register_screen, text ='Zipcode')
        zipcode_label.grid(row=4, column=0)
        
        # Create submit button
        submit_btn = tk.Button(register_screen, text="Add Record to Database", 
                               command=self.register_user)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        
        #Clears text boxes after submit
        user_name.delete(0, tk.END)
        first_name.delete(0, tk.END)
        password.delete(0, tk.END)
        city.delete(0, tk.END)
        zipcode.delete(0, tk.END)
        
     

     def submit(self):
        # If Username entry box is empty shows message
        if len(user_name.get())==0:
            tk.messagebox.showinfo("ERROR", "Username Not Defined")
        # If Password entry box is empty shows message    
        elif len(password.get())==0:
            tk.messagebox.showinfo("ERROR", "Password Not Defined")
            
        else:
            
            conn = sqlite3.connect('Users_data.db')
        
            # Create a cursor
            c = conn.cursor()
            
            #Insert into table
            c.execute("INSERT INTO users_data VALUES (:user_name, :first_name, :password, :city, :zipcode)", 
                      {
                       'user_name': user_name.get(),
                       'first_name': first_name.get(),
                       'password': password.get(),
                       'city': city.get(),
                       'zipcode': zipcode.get()
                       })
            
            
            # commit command
            conn.commit()
        
            #close connection
            conn.close()   
            
            # Label if registration was done
            tk.Label(register_screen, text="Registration Success", 
                     fg="green", font=("calibri", 11)).grid(row=8, column=0, columnspan=2)
        

        