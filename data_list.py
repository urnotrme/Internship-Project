from tkinter import messagebox, ttk
from tkinter import *
import random, os
import sqlite3

class Match:
    db_name = 'dictionary.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title("Customers' data")
        self.eng, self.trans = str(), str()
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 1, column = 0, columnspan = 2, sticky = W + E)
        self.left = Listbox(height = 12, exportselection=False, activestyle='none')
        self.left.grid(row = 2, column = 0)
        self.right = Listbox(height = 12, activestyle='none')
        self.right.grid(row = 2, column = 1)
        self.right.bind("<<ListboxSelect>>", self.callback_right)
        self.left.bind("<<ListboxSelect>>", self.callback_left)
        ttk.Button(text="Return", command=self.restart_program).grid(row = 4, column = 1, sticky = W + E)
        ttk.Button(text="Edit", command=self.run_edit).grid(row = 4, column = 0, sticky = W + E)
        self.wind.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.get_names()
    def on_exit(self):
        if messagebox.askyesno("Exit", "Close?"):
            self.wind.destroy()
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
 
    def get_names(self):
        query = 'SELECT * FROM dictionary ORDER BY name DESC'
        db_rows = self.run_query(query)
        lst_left, lst_right = [], []
        for row in db_rows:
            lst_left.append(row[1])
            lst_right.append(row[2])
        random.shuffle(lst_left)
        random.shuffle(lst_right)
        dic = dict(zip(lst_left, lst_right))
        for k, v in dic.items():
            self.left.insert(END, k)
            self.right.insert(END, v)
    def callback_left(self, event):
        self.message['text'] = ''
        if not event.widget.curselection():
            return
        w = event.widget
        idx = int(w.curselection()[0])
        self.eng = w.get(idx)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            sqlite_select_query = 'SELECT * from dictionary WHERE name = ?'
            cursor.execute(sqlite_select_query, (self.eng,))
            record = cursor.fetchone()
            self.trans = record[2]
   
    def callback_right(self, event1):
        self.message['text'] = ''
        if not event1.widget.curselection():
            return
        
        w = event1.widget
        idx = int(w.curselection()[0])
        click = w.get(idx)
        if click == self.trans:
            self.right.delete(ANCHOR)
            self.left.delete(ANCHOR)
        else:
            self.message['text'] = 'Неправильно'
            self.right.selection_clear(0, END)
    def run_edit(self):
        os.system('edit_data.py')
    def restart_program(self):
        self.message['text'] = ''
        self.left.delete(0, END)
        self.right.delete(0, END)
        self.get_names()

if __name__ == '__main__':
    window = Tk()
    window.geometry('250x245+350+200')
    application = Match(window)
    window.mainloop()
