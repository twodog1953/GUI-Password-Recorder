from tkinter.messagebox import showinfo
from tkinter import *
import sqlite3
from os import path
from datetime import datetime

root = Tk()
root.title('Password Logger')
root.geometry("450x600")

# db table
if path.exists('password.db') == False:
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE password (
        website text, 
        username text, 
        password text
    )""")
    conn.commit()
    conn.close()
else:
    print('DB already exist. \n ------------------------------')

# GUI
frame = LabelFrame(root, text="input here", padx=20, pady=20)
title_label = Label(root, text='This bloody thing will log your passwords for different websites. ',
                    padx=15,
                    pady=15
                    )
frame.grid(row=1, column=0, columnspan=2, padx=30, pady=30)
title_label.grid(row=0, column=0, columnspan=2)

website_label = Label(frame, text='Enter the website name here: ', padx=15, pady=15)
website_label.grid(row=0, column=0, columnspan=2)

e1 = Entry(frame, width=50, bg='white', fg='black', borderwidth=5)
e1.grid(row=1, column=0, columnspan=2)

name_label = Label(frame, text='Enter the user name here: ', padx=15, pady=15)
name_label.grid(row=2, column=0, columnspan=2)

e2 = Entry(frame, width=50, bg='white', fg='black', borderwidth=5)
e2.grid(row=3, column=0, columnspan=2)

password_label = Label(frame, text='Enter the password here: ', padx=15, pady=15)
password_label.grid(row=4, column=0, columnspan=2)

e3 = Entry(frame, width=50, bg='white', fg='black', borderwidth=5)
e3.grid(row=5, column=0, columnspan=2)


# functions
def store():
    website = e1.get()
    usn = e2.get()
    pw = e3.get()
    # sql process
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("INSERT INTO password VALUES ('{}', '{}', '{}')".format(website, usn, pw))
    conn.commit()
    conn.close()
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)


def show():
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * from password")
    items = c.fetchall()
    now = datetime.now()
    print(now.strftime("%H:%M:%S"))
    for i in items:
        print('Index: {}. Website: {}. Username: {}. Password: {}. '.format(i[0], i[1], i[2], i[3]))
    print('------------------------------')
    conn.commit()
    conn.close()
    showinfo(title='Hey brudda', message='The result has been printed in the command window. ')


def change():
    global e4
    top = Toplevel()
    top.geometry("350x400")
    change_label1 = Label(top, text='Enter the index of the record you want to delete. ')
    change_label1.grid(row=0, column=0, padx=10, pady=10)
    e4 = Entry(top, width=50, bg='white', fg='black', borderwidth=5)
    e4.grid(row=1, column=0, padx=10, pady=10)
    btn_exe_change = Button(top, text='Store', width=15, height=3, font=("Helvetica", 12), command=change_exe)
    btn_exe_change.grid(row=2, column=0, padx=10, pady=10)


def change_exe():
    del_ind = e4.get()
    e4.delete(0,END)
    conn = sqlite3.connect('password.db')
    c = conn.cursor()
    c.execute("DELETE from password WHERE rowid = {}".format(str(del_ind)))
    conn.commit()
    conn.close()
    showinfo(message='Record No.{} is deleted. '.format(str(del_ind)))
    return


def quit_all():
    root.quit()


btn_store = Button(root, text='Store', width=15, height=3, font=("Helvetica", 12), command=store)
btn_show = Button(root, text='Show Records', width=15, height=3, font=("Helvetica", 12), command=show)
btn_change = Button(root, text='Delete Record', width=15, height=3, font=("Helvetica", 12), command=change)
btn_quit = Button(root, text='Quit', width=15, height=3, font=("Helvetica", 12), command=quit_all)

btn_store.grid(row=2, column=0, padx=10, pady=10)
btn_show.grid(row=2, column=1, padx=10, pady=10)
btn_change.grid(row=3, column=0, padx=10, pady=10)
btn_quit.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()
