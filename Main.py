
import tkinter as tk
from tkinter import ttk
from math import *
import time as tm

from datetime import *
from tkcalendar import Calendar
from PIL import Image, ImageTk, ImageDraw 




class AmazingButler(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        frame = StartPage(container, self)
        
        self.frames[StartPage] = frame
        
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
        
        self.lbl = tk.Label(self, bg="white")
        self.lbl.place(x=10, y=10, height=200, width=200)
        
        self.working()
        self.calendar()
        
    def clock_image(self, hr, min_, sec_):
        clock=Image.new("RGB",(400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)
        # For clock image
        bg = Image.open("clock4.png")
        bg=bg.resize((200,200), Image.ANTIALIAS)
        clock.paste(bg, (100, 100))
        
       
        # Hour Line Image
        origin = 200, 200
        draw.line((origin, 200+50*sin(radians(hr)), 200-50*cos(radians(hr))), fill="black", width=4)
        # Min Line Image
        draw.line((origin, 200+80*sin(radians(min_)), 200-80*cos(radians(min_))), fill="black", width=4)
        # Sec Line Image
        draw.line((origin, 200+80*sin(radians(sec_)), 200-80*cos(radians(sec_))), fill="black", width=1)
        
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
        
        
        
app = AmazingButler()
app.mainloop()