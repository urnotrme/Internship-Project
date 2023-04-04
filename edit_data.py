from tkinter import ttk
from tkinter import *
import sqlite3

class Dictionary:
    db_name = 'dictionary.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Database with customers')

        frame = LabelFrame(self.wind, text = 'Type new customer')
        frame.grid(row = 0, column = 0, columnspan = 2, pady = 20)
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        Label(frame, text = 'VAT identification number: ').grid(row = 2, column = 0)
        self.vat = Entry(frame)
        self.vat.grid(row = 2, column = 1)
        Label(frame, text = 'Date (DD.MM.YYYY): ').grid(row = 3, column = 0)
        self.date = Entry(frame)
        self.date.grid(row = 3, column = 1)
        Label(frame, text = 'Address: ').grid(row = 4, column = 0)
        self.address = Entry(frame)
        self.address.grid(row = 4, column = 1)
        ttk.Button(frame, text = 'Add a customer', command = self.add_customer).grid(row = 5, columnspan = 2, sticky = W + E)
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 5, column = 0, columnspan = 2, sticky = W + E)
        self.tree = ttk.Treeview(height = 10, columns=("#0","#1","#2","#3"))
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name',anchor = CENTER)
        self.tree.heading('#1', text = 'VAT',anchor = CENTER)
        self.tree.heading('#2', text = 'Date',anchor = CENTER)
        self.tree.heading('#3', text = 'Address',anchor = CENTER)

        ttk.Button(text = 'Delete', command = self.delete_customer).grid(row = 7, column = 0, sticky = W + E)
        ttk.Button(text = 'Edit', command = self.edit_customer).grid(row = 7, column = 1, sticky = W + E)

        self.get_customer()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_customer(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM dictionary ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.vat.get() ) != 0 and len(self.date.get() ) != 0 and len(self.address.get() ) != 0
    def add_customer(self):
        if self.validation():
            query = 'INSERT INTO dictionary VALUES(NULL, ?, ?, ?, ?)'
            parameters =  (self.name.get(), self.vat.get(), self.date.get(), self.address.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Customer {} is added to the list'.format(self.name.get())
            self.name.delete(0, END)
            self.vat.delete(0, END)
            self.date.delete(0, END)
            self.address.delete(0, END)
        else:
            self.message['text'] = "Type customer's data"
        self.get_customer()
    def delete_customer(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = ''
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM dictionary WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Customer {} is deleted succesfully'.format(name)
        self.get_customer()
    def edit_customer(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Choose customer to delete from the list'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_vat = self.tree.item(self.tree.selection())['values'][0]
        old_date = self.tree.item(self.tree.selection())['values'][0]
        old_address = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Edit customer's data"

        Label(self.edit_wind, text = 'Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        
        Label(self.edit_wind, text = 'New name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name))
        new_name.grid(row = 1, column = 2)

        Label(self.edit_wind, text = 'VAT:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_vat), state = 'readonly').grid(row = 2, column = 2)
 
        Label(self.edit_wind, text = 'New VAT:').grid(row = 3, column = 1)
        new_vat= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_vat))
        new_vat.grid(row = 3, column = 2)

        Label(self.edit_wind, text = 'Date:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_date), state = 'readonly').grid(row = 4, column = 2)
 
        Label(self.edit_wind, text = 'New date:').grid(row = 5, column = 1)
        new_date= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_date))
        new_date.grid(row = 5, column = 2)

        Label(self.edit_wind, text = 'Address:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_address), state = 'readonly').grid(row = 6, column = 2)
 
        Label(self.edit_wind, text = 'New address:').grid(row = 7, column = 1)
        new_address= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_address))
        new_address.grid(row = 7, column = 2)

        Button(self.edit_wind, text = 'Edit', command = lambda: self.edit_records(new_name.get(), name, new_vat.get(), old_vat, new_date.get(), old_date, new_address.get(), old_address)).grid(row = 8, column = 2, sticky = W)
        self.edit_wind.mainloop()
    def edit_records(self, new_name, name, new_vat, old_vat, new_date, old_date, new_address, old_address):
        query = 'UPDATE dictionary SET name = ?, vat = ?, date = ?, address = ? WHERE name = ? AND vat = ? AND date = ? AND address = ?'
        parameters = (new_name, new_vat, new_date, new_address, name, old_vat, old_date, old_address)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Customer {} is edeted successfully'.format(name)
        self.get_customer()

if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()
