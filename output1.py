# output1.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
#import matplotlib
from ui_util import VerticalScrolledFrame
import ui_plot
import default_stat_analysis as dsa
import nctq
import os

# Import the nces data
nces_final = pd.read_csv("csv/nces_final.csv", index_col=0)
nces_trends = nces_final[[col for col in nces_final.columns if col.startswith("Trend")]]
nces_original = pd.read_csv("csv/nces_raw.csv", index_col=0)

# Import the nctq data
nctqdic_original = {}
for filename in os.listdir("csv/"):
    if filename.startswith("nctq"):
        nctqdic_original[filename.strip(".csv")] = pd.read_csv("csv/{}".format(filename), index_col = 0)
nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg_nctq = nctq.center_df(avg_nctq)

return_dict = {"IL": [50, "Pay Scales (Retaining Effective Teachers Policy)", "	Academic Requirements (Early Childhood Preparation Policy)"], 
        "CA": [75, "Pension Flexibility (Retaining Effective Teachers Policy)", "Induction (Retaining Effective Teachers Policy)"]}

class Output1:
    def __init__(self, master, return_dict):
        self.master = master
        self.master.attributes("-fullscreen", True)
        self.return_dict = return_dict
        self.states = return_dict.keys()
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