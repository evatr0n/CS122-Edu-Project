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
outcomes = ['Trend: Average Daily Attendance %', 'Trend: Students Enrolled in Gifted Programs %', 'Trend: Average Base Teacher Salary w/ Bachelors', 'Trend: Average Base Teacher Salary w/ Masters Constant Dollars', 'Trend: Teacher Percentage of School Staff', 'Trend: Average Freshman Graduation Rate', 'Trend: 4th Grade Reading Scores', 'Trend: 8th Grade Math Scores', 'Trend: 4th Grade Math Scores', 'Trend: Overall Average Teacher Salary', 'Trend: % of Public Schools That Are Charters', 'Trend: Adjusted Cohort Graduation Rate']

class Output1:
    def __init__(self, master, return_dict, outcomes):
        self.master = master
        self.master.attributes("-fullscreen", True)
        self.return_dict = return_dict
        self.states = return_dict.keys()
        self.outcomes = outcomes
        # self.screen_width = master.winfo_screenwidth()
        # self.screen_height= master.winfo_screenheight()
        self.frame = VerticalScrolledFrame(
            master, 
            bg="white",
            cursor="arrow",
            height= 1000,
            width= 1000
        )
        self.title_frame()
        self.build_miniFrames()
        self.frame.pack()
       # self.frame.pack(side="top", fill="both", expand=True)

    def title_frame(self):
        title_frame = tk.Frame(self.frame, bg = "pink")
        title_frame.pack()
        text = tk.Text(title_frame, height = 5, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
        text.grid(column = 1, row = 0)
        intro = "This is a general description of how the default calc works"
        text.insert(tk.END, intro)
        text.configure(state='disabled')

        quitButton = tk.Button(title_frame, text = 'Quit', width = 25, command = self.close_windows)
        quitButton.grid(column = 2, row = 0)

    def build_miniFrames(self):
        all_states_frame = tk.Frame(self.frame, bg = "blue")
        all_states_frame.pack()
        for state in self.states:
            new_frame = miniFrame(state, return_dict, all_states_frame)
        # call miniFrame class to build as many of those as there are states
        pass

    def close_windows(self):
        self.master.destroy()
    
class miniFrame:
    def __init__(self, state, return_dict, all_states_frame):
        self.state_frame = tk.Frame(all_states_frame, bg = "green")
        self.state_frame.pack(expand=True, fill="x")
        self.return_dict = return_dict
        self.state = state
        self.score = return_dict[state][0]
        self.best_policy = return_dict[state][1]
        self.worst_policy = return_dict[state][2]
        self.info_frame()
        self.plots_frame()

    def info_frame(self):
        state_text = "State: " + self.state
        score_text = "Score: " + str(self.score) + "th percentile"
        best_pol_text = "The Most Effective Policy for " + self.state + " was: " + self.best_policy
        least_pol_text = "The Least Effective Policy for " + self.state + " was: " + self.worst_policy
        state_label = ttk.Label(self.state_frame, text=state_text, anchor=tk.CENTER).grid(column = 0, row = 1, padx = 35, pady = 25, columnspan=2)
        score_label = ttk.Label(self.state_frame, text=score_text, anchor=tk.CENTER).grid(column = 0, row = 2, padx = 35, pady = 25, columnspan=2)
        best_label = ttk.Label(self.state_frame, text=best_pol_text, anchor=tk.CENTER).grid(column = 2, row = 2, padx = 35, pady = 25, columnspan=2)
        worst_label = ttk.Label(self.state_frame, text=least_pol_text, anchor=tk.CENTER).grid(column = 2, row = 3, padx = 35, pady = 25, columnspan=2)
        

    def plots_frame(self):
        pass

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