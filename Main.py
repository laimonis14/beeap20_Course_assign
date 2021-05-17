
import tkinter as tk
from tkinter import ttk
import math as mt
import time as tm
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.filedialog import asksaveasfile
import webbrowser
import numpy as np
import csv
import pandas as pd

from datetime import *
from tkcalendar import Calendar, DateEntry
from PIL import Image, ImageTk, ImageDraw
import requests, base64
from WeatherFile import OpenWeatherMap, OWIconLabel
from DB import transactions
from dice import dices


class AmazingButler(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F,geometry in zip((StartPage, PageOne, PageTransactions, PageEdit, Summary, Setup), 
                              ('700x550', '1050x720', '900x600','1050x550','1000x700','1050x500')):
            cont = F.__name__
            frame = F(parent=container, controller=self)
            # store the frame and the geometry for this frame
            self.frames[cont] = (frame, geometry)
            frame.configure(bg='white')

            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame('StartPage')
        self.title("Amazing Butler App")
        #self.geometry("1100x750")
        
        def save():
            files = [('All Files', '*.*'), 
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
            file = asksaveasfile(filetypes = files, defaultextension = files)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Save', command=save)
        filemenu.add_command(label='LogOut', 
                             command=lambda: self.show_frame('StartPage'))
        filemenu.add_command(label='Exit', command=self.destroy)
                
        def OpenUrl():
            url = 'http://www.google.com'
            webbrowser.open_new(url)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='Help', command =OpenUrl)

        tk.Tk.config(self, menu=menubar)

    def show_frame(self, cont):
        
        
        frame, geometry = self.frames[cont]
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lbl = tk.Label(self, bg="white")
        self.lbl.place(x=10, y=10, height=200, width=200)
        transactions.target_table(self)
        transactions.create_table(self)
        self.working()
        self.calendar()
        self.weather()
        self.Login()

    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)
        # For clock image
        bg = Image.open("clock4.png")
        bg = bg.resize((200, 200), Image.ANTIALIAS)
        clock.paste(bg, (100, 100))

        # Hour Line Image
        origin = 200, 200
        draw.line((origin, 200+50*mt.sin(mt.radians(hr)),
                   200-50*mt.cos(mt.radians(hr))), fill="black", width=4)
        # Min Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(min_)),
                   200-80*mt.cos(mt.radians(min_))), fill="black", width=4)
        # Sec Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(sec_)),
                   200-80*mt.cos(mt.radians(sec_))), fill="black", width=1)

        draw.ellipse((195, 195, 210, 210), fill="black")

        clock.save("clock_new.png")

    def working(self):

        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second

        # Formula to convert clock in circle values for analog clock
        hr = (h/12)*360
        min_ = (m/60)*360
        sec_ = (s/60)*360

        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)

    def calendar(self):

        # Make a frame
        f1 = tk.Frame(self, width=250, height=250)
        f1.place(x=10, y=230)

        # Place calendar inside frame
        cal = Calendar(f1, selectmode="day",
                       background="darkblue", foreground="white")

        cal.place(width=250, height=250)

    def weather(self):

        owm = OpenWeatherMap()
        # Define city
        owm.get_city('Vantaa')

        # gets temp value
        temperature = owm.get_main('temp')
        # Find weather icon
        temp_icon = OWIconLabel(self,
                                weather_icon=owm.get_icon_data(), bg="white")
        temp_icon.place(x=350, y=25)

        # Gets location name
        location = owm.get('name')
        # gets country name
        country = owm.get_sys("country")
        # Country and city label
        self.location_lbl = tk.Label(self,
                                     text="{}, {}".format(location, country),
                                     font=("Bold", 15), bg="white")
        self.location_lbl.place(x=360, y=10)

        # Temperature label
        self.temp = tk.Label(self,
                             text='{:.1f} °C'.format(temperature),
                             font=("Bold", 15), bg="white")
        self.temp.place(x=410, y=40)

        # Temperature \'feel like'\ value
        temp_feel = owm.get_main('feels_like')
        # Weather description
        desc = owm.get_weather('description')
        # Temperature \'feel like'\ and Weather description label
        self.fell_lbl = tk.Label(self,
                                 text="Feels like: {:.1f} °C. {}".format(temp_feel,
                                 desc.capitalize()),
                                 font=("Bold", 13), bg="white")
        self.fell_lbl.place(x=360, y=70)

    def Login(self):

        global password_verify
       
        
       

        password_verify = tk.StringVar()
        # Login button
        Login_button = tk.Button(self,
                                 text='Login', command=self.login_verify,
                                 height=3, width=13, fg='white',
                                 bd='5', bg='blue')

        
        
        Login_button.place(x=420, y=350)

        # Password label
        self.password_lbl = tk.Label(self, text='Enter Password', 
                                     bg='white', justify='center')
        self.password_lbl.config(font=("Times New Roman", 12, "bold"))
        self.password_lbl.place(x=420, y=250)

        global box2

        # Password insert box
        box2 = tk.Entry(self, textvariable=password_verify, show="*",
                        borderwidth = 3, width=20, font=20)
        box2.place(x=380, y=280, height=30)

    def login_verify(self):


            # If Password entry box is empty shows message
        if len(box2.get()) == 0:
            tk.messagebox.showinfo("ERROR", "Password Not Defined")

        else:

            password1 = password_verify.get()
            # Open data base
            with sqlite3.connect("Users_data.db") as db:
                cursor = db.cursor()
            # Select variables what need
            find_user = ('SELECT *, oid FROM users_data WHERE password = ?')
            # what values need to search in data base
            cursor.execute(find_user, [(password1)])
            results = cursor.fetchall()

            if results:
                for i in results:
                    box2.delete(0, tk.END)
                    self.login_sucess()
                    break
            else:
                tk.messagebox.showinfo("ERROR", "Wrong Password")

        db.close()

    def login_sucess(self):

        global login_success_screen
        login_success_screen = tk.Toplevel(self)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        tk.Label(login_success_screen, text="Login Success").pack()

        # open new window after 1s
        login_success_screen.after(1000,
                                   lambda: self.controller.show_frame('PageOne'))
        # closes pop up window after 1,5s
        login_success_screen.after(1500, login_success_screen.destroy)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.load_graph()
        self.lbl = tk.Label(self, bg="white")
        self.lbl.place(x=10, y=10, height=200, width=200)
        self.working()
        StartPage.weather(self)
        StartPage.calendar(self)
        self.button()

    def button(self):

        logout = tk.Button(self, text="Logout",
                           fg='white', bd='5', bg='blue',
                           command=lambda: self.controller.show_frame('StartPage'))
        logout.pack()
        logout.place(x=800, y=100, height=60, width=200)

        addtrans = tk.Button(self, text="Add transaction",
                             fg='white', bd='5', bg='blue',
                             command=lambda: self.controller.show_frame('PageTransactions'))
        addtrans.place(x=800, y=200, height=60, width=200)

        editaccount = tk.Button(self, text="Edit account",
                                fg='white', bd='5', bg='blue',
                                command=lambda: self.controller.show_frame('PageEdit'))
        editaccount.place(x=800, y=300, height=60, width=200)

        setup = tk.Button(self, text="Setup", fg='white', bd='5', bg='blue',
                          command=lambda: self.controller.show_frame('Setup'))
        setup.place(x=800, y=400, height=60, width=200)

        Accountsum = tk.Button(self, text="Account summary",
                               fg='white', bd='5', bg='blue',
                               command=lambda: self.controller.show_frame('Summary'))
        Accountsum.place(x=800, y=500, height=60, width=200)

        playlotto = tk.Button(self, text="Play lotto",
                              fg='white', bd='5', bg='blue',
                              command=self.lot)
        playlotto.place(x=800, y=600, height=60, width=200)
        
        refresh = tk.Button(self, text="Refresh",
                              fg='white', bd='5', bg='blue',
                              command=self.load_graph)
        refresh.place(x=650, y=180, height=20, width=50)
        
    def load_graph(self):
        self.graph_val()
        self.main_graph()
        self.get_balance()
        self.in_da_bank()
        

    def lot(self):
        Lotto.roll_dice(self)
    
    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)
        # For clock image
        bg = Image.open("clock4.png")
        bg = bg.resize((200, 200), Image.ANTIALIAS)
        clock.paste(bg, (100, 100))

        # Hour Line Image
        origin = 200, 200
        draw.line((origin, 200+50*mt.sin(mt.radians(hr)),
                   200-50*mt.cos(mt.radians(hr))), fill="black", width=4)
        # Min Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(min_)),
                   200-80*mt.cos(mt.radians(min_))), fill="black", width=4)
        # Sec Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(sec_)),
                   200-80*mt.cos(mt.radians(sec_))), fill="black", width=1)

        draw.ellipse((195, 195, 210, 210), fill="black")

        clock.save("clock_new.png")

    def working(self):

        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second

        # Formula to convert clock in circle values for analog clock
        hr = (h/12)*360
        min_ = (m/60)*360
        sec_ = (s/60)*360

        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)
        
    def main_graph(self):
        
        Main_Canvas = tk.Canvas(self, width=305, height=150)
        Main_Canvas.place(x=280, y=200)
        
        
        f1 = Figure(figsize=(5,5), dpi=100)
        a1 = f1.add_subplot(111)
        a1.plot(sav_val, sav_dates, label='Saving Target')
        a1.plot(spen_val, spen_dates, label='Spending target')
        a1.plot(estim_val, estim_dates, label='Estimated budget')
        a1.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0) 
        a1.set_xticklabels(estim_val, rotation=45, ha='right')
        canvas1 = FigureCanvasTkAgg(f1, Main_Canvas)
       
        canvas1.get_tk_widget().pack()
        
    def in_da_bank(self):
        
        Balance = tk.Label(self, text='Balance: ', 
                           font='Helvetica 15 bold', bg='white')
        Balance.place(x=350, y=150)
        Balance_show = tk.Label(self, text=balance1, font='bold', 
                                bg='white', borderwidth=2, relief="solid", 
                                width = 10)
        Balance_show.place(x=450, y=150)
        
    def get_balance(self):
        global balance1
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        c.execute('SELECT SUM(Amount) FROM Income WHERE InEx = "Income"')
        incomes = c.fetchall()
        
        c.execute('SELECT SUM(Amount) FROM Income WHERE InEx = "Expenses"')  
        expenses = c.fetchall()
        
        a = np.float_(incomes)
        b = np.float_(expenses)
        balance = a-b
        balance1 = str(balance).lstrip('[').rstrip(']')
        
    def graph_val(self):
        global sav_val
        global sav_dates
        global spen_val
        global spen_dates
        global estim_val
        global estim_dates
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        sav_dates = []
        sav_val = []

        c.execute('SELECT Saving, strftime("%m-%Y", Date) FROM Targets ORDER BY Date ASC')
        for row in c.fetchall():
            sav_dates.append(row[0])
            sav_val.append(row[1])

        spen_dates = []
        spen_val = []
        c.execute('SELECT Spending, strftime("%m-%Y", Date) FROM Targets ORDER BY Date ASC')
        for row in c.fetchall():
            spen_dates.append(row[0])
            spen_val.append(row[1])

            
        estim_dates = []
        estim_val = []
        c.execute('SELECT Estimated, strftime("%m-%Y", Date) FROM Targets ORDER BY Date ASC')
        for row in c.fetchall():
            estim_dates.append(row[0])
            estim_val.append(row[1])

 
