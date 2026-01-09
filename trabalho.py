from tkinter import *
from tkinter import ttk
import sqlite3
root = Tk()
root.geometry("800x600")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Game world").grid(column=7, row=7)

root.mainloop()
