import random
from tkinter import *
import sqlite3
import os
from tkinter import ttk
from tkinter import messagebox


upper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

lower = list(map(lambda x: x.lower(), upper))

numbers = ['1','2','3','4','5','6','7','8','9','0']

special = ['@','#','$','%','&','*','_']

All = upper + lower + special + numbers
letter = upper + lower

def create_database():
    if os.path.isfile('Users.db'):
        print ("Database already exists")

    else:
        conn = sqlite3.connect('Users.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS AllUsers(Description TEXT, Password CHAR(20))''')
        conn.close()

def generate():
    Textbox.delete('1.0', END)
    password = ''.join(random.sample(letter,1) + random.sample(All,10))
    Textbox.insert(END,password)

def database(Pass_Text,Desc_Text,Desc,Pass):
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    c.execute("INSERT INTO AllUsers VALUES('{}','{}')".format(Desc,Pass))
    conn.commit()
    conn.close()

def remove_items(table,selection):
    choice = messagebox.askquestion("askquestion", "Are you sure you want to delete selected passwords?")

    if choice == "yes":
        selected_items = selection
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        for selected_item in selected_items:
            cur.execute("DELETE FROM AllUsers WHERE Description = ?", (table.item(selected_item)['values'][0],))

        con.commit()
        con.close()

        for selected_item in selected_items:
            table.delete(selected_item)

    else:
        pass


def view():
    conn = sqlite3.connect("Users.db")
    cursor = conn.execute("SELECT * from AllUsers")
    rows = cursor.fetchall()
    View = Toplevel()
    View.geometry('400x400')
    View.title('View your passwords')
    View.iconbitmap('Images/Icon.ico')
    View.resizable(False,False)
    View.focus_force()
    table = Frame(View)
    table.pack()
    scrollx = Scrollbar(table, orient=HORIZONTAL)
    scrolly = Scrollbar(table, orient=VERTICAL)
    PassTable = ttk.Treeview(table,columns=("Description","Password"), xscrollcommand= scrollx.set, yscrollcommand=scrolly.set)

    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.config(command=PassTable.xview)
    scrolly.config(command=PassTable.yview)

    PassTable.heading("Description", text="Description")
    PassTable.heading("Password", text="Password")

    PassTable["show"] = "headings"

    PassTable.column("Description")
    PassTable.column("Password")

    for row in rows:
        PassTable.insert("", "end", values=row)

    PassTable.pack(fill=BOTH, expand=1, padx=10, pady=10)

    remove_button = Button(View,fg="white",bg="Maroon",text="Remove selected",font=('Goudy',10,'bold'),command=lambda:remove_items(PassTable,PassTable.selection()))
    remove_button.place(relx=0.5,rely=0.8,anchor=CENTER)

    conn.close()

def storage():
    storage = Toplevel()
    storage.geometry('400x400')
    storage.title('Store your passwords')
    storage.iconbitmap('Images/Icon.ico')
    storage.resizable(False,False)
    storage.focus_force()
    Desc = Label(storage,text="Enter Description",fg="Maroon",font=('Goudy',20,'bold'))
    Desc.pack()
    Desc_Text = Text(storage,height=3,width=30)
    Desc_Text.place(relx=0.5,rely=0.2,anchor=CENTER)
    Pass = Label(storage,text="Enter your Password",fg="Maroon",font=('Goudy',20,'bold'))
    Pass.place(relx=0.5,rely=0.4,anchor=CENTER)
    Pass_Text = Entry(storage,show='*',font=('Arial',15))
    Pass_Text.place(relx=0.5,rely=0.5,anchor=CENTER)
    store_button = Button(storage,text="Store in database",fg="white",bg="Maroon",font=('Goudy',15,'bold'),command=lambda:database(Pass_Text,Desc_Text,Desc_Text.get('1.0', 'end'),Pass_Text.get()))
    store_button.place(relx=0.5,rely=0.7,anchor=CENTER)
    view_button = Button(storage,text="View stored passwords",fg='white',bg="Maroon",font=('Goudy',15,'bold'),command=view)
    view_button.place(relx=0.5,rely=0.85,anchor=CENTER)


create_database()
win = Tk()
win.geometry('400x400')
win.title('Random Password Generator')
win.iconbitmap('Images/Icon.ico')
win.resizable(False,False)
header = Label(win,text='Generate a Random Password',fg='Maroon',font=('Impact',20,'bold'))
header.pack()
button = Button(win,text="Click here to generate",fg='white',bg='Maroon',font=('Goudy',15,'bold'),command=generate)
button.place(relx=0.5,rely=0.4,anchor=CENTER)
Textbox = Text(win, height = 1, width = 20)
Textbox.place(relx=0.5,rely=0.6,anchor=CENTER)
button1 = Button(win,text="Storage",fg="white",bg="Maroon",font=('Goudy',15,'bold'),command=storage)
button1.place(relx=0.5,rely=0.8,anchor=CENTER)
win.mainloop()