class PageTransactions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.lbl = tk.Label(self, bg="white", height=200, width=200)
        self.lbl.grid(row=0, column=0, padx=10, pady=10)
        self.controller = controller
       
        
        transactions.create_table(self)
        StartPage.calendar(self)
        
        self.working()
        self.transaction()
        
       

       

        logout = tk.Button(self, text="Logout", fg='white',
                           bd='5', bg='blue',
                           command=lambda: self.controller.show_frame('StartPage'))
        logout.place(x=650, y=60, height=60, width=200)

        confirm_btn = tk.Button(self, text='Add transaction', 
                                fg='white', bd='5', bg='blue',
                                command=self.entry_data
                                )
        confirm_btn.place(x=650, y=140, height=60, width=200)

        return_btn = tk.Button(self, text='Cancel and return',
                               fg='white', bd='5', bg='blue',
                               command=lambda: self.controller.show_frame('PageOne'))
        return_btn.place(x=650, y=220, height=60, width=200,)
     
    
     
    def transaction(self):
        
        
        global entry_verify
        global opts
        global opts1
        global comment_Box
        global date_Box
        global var
        global names
        global names1
        
        
        entry_verify = tk.StringVar()
        entry_verify1 = tk.StringVar()
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM Income")
        
        
        from_where = ['Account', 'Savings', 'Salary', 'Others']
        opts = tk.StringVar()
        opts1 = tk.StringVar()
        

        def to_where(self):
            names1 = ['Account']
            names = ['Rent', 'Savings', 'Travel', 'Groceries', 'Subscriptions', 'Pleasure', 'Gambling', 'Others']

            if opts.get()=='Account':
                to_Box['values'] = names
            else:
                to_Box['values'] = names1

        from_label = tk.Label(self, text="From:", bg='white',
                                  justify='center', font='bold', width=8)
        from_label.place(x=290, y=100)

        from_Box = ttk.Combobox(self, font=14, width=18, textvariable=opts)
        from_Box.place(x=380, y=100, height=30)
        from_Box['values'] = from_where
        from_Box.bind("<<ComboboxSelected>>", to_where)
        
        to_label = tk.Label(self, text="To:", bg='white',
                                  justify='center', font='bold', width=8)
        to_label.place(x=290, y=200)
        
        to_Box = ttk.Combobox(self, font=14, width=18, textvariable=opts1)
        to_Box.place(x=380, y=200, height=30)
        to_Box.bind("<<ComboboxSelected>>")

        amount_label = tk.Label(self, text='Amount:', bg='white',
                                justify='center', font='bold', width=8)
        amount_label.place(x=290, y=300)

        Amount_Box = tk.Entry(self, font=20, bd='2', textvariable=entry_verify)
        Amount_Box.place(x=380, y=300, height=30)

        date_label = tk.Label(self, text='Date:', bg='white',
                              justify='center', font='bold', width=8)
        date_label.place(x=290, y=400)

        date_Box = DateEntry(self, font=14, bd='2', selectmode="day",
                             date_pattern='dd.mm.y')
        date_Box.place(x=380, y=400, height=30)
        
        comment_label = tk.Label(self, text='Comments: ', bg='white',
                              justify='center', font='bold', width=10)
        comment_label.place(x=290, y=500)
        comment_Box = tk.Text(self, font=20, bd='2', width=20)
        comment_Box.place(x=380, y=500, height=50)
        

    def entry_data(self, event=None):
        
        
        val1 = entry_verify.get()
        sel = opts.get()
        sel1 = opts1.get()
        date = date_Box.get_date()
        com = comment_Box.get("1.0",'end-1c')
        
        if sel == 'Account':
            val2 = 'Expenses'
        else:
            val2 = 'Income'
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        
        c.execute('INSERT INTO Income (from_where, category, Amount, date, InEx, comments) VALUES (?,?,?,?,?,?)', 
                  (sel, sel1, val1, date, val2, com))

        
        conn.commit()
        conn.close() 
    
    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)
        # For clock image
        bg = Image.open("clock4.png")
        bg = bg.resize((200, 200), Image.ANTIALIAS)
        clock.paste(bg, (100, 100))

        # Hour Line Image
        origin = 200, 200
        draw.line((origin, 200+50*mt.sin(mt.radians(hr)),
                   200-50*mt.cos(mt.radians(hr))), fill="black", width=4)
        # Min Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(min_)),
                   200-80*mt.cos(mt.radians(min_))), fill="black", width=4)
        # Sec Line Image
        draw.line((origin, 200+80*mt.sin(mt.radians(sec_)),
                   200-80*mt.cos(mt.radians(sec_))), fill="black", width=1)

        draw.ellipse((195, 195, 210, 210), fill="black")

        clock.save("clock_new.png")

    def working(self):
        global hr
        global min_
        global sec_

        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second

        # Formula to convert clock in circle values for analog clock
        hr = (h/12)*360
        min_ = (m/60)*360
        sec_ = (s/60)*360

        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)    


