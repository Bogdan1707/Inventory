import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):  # функция определения верхней части Тулбар
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add-row-64.png')
        btm_open_dialog = tk.Button(toolbar, text='Додати позицію товару', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btm_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='edit-64.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редагувати позицію', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete-64.png')
        btn_delete = tk.Button(toolbar, text='Видалити позицію', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search-64.png')
        btn_search = tk.Button(toolbar, text='Пошук за найменуванням', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='sinchronize-64.png')
        btn_refresh = tk.Button(toolbar, text='Оновити дані', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.info_item_img = tk.PhotoImage(file='info-64.png')
        btn_info = tk.Button(toolbar, text='Дані про програму', bg='#d7d8e0', bd=0, image=self.info_item_img,
                             compound=tk.TOP, command=self.open_info_dialog)
        btn_info.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, column=('ID', 'item', 'description', 'costs', 'total', 'price'), height=15,
                                 show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('item', width=155, anchor=tk.CENTER)
        self.tree.column('description', width=240, anchor=tk.CENTER)
        self.tree.column('costs', width=90, anchor=tk.CENTER)
        self.tree.column('total', width=80, anchor=tk.CENTER)
        self.tree.column('price', width=105, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('item', text='Артикул')
        self.tree.heading('description', text='Найменування')
        self.tree.heading('costs', text='Вид товару')
        self.tree.heading('total', text='Кількість, шт')
        self.tree.heading('price', text='Ціна одиниці, грн')

        self.tree.pack()

    def records(self, item, description, costs, total, price):
        self.db.insert_data(item, description, costs, total, price)
        self.view_records()

    def update_record(self, item, description, costs, total, price):
        self.db.c.execute('''UPDATE inventory SET item=?, description=?, 
        costs=?, total=?, price=? WHERE ID=?''',
                          (item, description, costs, total, price,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT *FROM inventory''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM inventory WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM inventory 
        WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_search_dialog(self):
        Search()

    def open_dialog(self):  # функция вызова класса Child
        Child()

    def open_update_dialog(self):  # функция вызова класса Update
        Update()

    def open_info_dialog(self):
        Info()


class Child(tk.Toplevel):  # ссылаемся на объект в Топ вверху окна
    def __init__(self):
        super().__init__(root)
        self.init_child()  # вызов функции открытие окна
        self.view = app

    def init_child(self):
        self.title('Додати позицію товару')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_item = tk.Label(self, text='Актикул')
        label_item.place(x=50, y=20)
        label_description = tk.Label(self, text='Найменування')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Вид товару')
        label_select.place(x=50, y=80)
        label_cost = tk.Label(self, text='Кількість, шт')
        label_cost.place(x=50, y=110)
        label_price = tk.Label(self, text='Ціна одиниці, грн')
        label_price.place(x=50, y=140)

        self.entry_item = ttk.Entry(self)
        self.entry_item.place(x=150, y=20, width=225)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=150, y=50, width=225)

        self.combobox = ttk.Combobox(self, values=[u'Апаратне забезпечення', u'Програмне забезпечення'])
        self.combobox.current(0)
        self.combobox.place(x=232, y=80)

        self.entry_cost = ttk.Entry(self)
        self.entry_cost.place(x=232, y=110, width=143)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=232, y=140, width=143)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Додати')
        self.btn_ok.place(x=205, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_item.get(),
                                                                       self.entry_description.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_cost.get(),
                                                                       self.entry_price.get()))

        self.grab_set()  # перехват событий в приложение
        self.focus_set()  # перехват и удержание фокуса в дочернем окне


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.defaulf_data()

    def init_edit(self):
        self.title('Редагувати позицію')
        btn_edit = ttk.Button(self, text='Редагувати')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_item.get(),
                                                                          self.entry_description.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_cost.get(),
                                                                          self.entry_price.get()))

    def defaulf_data(self):
        self.db.c.execute('''SELECT * FROM inventory WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_item.insert(0, row[1])
        self.entry_description.insert(0, row[2])
        if row[3] != 'Апаратне забезпечення':
            self.combobox.current(1)
        self.entry_cost.insert(0, row[4])
        self.entry_price.insert(0, row[5])

        self.btn_ok.destroy()


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Пошук за найменуванням')
        self.geometry('330x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Пошук')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=170)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=205, y=50)

        btn_search = ttk.Button(self, text='Пошук')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS inventory (id integer primary key, item text, 
            description text, costs text, total real, price real)''')
        self.conn.commit()

    def insert_data(self, item, description, costs, total, price):
        self.c.execute('''INSERT INTO inventory(item, description, 
        costs, total, price) VALUES (?, ?, ?, ?, ?)''',
                       (item, description, costs, total, price))
        self.conn.commit()


class Info(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_info()
        self.view = app

    def init_info(self):
        self.title('Дані про програму')
        self.geometry('400x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Додаток підсистеми "Склад". Версія 1.0')
        label_search.place(x=50, y=20)
        label_search = tk.Label(self, text='Розроблений студентом групи ІПЗ - 4.2.03')
        label_search.place(x=50, y=40)
        label_search = tk.Label(self, text='Федоровим Богданом Геннадійовичем')
        label_search.place(x=50, y=60)



if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Склад")
    root.iconbitmap('icon-inv.ico')
    root.geometry("700x450+300+200")
    root.resizable(False, False)
    root.mainloop()
