# output1.py

import default_stat_analysis as d 
import tkinter as tk
import pandas as pd
from ui_util import VerticalScrolledFrame
import ui_plot


class Output2:
    def __init__(self, master, states, outcomes):
        self.master = master
        self.states = states
        self.outcomes = outcomes
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= 1000,
            width= 1000
        )
        self.show_states()
        self.show_outcomes()
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(column = 1, row = 3)
        self.frame.pack()
    
    def show_states(self):
        state_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        state_text.grid(column = 1, row = 0)
        state_text.insert(tk.END, " ".join(self.states))
        state_text.configure(state='disabled')

    def show_outcomes(self):
        outcome_text = tk.Text(self.frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        outcome_text.grid(column = 1, row = 1)
        outcome_text.insert(tk.END, " ".join(self.outcomes))
        outcome_text.configure(state='disabled')

    def close_windows(self):
        self.master.destroy()