class PageEdit(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.choose_date()
        self.display_data()

        
        logout = tk.Button(self, text="Logout", fg='white',
                           bd='5', bg='blue',
                           command=lambda: self.controller.show_frame('StartPage'))
        logout.place(x=800, y=60, height=60, width=200)

        accept_btn = tk.Button(self, text='Accept changes', 
                                fg='white', bd='5', bg='blue',
                                command=self.save_new_data)
        accept_btn.place(x=800, y=140, height=60, width=200)

        return_btn = tk.Button(self, text='Return',
                               fg='white', bd='5', bg='blue',
                               command=lambda: self.controller.show_frame('PageOne'))
        return_btn.place(x=800, y=220, height=60, width=200,)
        
        refresh_btn = tk.Button(self, text='View/Refresh',
                               fg='white', bd='5', bg='blue',
                               command=self.get_data)
        refresh_btn.place(x=550, y=60, height=60, width=200,)
        
        export_btn = tk.Button(self, text='Export to CSV',
                               fg='white', bd='5', bg='blue',
                               command=self.save_csv)
        export_btn.place(x=550, y=140, height=60, width=200,)
        
    def choose_date(self):
        
        global from_Box
        global to_Box
        
        choose_date = tk.Label(self, text='Choose date: ', bg='white')
        choose_date.place(x=20, y=20)
        
        from_date = tk.Label(self, text='From: ', bg='white')
        from_date.place(x=20, y=60)
        from_Box = DateEntry(self, font=14, width=10, bd='2', selectmode="day",
                             date_pattern='dd.mm.y')
        
        from_Box.place(x=60, y=60, height=20)
        
        to_date = tk.Label(self, text='To: ', bg='white')
        to_date.place(x=20, y=120)
        to_Box = DateEntry(self, font=14, width=10, bd='2', selectmode="day",
                           date_pattern='dd.mm.y')
        to_Box.place(x=60, y=120, height=20)
        
    def display_data(self):
        global select
        global my_tree
        global frame3
        conn = sqlite3.connect('Users_data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        get_column_names = c.execute('SELECT * FROM Income')
        col_name=[i[0] for i in get_column_names.description]
        
        frame3 = tk.Frame(self)       # select of names
        frame3.place(x=20, y=250)
        my_tree = ttk.Treeview(frame3)
        my_tree['columns'] = col_name
        scroll = tk.Scrollbar(frame3, orient=tk.VERTICAL)
        
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y, expand=1)
        conn = sqlite3.connect('Users_data.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        get_column_names = c.execute('SELECT * FROM Income')
        col_name=[i[0] for i in get_column_names.description]

        my_tree = ttk.Treeview(frame3, yscrollcommand=scroll.set)
        my_tree['columns'] = col_name
        scroll.config(command=my_tree.yview)
        #format column'
        my_tree.column('#0', width=0, stretch=tk.NO)
        my_tree.column(col_name[0], width=0, stretch=tk.NO)
        my_tree.column(col_name[1], anchor=tk.W, width=120)
        
        my_tree.column(col_name[2], anchor=tk.W, width=80)
        my_tree.column(col_name[3], anchor=tk.CENTER, width=120)
        my_tree.column(col_name[4], anchor=tk.W, width=120)
        my_tree.column(col_name[5], anchor=tk.W, width=120)
        my_tree.column(col_name[6], anchor=tk.W, width=120)
        
        #cREATE HEADINGS
        my_tree.heading('#0', text='', anchor=tk.W)
        my_tree.heading(col_name[0], text='', anchor=tk.W)
        my_tree.heading(col_name[1], text = 'From', anchor=tk.W)
        
        my_tree.heading(col_name[2], text='To', anchor=tk.CENTER)
        my_tree.heading(col_name[3], text='Amount', anchor=tk.W)
        my_tree.heading(col_name[4], text='Date', anchor=tk.W)
        my_tree.heading(col_name[5], text='Income/Expenses', anchor=tk.W)
        my_tree.heading(col_name[6], text='Comment', anchor=tk.W)
        
        my_tree.pack(side=tk.LEFT,  fill=tk.BOTH, expand=1)
        
        
        my_tree.bind('<Double-1>', self.set_cell_values)
        
        
        
    def get_data(self):
        
        from_date=from_Box.get_date()
        to_date = to_Box.get_date()

        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()

        c.execute('SELECT * FROM Income WHERE date BETWEEN ? and ?',
                   (from_date, to_date,))
        results = c.fetchall()
       
        count = 0
        if my_tree.exists(count)==True:
            my_tree.delete(*my_tree.get_children())
            for record in results:
           
                my_tree.insert('', index='end', iid=count, tex='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
                count += 1
        else:
            for record in results:
           
                my_tree.insert('', index='end', iid=count, tex='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
                count += 1
       
        conn.close()    
        
    def save_csv(self):
        
        
        data = [my_tree.item (item) ['values'] for item in my_tree.get_children ()]
        df = pd.DataFrame (data)
        df.columns = ['Id', 'From', 'To', 'Amount', 'Date', 'Income/Expenses', 'Comment']
        df.to_csv ('data.csv', encoding ='shift-jis', header = True, index = False)
        

            
    def set_cell_values(self, event):

        for item in my_tree.selection():
            item_text = my_tree.item(item, "values")
            column = my_tree.identify_column(event.x)
            row = my_tree.identify_row(event.y)
        cn = int(str(column).replace('#', ''))
        rn = int(str(row).replace('I', ''))
        entryedit = tk.Text(frame3, width=10 + (2 - 1) * 16, height=1)
        entryedit.place(x=16 + (2 - 1) * 130, y=6 + 20)
        
        def saveedit():
            my_tree.set(item, column=column, value=entryedit.get(0.0, "end"))
            entryedit.destroy()
            okb.destroy()
            self.save_new_data()
    
        okb = ttk.Button(frame3, text='OK', width=4, command=saveedit)
        okb.place(x=90 + (2 - 1) * 242, y=6 + 20)
        
    def save_new_data(self):
        
        curItem = my_tree.focus()

        values = my_tree.item(curItem, 'values')
        

        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()

        c.execute('UPDATE Income SET from_where = ?,  category= ?, Amount = ?, Date = ?, InEx = ?, comments = ? WHERE id = ?', 
                  (values[1], values[2], values[3], values[4], values[5], values[6], values[0]))
        
        conn.commit()
        conn.close()


class Summary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller 
        self.show_values()

        logout = tk.Button(self, text="Logout", fg='white',
                           bd='5', bg='blue',
                           command=lambda: self.controller.show_frame('StartPage'))
        logout.place(x=650, y=60, height=60, width=200)
        
        return_btn = tk.Button(self, text='Return',
                               fg='white', bd='5', bg='blue',
                               command=lambda: self.controller.show_frame('PageOne'))
        return_btn.place(x=650, y=240, height=60, width=200,)
        
        refresh_btn = tk.Button(self, text='Refresh',
                               fg='white', bd='5', bg='blue',
                               command=self.show_values)
        refresh_btn.place(x=650, y=150, height=60, width=200,)
        
        
    def show_values(self):
        
        
        global dates_get

        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()

        dates_get = tk.StringVar()

        dates = []

        c.execute('SELECT DISTINCT strftime("%m-%Y", date) FROM Income ORDER BY Date DESC')
        month_year = c.fetchall()
        for row in month_year:
                dates.append(row[0])

        self.month_Box = ttk.Combobox(self, font=14, width=15, textvariable=dates_get, state='readonly')
        self.month_Box.place(x=300, y=50, height=30)
        
        self.month_Box['values'] = dates
        self.month_Box.bind("<<ComboboxSelected>>", self.graph)
            
        month_lbl = tk.Label(self, text='Select Date: ', bg='white', font='bold')
        month_lbl.place(x=170, y=50)

    def graph(self, event=None):
        
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
        
        c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND strftime("%m-%Y",date) = ?',
                  (dates_get.get(),))
        expense = c.fetchall()
        c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Income" AND strftime("%m-%Y",date) = ?',
                  (dates_get.get(),))
        income = c.fetchall()
        c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Savings" AND strftime("%m-%Y",date) = ?',
                 (dates_get.get(),))
        savings = c.fetchall()
        
        Money_in = tk.Label(self, text='Money in', font='bold', bg='white')
        Money_in.place(x=650, y=400)
        Money_in_show = tk.Label(self, text=income, font='bold', bg='white', borderwidth=2, relief="solid", width = 10)
        Money_in_show.place(x=750, y=400)
        
        Spending = tk.Label(self, text='Spending', font='bold', bg='white')
        Spending.place(x=650, y=450)
        Spending_show = tk.Label(self, text=expense, font='bold', bg='white', borderwidth=2, relief="solid", width = 10)
        Spending_show.place(x=750, y=450)
        
        Savings = tk.Label(self, text='Savings', font='bold', bg='white')
        Savings.place(x=650, y=500)
        Savings_show = tk.Label(self, text=savings, font='bold', bg='white', borderwidth=2, relief="solid", width = 10)
        Savings_show.place(x=750, y=500)
        conn.commit()
        conn.close()
        
        to_graph = dates_get.get()
        
      
        values = []
        conn = sqlite3.connect('Users_data.db')
        c = conn.cursor()
       
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Rent" AND strftime("%m-%Y",date) = ?)',
            (to_graph,))
        rent = c.fetchone()[0]
        if rent == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Rent" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
     
        else:
            values.append(rent)
                
        
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Savings" AND strftime("%m-%Y",date) = ?)',
                         (to_graph,))
        savings = c.fetchone()[0]
        if savings == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Savings" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
                    
        else:
            values.append(savings)
                
    
               
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Travel" AND strftime("%m-%Y",date) = ?)',
                        (to_graph,))
        travel = c.fetchone()[0]
        if travel == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Travel" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
        else:
            values.append(travel)
        
                
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Groceries" AND strftime("%m-%Y",date) = ?)',
            (to_graph,))
        groceries = c.fetchone()[0]
        if groceries == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Groceries" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
        else:
            values.append(groceries)
            
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Subscriptions" AND strftime("%m-%Y",date) = ?)',
            (to_graph,))
        Subscriptions = c.fetchone()[0]
        if Subscriptions == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Subscriptions" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
     
        else:
            values.append(Subscriptions)
            
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Pleasure" AND strftime("%m-%Y",date) = ?)',
                         (to_graph,))
        pleasure = c.fetchone()[0]
        if pleasure == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Pleasure" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
        else:
            values.append(pleasure)
            
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Gambling" AND strftime("%m-%Y",date) = ?)',
                         (to_graph,))
        gambling = c.fetchone()[0]
        if gambling == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Gambling" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
        else:
            values.append(gambling)
                
        c.execute('SELECT EXISTS (SELECT Amount FROM Income WHERE InEx = "Expenses" AND category = "Others" AND strftime("%m-%Y",date) = ?)',
                         (to_graph,))
        others = c.fetchone()[0]
        if others == 1:
            c.execute('SELECT SUM (Amount) FROM Income WHERE InEx = "Expenses" AND category = "Others" AND strftime("%m-%Y",date) = ?',
            (to_graph,))
            x = c.fetchall()
            for row in x:
                    values.append(row[0])
        else:
            values.append(others)
        
        y = ["Rent", "Savings", "Travel", "Groceries", 'Subscriptions', 'Pleasure', 'Gambling', "Others"]
       
        First_Canvas = tk.Canvas(self, width=405, height=300)
        First_Canvas.place(x=30, y=100)
        
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.bar(y, values)
        a.set_xticklabels(y, rotation=45, ha='right')
        
        canvas = FigureCanvasTkAgg(f, First_Canvas)
       
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, First_Canvas)
        
        toolbar.config(background='white')
        toolbar._message_label.config(background='white')
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        conn.close()
        
