import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *

def Getvalue(event):
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    row_id=listbox.selection()[0]
    select=listbox.set(row_id)
    e1.insert(0,select["Emp_id"])
    e2.insert(0,select["Emp_name"])
    e3.insert(0,select["mobile"])
    e4.insert(0,select["salary"])


def Add():
    studid=e1.get()
    studname=e2.get()
    coursename=e3.get()
    fees=e4.get()
    
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="root",database="Payroll")
    mycursor=mysqldb.cursor()
    
    try:
        sql="INSERT INTO registration (Emp_id, Emp_name, mobile, salary) values (%s,%s,%s,%s)"
        val=(studid, studname, coursename, fees)
        mycursor.execute(sql,val)
        mysqldb.commit()
        lastid=mycursor.lastrowid
        messagebox.showinfo("Information","Employee inserted successfully...")
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
        e4.delete(0,END)
        e1.focus_set()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()
        
        
def update():
    studid=e1.get()
    studname=e2.get()
    coursename=e3.get()
    fees=e4.get()
    
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="root",database="Payroll")
    mycursor=mysqldb.cursor()
    
    
    try:
        sql="update registration set Emp_name=%s, mobile=%s, salary=%s where Emp_id=%s"
        val=(studname, coursename, fees, studid)
        mycursor.execute(sql,val)
        mysqldb.commit()
        lastid=mycursor.lastrowid
        messagebox.showinfo("Information","Record updated successfully...")
        
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
        e4.delete(0,END)
        e1.focus_set()  
        
    except Exception as e:
        
        print(e)
        mysqldb.rollback()
        mysqldb.close()


def delete():
    studid=e1.get()
    
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="root",database="Payroll")
    mycursor=mysqldb.cursor()
    
    
    try:
        sql=f"delete from registration where Emp_id={studid}"
        mycursor.execute(sql)
        mysqldb.commit()   
        lastid=mycursor.lastrowid
        messagebox.showinfo("Information","Record delete successfully...")
        
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
        e4.delete(0,END)
        e1.focus_set()  
        
    except Exception as e:
        
        print(e)
        mysqldb.rollback()
        mysqldb.close()


def show():  
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="root",database="Payroll")
    mycursor=mysqldb.cursor()           
    mycursor.execute("SELECT Emp_id, Emp_name, mobile, salary FROM registration")
    records=mycursor.fetchall()
    print(records)
    
    clearTreeView()

    for i, (studid, stname, course, fees) in enumerate(records, start=1):
        listbox.insert("","end", values=(studid, stname, course, fees))
        mysqldb.close()

def search():
    studid = e1.get()
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="root",database="Payroll")
    mycursor=mysqldb.cursor()           
    mycursor.execute(f"SELECT Emp_id, Emp_name, mobile, salary FROM registration where Emp_id={studid}")
    records=mycursor.fetchall()

    clearTreeView()
    
    for i, (studid, stname, course, fees) in enumerate(records, start=1):
        listbox.insert("","end", values=(studid, stname, course, fees))
        mysqldb.close()
        

def clearTreeView():
    for child in listbox.get_children(''):
        listbox.delete(child)

root=Tk()
root.geometry("800x500")
global e1
global e2        
global e3
global e4

tk.Label(root, text="Employee Registration", fg="red", font=(None, 30)).place(x=300, y=5)

tk.Label(root, text="Employee ID").place(x=10, y=10)
Label(root, text="Employee Name").place(x=10, y=40)
Label(root, text="Mobile").place(x=10, y=70)
Label(root, text="Salary").place(x=10, y=100)

e1=Entry(root)
e1.place(x=140, y=10)

e2=Entry(root)
e2.place(x=140, y=40)

e3=Entry(root)
e3.place(x=140, y=70)

e4=Entry(root)
e4.place(x=140, y=100)

Button(root, text="Add", command=Add, height=3, width=13).place(x=30, y=130)
Button(root, text="update", command=update, height=3, width=13).place(x=140, y=130)
Button(root, text="Delete", command=delete, height=3, width=13).place(x=250, y=130)
Button(root, text="Show", command=show, height=3, width=13).place(x=360, y=130)
Button(root, text="Search", command=search, height=3, width=13).place(x=470, y=130)

cols=("Emp_id","Emp_name","mobile","salary")
listbox=ttk.Treeview(root, columns=cols, show="headings")

for col in cols:
    listbox.heading(col, text=col)
    listbox.grid(row=1, column=0, columnspan=2)
    listbox.place(x=10, y=200)
    
show()
listbox.bind("<Double-Button-1>", Getvalue)

root.mainloop()