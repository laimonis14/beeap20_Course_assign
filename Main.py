
import tkinter as tk
from tkinter import ttk
from math import *
import time as tm
import sqlite3

from datetime import *
from tkcalendar import Calendar
from PIL import Image, ImageTk, ImageDraw 
import requests, base64
from WeatherFile import OpenWeatherMap, OWIconLabel
from registration_file import registers


class AmazingButler(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne):
        
            frame = F(container, self)
            frame.configure(bg='white')
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
              
               
        self.show_frame(StartPage)
        self.title("Amazing Butler App")
        self.geometry("700x500")
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
       

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lbl = tk.Label(self, bg="white")
        self.lbl.place(x=10, y=10, height=200, width=200)
        
        self.working()
        self.calendar()
        self.weather()
        self.Login()
        
    def clock_image(self, hr, min_, sec_):
        clock=Image.new("RGB",(400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)
        # For clock image
        bg = Image.open("clock4.png")
        bg=bg.resize((200,200), Image.ANTIALIAS)
        clock.paste(bg, (100, 100))
        
       
        # Hour Line Image
        origin = 200, 200
        draw.line((origin, 200+50*sin(radians(hr)), 
                   200-50*cos(radians(hr))), fill="black", width=4)
        # Min Line Image
        draw.line((origin, 200+80*sin(radians(min_)), 
                   200-80*cos(radians(min_))), fill="black", width=4)
        # Sec Line Image
        draw.line((origin, 200+80*sin(radians(sec_)), 
                   200-80*cos(radians(sec_))), fill="black", width=1)
        
        draw.ellipse((195, 195, 210, 210), fill="black")
        
        
        clock.save("clock_new.png")
        
        
    def working(self):
        
        
        h=datetime.now().time().hour
        m=datetime.now().time().minute
        s=datetime.now().time().second
                
        # Formula to convert clock in circle values for analog clock        
        hr = (h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360
        
        self.clock_image(hr,min_,sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)
        
        
    def calendar(self):
        
        # Make a frame
        f1 = tk.Frame(self, width = 250, height = 250)
        f1.place(x=10, y=230)
        
        #Place calendar inside frame
        cal = Calendar(f1, selectmode = "day", 
                       background = "darkblue", foreground = "white")
        
        cal.place(width = 250, height = 250)
        
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
        #gets country name
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
                                 desc.capitalize()), font=("Bold", 13), bg="white")
        self.fell_lbl.place(x=360, y=70)
        
        
    def Login(self):
        
        
        global username_verify
        global password_verify
        
        username_verify = tk.StringVar()
        password_verify = tk.StringVar()
        # Login button
        Login_button = tk.Button(self, 
                                 text='Login',command=self.login_verify, 
                                 height=3, width=13)
        Login_button.place(x=400, y=350)
        # Register button
        Register_button = tk.Button(self, text="Register",
                                    command = self.register, width=13, height=3)
        Register_button.place(x=540, y=350)
        # Username label
        self.user_lbl = tk.Label(self, text='Username', bg='white')
        self.user_lbl.place(x=350, y=250)
        # Password label
        self.password_lbl = tk.Label(self, text='Password', bg='white')
        self.password_lbl.place(x=350, y=280)
        
        global box1
        global box2
        # Username insert box
        box1 = tk.Entry(self, textvariable=username_verify) 
        box1.place(x=480, y=250)
        # Password insert box
        box2= tk.Entry(self, textvariable=password_verify, show="*") 
        box2.place(x=480, y=280)
        
            
    def register(self):
        
        
        registers.register(self)
        
                
    def register_user(self): 
        
        
        registers.submit(self)
               
          
    def login_verify(self):
        
        # If Username entry box is empty shows message
        if len(box1.get())==0:
            tk.messagebox.showinfo("ERROR", "Username Not Defined")
            # If Password entry box is empty shows message    
        elif len(box2.get())==0:
            tk.messagebox.showinfo("ERROR", "Password Not Defined")
                
        else:
            username1 = username_verify.get()
            password1 = password_verify.get()
            
            with sqlite3.connect("Users_data.db") as db:
                cursor = db.cursor()
            find_user = ('SELECT *, oid FROM users_data WHERE user_name = ? AND password = ?')
            cursor.execute(find_user,[(username1),(password1)])
            results = cursor.fetchall()
            
            if results:
                for i in results:
                    self.login_sucess()
                    break
            else:
                tk.messagebox.showinfo("ERROR", "Wrong Username or Password")
        
        box1.delete(0, tk.END)
        box2.delete(0, tk.END) 
        
        db.close()        
        
    def login_sucess(self):
        
        global login_success_screen
        login_success_screen = tk.Toplevel(self)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        tk.Label(login_success_screen, text="Login Success").pack()
            
        
        #open new window after 1s
        login_success_screen.after(1000, lambda: self.controller.show_frame(PageOne))
        #closes pop up window after 2s
        login_success_screen.after(1500, login_success_screen.destroy)
        if login_success_screen.showinfo('Success', 'Login Success'):
            lambda: self.controller.show_frame(PageOne)
            login_success_screen.destroy()
            
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        
        
app = AmazingButler()
app.mainloop()