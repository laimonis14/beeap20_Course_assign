
import tkinter as tk
from tkinter import ttk
from math import *
import time as tm

from datetime import *
from tkcalendar import Calendar
from PIL import Image, ImageTk, ImageDraw 
import requests, base64
from WeatherFile import OpenWeatherMap, OWIconLabel



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
        
        hr = (h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360
        
        self.clock_image(hr,min_,sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)
        
        
    def calendar(self):
        
        
        f1 = tk.Frame(self, width = 250, height = 250)
        f1.place(x=10, y=230)
        
        cal = Calendar(f1, selectmode = "day", 
                       background = "darkblue", foreground = "white")
        
        cal.place(width = 250, height = 250)
        
    def weather(self):
        
        owm = OpenWeatherMap()
        owm.get_city('Vantaa')
        
        temperature = owm.get_main('temp')
        temp_icon = OWIconLabel(self, 
                                weather_icon=owm.get_icon_data(), bg="white")
        temp_icon.place(x=350, y=25)
        
        location = owm.get('name')
        country = owm.get_sys("country")
        
        self.location_lbl = tk.Label(self, 
                                     text="{}, {}".format(location, country), 
                                     font=("Bold", 15), bg="white")
        self.location_lbl.place(x=360, y=10)

        
        self.temp = tk.Label(self,
                             text='{:.1f} °C'.format(temperature),
                             font=("Bold", 15), bg="white")
        self.temp.place(x=410, y=40)

        temp_feel = owm.get_main('feels_like')
        
        desc = owm.get_weather('description')
        
        self.fell_lbl = tk.Label(self, 
                                 text="Feels like: {:.1f} °C. {}".format(temp_feel, 
                                 desc.capitalize()), font=("Bold", 13), bg="white")
        self.fell_lbl.place(x=360, y=70)
        
        
    def Login(self):
        
        
        global username_verify
        global password_verify
        username_verify = tk.StringVar()
        password_verify = tk.StringVar()
        
        Login_button = tk.Button(self, 
                                 text='Login',command=self.login_verify, 
                                 height=3, width=13)
        Login_button.place(x=400, y=350)
        
        Register_button = tk.Button(self, text="Register",
                                    command = self.register, width=13, height=3)
        Register_button.place(x=540, y=350)
        
        self.user_lbl = tk.Label(self, text='Username', bg='white')
        self.user_lbl.place(x=350, y=250)
        self.password_lbl = tk.Label(self, text='Password', bg='white')
        self.password_lbl.place(x=350, y=280)
        
        global box1
        global box2
        box1 = tk.Entry(self, textvariable=username_verify) #username insert box
        box1.place(x=480, y=250)
        
        box2= tk.Entry(self, textvariable=password_verify) #password insert box
        box2.place(x=480, y=280)
        box2.config(show="*")
        
        
    def register(self):
        
        global register_screen
        register_screen = tk.Toplevel(self)
        register_screen.title("Register")
        register_screen.geometry("300x250")
        
        global username
        global password
        global username_entry
        global password_entry
        
        username = tk.StringVar()
        password = tk.StringVar()
        
        tk.Label(register_screen, text="Please enter details below").pack()
        tk.Label(register_screen, text="").pack()
        
        username_lable = tk.Label(register_screen, text="Username * ")
        username_lable.pack()
        username_entry = tk.Entry(register_screen, textvariable=username)
        username_entry.pack()
        
        password_lable = tk.Label(register_screen, text="Password * ")
        password_lable.pack()
        password_entry = tk.Entry(register_screen, textvariable=password, show='*')
        password_entry.pack()
        
        tk.Label(register_screen, text="").pack()
        tk.Button(register_screen, 
                            text="Register", width=10, height=1, 
                            command = self.register_user).pack()
        
    def register_user(self): 
        
        
        username_info = username.get()
        password_info = password.get()
        
        file = open("Data_file.csv", 'a')  #open file
        file.write(username_info+','+password_info)  #write in file
        
        username_entry.delete(0, tk.END)    #deletes entry of username
        password_entry.delete(0, tk.END)    # Same just for password
        
        tk.Label(register_screen, text="Registration Success", 
                 fg="green", font=("calibri", 11)).pack()
      
        file.close
     
        
    def login_verify(self):
        
        
        succes = False
        username1 = username_verify.get()
        password1 = password_verify.get()
        
        box1.delete(0, tk.END)
        box2.delete(0, tk.END) 
        
        file = open('Data_file.csv', 'r')
        
        for i in file:
            a,b = i.split(",")
            b=b.strip()
            
            if (a==username1 and b==password1):
                succes=True
                break
               
        file.close()
        
        if(succes):
            self.login_sucess()
            
        else:
            self.password_not_recognised()
        
    def password_not_recognised(self):
        
        
        global password_not_recog_screen
        password_not_recog_screen = tk.Toplevel(self)
        password_not_recog_screen.title("ERROR")
        password_not_recog_screen.geometry("200x100")
        tk.Label(password_not_recog_screen, 
                 text="Wrong Username or Password ").pack()
        tk.Button(password_not_recog_screen, text="OK", 
                  command=password_not_recog_screen.destroy).pack()   
        
        
    def login_sucess(self):
        
        global login_success_screen
        login_success_screen = tk.Toplevel(self)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        tk.Label(login_success_screen, text="Login Success").pack()
        tk.Button(login_success_screen, text="OK", 
                          command=login_success_screen.destroy).pack()    
        
        #open new window after 1s
        login_success_screen.after(1000, lambda: self.controller.show_frame(PageOne))
        #closes pop up window after 2s
        login_success_screen.after(2000, login_success_screen.destroy)
        if login_success_screen.showinfo('Success', 'Login Success'):
            lambda: self.controller.show_frame(PageOne)
            login_success_screen.destroy()
            
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        
        
app = AmazingButler()
app.mainloop()