class Lotto():
    def roll_dice(self):
        dices.roll_dice(self)
        

class Setup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.targets()
        self.target_val()

        
        
        logout = tk.Button(self, text="Logout", fg='white',
                           bd='5', bg='blue',
                           command=lambda: self.controller.show_frame('StartPage'))
        logout.place(x=650, y=60, height=60, width=200)
        
        return_btn = tk.Button(self, text='Return',
                               fg='white', bd='5', bg='blue',
                               command=lambda: self.controller.show_frame('PageOne'))
        return_btn.place(x=650, y=240, height=60, width=200,)
        
        accept_btn = tk.Button(self, text='Accept changes',
                               fg='white', bd='5', bg='blue',
                               command=self.get_targets)
        accept_btn.place(x=650, y=150, height=60, width=200,)
        
    def targets(self):
        
        transactions.target_table(self)
        
    def target_val(self):
        global saving_tar
        global spending_tar
        global estim_tar
        saving_tar = tk.IntVar()
        spending_tar = tk.IntVar()
        estim_tar = tk.IntVar()
        
        saving_label = tk.Label(self, text='Saving target', bg='white',
                                justify='right', font='bold')
        saving_label.place(x=40, y=100)
        saving_tar_Box = tk.Entry(self, font=20, bd='2', textvariable=saving_tar)
        saving_tar_Box.place(x=200, y=100, height=30, width=100) 
        
        spending_label = tk.Label(self, text='Spending target', bg='white',
                                justify='right', font='bold')
        spending_label.place(x=40, y=250)
        spending_tar_Box = tk.Entry(self, font=20, bd='2', textvariable=spending_tar)
        spending_tar_Box.place(x=200, y=250, height=30, width=100) 
        
        estim_label = tk.Label(self, text='Monthly \n estimated budget', bg='white',
                                justify='center', font='bold')
        estim_label.place(x=40, y=400)
        estim_tar_Box = tk.Entry(self, font=20, bd='2', textvariable=estim_tar)
        estim_tar_Box.place(x=200, y=400, height=30, width=100) 
        
    def get_targets(self):
        
        sav_val = saving_tar.get()
        spen_val = spending_tar.get() 
        estim_val = estim_tar.get()
        
        transactions.insert_target_table(self, sav_val, spen_val, estim_val)
        self.input_aff()
        
        
    def input_aff(self):
        
        global input_success_screen
        input_success_screen = tk.Toplevel(self)
        input_success_screen.title("Success")
        input_success_screen.geometry("150x100")
        tk.Label(input_success_screen, text="Modification succesfull").pack()

        input_success_screen.after(500, 
                                   lambda: self.controller.show_frame('PageOne'))
        
        input_success_screen.after(1500, input_success_screen.destroy)


app = AmazingButler()
app.mainloop()