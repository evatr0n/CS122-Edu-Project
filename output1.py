# output1.py, the tkinter window the user input options 1 and 2

import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

from ui_util import VerticalScrolledFrame
import ui_plot
import default_stat_analysis as dsa
import nctq
import basic_regression as br

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


class Output1:
    """
    Constructor for the output window class that takes in a tkinter root object, the return_dict from input_interface's
    call to this class, and the list of outcomes that correspond to the user input
    """
    def __init__(self, master, return_dict, outcomes):
        self.master = master
        self.return_dict = return_dict
        self.states = return_dict.keys()
        self.outcomes = outcomes
        self.screen_width = master.winfo_screenwidth()
        self.screen_height= master.winfo_screenheight()
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= self.screen_height,
            width= self.screen_width
        )
        self.title_frame()
        self.build_miniFrames()
        self.frame.pack()


    def title_frame(self):
        """
        Function that creates frame that holds the header for the window.
        This includes a short description and quit button to destroy the page
        """
        title_frame = tk.Frame(self.frame, bg = "light blue")
        title_frame.pack(anchor="n", fill="x", expand=False)
        text = tk.Text(title_frame, height = 12, bg = "light blue", font=("Helvetica", 13), bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        text.grid(column = 0, row = 0)
        intro = "Here you will see a collection of information returned for each state you wished you consider."
        note1 = "The score represents the percentage at which your given state's educational wellbeing is at relative to the highest in America."
        note2 = "You will also see which policies were most and least effective in your state's overall educational outcomes."
        note3 = "Below will be a series of scatterplots with regression lines, visualizing how that state's best policy correlates with each outcome variable available."
        text.insert(tk.END, intro + "\n"*2 + note1 + "\n"*2 + note2 + "\n"*2 + note3)
        text.configure(state='disabled')
        # Quit button widget
        quitButton = tk.Button(title_frame, text = 'Quit', width = 25, command = self.close_windows)
        quitButton.grid(column = 1, row = 0, sticky="e")
        quit_label = ttk.Label(title_frame, text = "Note: quitting may take awhile if you have many plots").grid(column = 1,  
                row = 1, padx = 35, pady = 25, sticky="ne") 


    def build_miniFrames(self):
        """
        This function calls upon the miniFrame class to create a new frame for each state that the user wants 
        to visualize
        """
        all_states_frame = tk.Frame(self.frame, bg = "blue")
        all_states_frame.pack(anchor="n", fill="x", expand=False)
        for state in self.states:
            new_frame = miniFrame(state, self.return_dict, all_states_frame, self.outcomes)
        # call miniFrame class to build as many of those as there are states

    def close_windows(self):
        self.master.destroy()
    
class miniFrame:
    def __init__(self, state, return_dict, all_states_frame, outcomes):
        """
        Constructor that creates a new miniFrame for each state and calls the functions in this class
        Inputs: state: name of a state
                return_dict: the return from the input_interface that holds information for each state
                            as a dict: {state: [score, best policy, worst policy]}
                all_states_frame: the main frame to put the miniframe in
                outcomes: return from input_interface with list of outcomes user cares about
        """
        self.state_frame = tk.Frame(all_states_frame, bg = "green")
        self.state_frame.pack(anchor="n", fill="x", expand=False)
        self.return_dict = return_dict
        self.state = state
        self.score = return_dict[state][0]
        self.best_policy = return_dict[state][1]
        self.worst_policy = return_dict[state][2]
        self.outcomes = outcomes
        self.info_frame()
        self.plots_frame()


    def info_frame(self):
        """
        Frame that displays the state's score, best and worst policies
        """
        info_frame = tk.Frame(self.state_frame, bg = "green")
        info_frame.pack(anchor="n", fill="x", expand=False)
        state_text = "State: " + self.state
        score_text = "Score:\n\n" + str(self.score) + "%"
        best_pol_text = "The most effective policy for " + self.state + " was:\n\n" + self.best_policy
        least_pol_text = "The least effective policy for " + self.state + " was:\n\n" + self.worst_policy
        state_label = ttk.Label(info_frame, text=state_text, anchor="center", font=("Helvetica", 20), background="light green").grid(column = 0, row = 1, padx = 25, pady = 25, columnspan= 2, sticky="nw")
        score_label = ttk.Label(info_frame, text=score_text, anchor="w", font=("Helvetica", 18), background="light green").grid(column = 0, row = 2, padx = 35, pady = 25)
        best_label = ttk.Label(info_frame, text=best_pol_text, anchor="w", font=("Helvetica", 15), background="light green").grid(column = 2, row = 2, padx = 35, pady = 25)
        worst_label = ttk.Label(info_frame, text=least_pol_text, anchor="w", font=("Helvetica", 15), background="light green").grid(column = 3, row = 2, padx = 35, pady = 45)


    def plots_frame(self):
        """
        Frame that displays the state's scatterplots of its best policy vs each outcome the user said they care about
        """
        plots_frame = tk.Frame(self.state_frame, bg = "light blue")
        plots_frame.pack(anchor="n", fill="x", expand=False)
        canvas = tk.Canvas(plots_frame, width=1300, height=400)
        canvas.grid(column = 0, row = 0)
        sub_canvas_frame = tk.Frame(canvas)

        # Each iteration creates and places a new scatterplot
        for outcome in self.outcomes:
            outcome_series = nces_trends[outcome]
            best_pol_series = avg_nctq[self.best_policy]
            rr_df = br.run_regression(best_pol_series, outcome_series, trend=True)
            fig = plt.Figure(figsize=(5,4), dpi=100)
            ax = ui_plot.scplot(fig, best_pol_series, outcome_series, rr_df)
            fig_canvas = FigureCanvasTkAgg(fig, master=sub_canvas_frame)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(side=tk.LEFT, padx = 20, pady = 20)
            ax.legend(['Each state']) 
            ax.set_xlabel(best_pol_series.name, labelpad=15)
            ax.set_ylabel(outcome_series.name, labelpad=15)
            ax.set_title("{a} vs. {b}".format(a = self.state + "'s Best Policy", b = "Trend Outcome"))
            fig.tight_layout(pad=3.0, w_pad=4.5, h_pad=4.0)

        canvas.create_window(0, 0, window = sub_canvas_frame, anchor = "nw")
        plots_frame.update()

        #Adding horizontal scrollbar to canvas that holds the plots
        plots_scrollbarh = tk.Scrollbar(plots_frame, orient="horizontal")
        plots_scrollbarh.config(command=canvas.xview)
        canvas.config(xscrollcommand=plots_scrollbarh.set)
        canvas.configure(scrollregion=canvas.bbox("all"))
        plots_scrollbarh.grid(column = 0, row = 1, sticky = "NWE")
