# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 20:58:29 2021

@author: Laimonis
"""
import tkinter as tk
from tkinter import ttk
from math import *
import time as tm

from PIL import Image, ImageTk, ImageDraw 
from datetime import *



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
        self.geometry("700x400")
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
       

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        
        
        
app = AmazingButler()
app.mainloop()