# output1.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
#import matplotlib
from ui_util import VerticalScrolledFrame
#from ui_util import DoubleScrollbarFrame
import ui_plot
import default_stat_analysis as dsa
import nctq
import os
import basic_regression as br
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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

"""
return_dict = {"IL": [50, "Pay Scales (Retaining Effective Teachers Policy)", "Academic Requirements (Early Childhood Preparation Policy)"], 
        "CA": [75, "Pension Flexibility (Retaining Effective Teachers Policy)", "Induction (Retaining Effective Teachers Policy)"],
        "NY": [90, "Pension Flexibility (Retaining Effective Teachers Policy)", "Induction (Retaining Effective Teachers Policy)"]}
outcomes = ['Trend: Average Daily Attendance %', 'Trend: Students Enrolled in Gifted Programs %', 'Trend: Average Base Teacher Salary w/ Bachelors']
#'Trend: Average Base Teacher Salary w/ Masters Constant Dollars', 'Trend: Teacher Percentage of School Staff', 'Trend: Average Freshman Graduation Rate', 'Trend: 4th Grade Reading Scores', 'Trend: 8th Grade Math Scores', 'Trend: 4th Grade Math Scores', 'Trend: Overall Average Teacher Salary', 'Trend: % of Public Schools That Are Charters', 'Trend: Adjusted Cohort Graduation Rate']
"""

class Output1:
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
        # self.frame = DoubleScrollbarFrame(self.master)
        self.title_frame()
        self.build_miniFrames()
        self.frame.pack()
       # self.frame.pack(side="top", fill="both", expand=True)

    def title_frame(self):
        title_frame = tk.Frame(self.frame, bg = "light blue")
        title_frame.pack(anchor="n", fill="x", expand=False)
        text = tk.Text(title_frame, height = 10, bg = "light blue", font=("Helvetica", 14), bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        text.grid(column = 0, row = 0)
        intro = "This is a general description of how the default calc works"
        text.insert(tk.END, intro)
        text.configure(state='disabled')

        quitButton = tk.Button(title_frame, text = 'Quit', width = 25, command = self.close_windows)
        quitButton.grid(column = 1, row = 0, sticky="e")

    def build_miniFrames(self):
        all_states_frame = tk.Frame(self.frame, bg = "blue")
        all_states_frame.pack(anchor="n", fill="x", expand=False)
        for state in self.states:
            new_frame = miniFrame(state, self.return_dict, all_states_frame, self.outcomes)
        # call miniFrame class to build as many of those as there are states

    def close_windows(self):
        self.master.destroy()
    
class miniFrame:
    def __init__(self, state, return_dict, all_states_frame, outcomes):
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
        plots_frame = tk.Frame(self.state_frame, bg = "light blue")
        plots_frame.pack(anchor="n", fill="x", expand=False)
        canvas = tk.Canvas(plots_frame, width=1300, height=400)
        canvas.grid(column = 0, row = 0)
        sub_canvas_frame = tk.Frame(canvas)

        for outcome in self.outcomes:
            outcome_series = nces_trends[outcome]
            best_pol_series = avg_nctq[self.best_policy]
            rr_df = br.run_regression(best_pol_series, outcome_series, trend=True)
            fig = plt.Figure(figsize=(5,4), dpi=100)
            ax = ui_plot.scplot(fig, best_pol_series, outcome_series, rr_df)
            fig_canvas = FigureCanvasTkAgg(fig, master=sub_canvas_frame)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(side=tk.LEFT, padx = 20, pady = 10)
            ax.legend(['State']) 
            ax.set_xlabel(best_pol_series.name, labelpad=15)
            ax.set_ylabel(outcome_series.name, labelpad=15)
            ax.set_title("{a} vs. {b}".format(a = self.state + "'s Best Policy", b = "Trend Outcome"))
            fig.tight_layout(pad=3.0, w_pad=4.5, h_pad=3.0)

        #canvas = FigureCanvasTkAgg(figure, master = plots_frame)
        #canvas.get_tk_widget().pack(side=tk.LEFT, padx = 20, pady = 10)

        canvas.create_window(0, 0, window = sub_canvas_frame, anchor = "nw")
        plots_frame.update()
        #Adding horizontal scrollbar to policies listbox
        plots_scrollbarh = tk.Scrollbar(plots_frame, orient="horizontal")
        plots_scrollbarh.config(command=canvas.xview)
        canvas.config(xscrollcommand=plots_scrollbarh.set)
        canvas.configure(scrollregion=canvas.bbox("all"))
        plots_scrollbarh.grid(column = 0, row = 1, sticky = "NWE")


"""
# for testing purposes
def main(): #run mianloop 
    master = tk.Tk()
    #getting screen width and height of display 
    screen_width = master.winfo_screenwidth()  #in pixels
    screen_height= master.winfo_screenheight() #in pixels
    #setting tkinter window size 
    master.geometry("%dx%d" % (screen_width, screen_height))
    master.title("Output1")
    app = Output1(master, return_dict, outcomes)
    master.mainloop()

if __name__ == '__main__':
    main()
"""