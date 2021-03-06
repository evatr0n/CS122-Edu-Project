# utilities for user-interface.py 

import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import Toplevel
import json

class VerticalScrolledFrame:
    """
    Taken from https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8

    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)
# Taken from https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8


class NewWindow(Toplevel):
    '''
    Adapted from https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
    and https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762

    This class was built to allow a new window to open with information uploaded
    from a csv or json present in the new window. It was utilized to allow a 
    user of our program to see the underlying data affecting our outputs.
    '''
    def __init__(self, file, master): 
        '''
        It initializes taking in a file location, which is a string containing
        the directory of the desired file and the name of the master program.
        '''
          
        super().__init__(master) 
        self.title("Underlying Data") 
        self.geometry("1000x500")
        self.file = file 
        self.fill_window() 
    

    # Treeview Widget
    def fill_window(self):
        '''
        Fill window has information on the Treeview object that will fill up our
        Toplevel window. It is made to fill up the whole window, allows a user
        to scroll, and can load in json files and csv files.
        '''
        s = ttk.Style()
        s.configure("Json.Treeview", rowheight = 55)
        if self.file[-4:] == "json":
            tv1 = ttk.Treeview(self, style="Json.Treeview")
        else:
            tv1 = ttk.Treeview(self)
        tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = tk.Scrollbar(self, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
        
        if self.file[-4:] == "json":
            tv1.place(relheight=1, relwidth=1)
            with open(self.file) as f:
                data = json.load(f)
            data1 = list(data.keys())
            data2 = list(data.values())
            df_data = {"Policy Type": data1, "Description of High Quality Policy": data2}
            df = pd.DataFrame(data=df_data)
            tv1["column"] = list(df.columns)
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column) # let the column heading = column name
            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                print(row)
                new_lst = row[1].split()
                if len(new_lst) > 30:
                    new_lst.insert(round(len(new_lst) / 3), "\n")
                    new_lst.insert(round(2 * len(new_lst) / 3), "\n")
                else:
                    new_lst.insert(round(len(new_lst) / 2), "\n")
                row[1] = " ".join(new_lst)
                tv1.insert("", "end", values=row) # inserts each list into the treeview
            
        else:
            df = pd.read_csv(self.file)

            tv1["column"] = list(df.columns)
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column) # let the column heading = column name

            df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
            for row in df_rows:
                tv1.insert("", "end", values=row)
