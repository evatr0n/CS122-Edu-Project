# output1.py

import default_stat_analysis as d 
import tkinter as tk
import pandas as pd
from ui_util import VerticalScrolledFrame
import ui_plot


class Output1:
    def __init__(self, master, return_dict):
        self.master = master
        self.master.attributes("-fullscreen", True)
        self.return_dict = return_dict
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= 1000,
            width= 1000
        )
        self.show_states()
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(column = 1, row = 3)
        self.frame.pack()
    
    def show_states(self):
        state_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        state_text.grid(column = 1, row = 0)
        state_text.insert(tk.END, " ".join(self.return_dict.keys()))
        state_text.configure(state='disabled')

    def close_windows(self):
        self.master.destroy()