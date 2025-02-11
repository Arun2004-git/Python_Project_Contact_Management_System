import MySQLdb
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk

try:
    conn = MySQLdb.connect(
    host="localhost",
    user="root",          # Your MySQL username
    passwd="password",    # Your MySQL password
    db="contactDB"       # Your database name
    )
    cursor = conn.cursor()
except Exception as e:
    showerror("Database Error",f"Connection error:{e}!")

def search():
    for row in tree.get_children():
        tree.delete(row)
    name=esearch.get().capitalize()
    if not name:
        showwarning("Empty Field","Enter name!")
        return
    try:
        cursor.execute("select * from contact where name=%s",(name,))
        data=cursor.fetchall()
        if not data:
            showwarning("Not matched","Result not found!")
            return
        for items in data:
            tree.insert("",END, values=items)
        #showinfo("Success","Data retrived successfully!")
        esearch.delete(0,END)
    except Exception as e:
        showerror("Database Error", f"Error adding record: {e}")
    

def display():
    for row in tree.get_children():
        tree.delete(row)
    try:
        cursor.execute("select * from contact")
        data=cursor.fetchall()
        for items in data:
            tree.insert("",END, values=items)
        #showinfo("Success","Data retrived successfully!")
    except Exception as e:
        showerror("Database Error", f"Error adding record: {e}")




def add_data():
    name=ename.get().capitalize()
    gender=gender_var.get()
    address=eaddress.get().capitalize()
    contact=econtact.get()
    if not name or not gender or not address or not contact :
        showwarning("Empty Field","All field must be fill!")
        return
    try:
        cursor.execute("insert into contact(name,gender,address,contact_number) values(%s,%s,%s,%s)",(name,gender,address,contact))
        conn.commit()
        id= cursor.lastrowid
        showinfo("Success","Data inserted successfully!")
        data=(id,name,gender,address,contact)
        #tree.insert(END,f"Name:{name}   Geneder:{gender}   Address:{address}   Contact No.:{contact}")
        tree.insert("",END, values=data)
    except Exception as e:
        showerror("Database Error", f"Error adding record: {e}")

def update():
    select=tree.selection()
    if not select:
        showwarning("No Selection", "Please select a row in the Treeview!")
        return
    item=tree.item(select[0])
    id=item["values"][0]
    name=ename.get().capitalize()
    gender=gender_var.get()
    address=eaddress.get().capitalize()
    contact=econtact.get()
    if not name or not gender or not address or not contact :
        showwarning("Empty Field","All field must be fill!")
        return
    try:
        cursor.execute("update contact set name=%s,gender=%s,address=%s,contact_number=%s where id=%s",(name,gender,address,contact,id))
        conn.commit()
        display()
        showinfo("Success","Data updated successfully!")
    except Exception as e:
        showerror("Database Error", f"Error record updating: {e}")
 
def delete_data():
    select=tree.selection()
    if not select:
        showwarning("No Selection", "Please select a row in the Treeview!")
        return
    item=tree.item(select[0])
    id=item["values"][0]
    try:
        cursor.execute("delete from contact where id=%s",(id,))
        conn.commit()
        display()
        showinfo("Success","Data deleted successfully!")
    except Exception as e:
        showerror("Database Error", f"Error record deleting: {e}")
 

def double_click(event):
    reset()
    select=tree.selection()
    item=tree.item(select[0])
    data=item["values"]

    ename.insert(0,data[1])
    gender_var.set(data[2])
    eaddress.insert(0,data[3])
    econtact.insert(0,data[4])


def reset():
    ename.delete(0,END)
    eaddress.delete(0,END)
    econtact.delete(0,END)

root=Tk()
root.title("Contact Management")
root.geometry("1160x550")
root.attributes("-topmost", True)
root["bg"]="Mint Cream"

fnt=("Arial", 12, "bold")
fn=("Arial", 12)
f=Frame(root,bg="Powder Blue")
f.place(x=10,y=1,height=510,width=200)
l1=Label(f,text="Name:",font=fnt,bg="Powder Blue")
l1.pack()
ename=Entry(f,font=fn)
ename.pack()

l2=Label(f,text="Geneder:",font=fnt,bg="Powder Blue")
l2.pack()
gender_var=StringVar()
genders = ["Male", "Female", "Other"]
gender_var.set(genders[0])  # Default value
OptionMenu(f, gender_var, *genders).pack(pady=4, padx=5)
l3=Label(f,text="Address:",font=fnt,bg="Powder Blue")
l3.pack()
eaddress=Entry(f,font=fn)
eaddress.pack()
l4=Label(f,text="Contact No.:",font=fnt,bg="Powder Blue")
l4.pack()
econtact=Entry(f,font=fn)
econtact.pack()
Button(f,text="Submit",font=fnt,height=1,width=12,bg="light green",command=add_data).pack(padx=4,pady=4)

f1=Frame(root,bg="khaki")
f1.place(x=215,y=1,height=510,width=200)
esearch=Entry(f1,width=20,font=fn)
esearch.pack(padx=10,pady=10)
Button(f1,text="Search",bg="Goldenrod",font=fnt,width=15,height=2,command=search).pack(padx=2,pady=2)
Button(f1,text="View",bg="Goldenrod",font=fnt,width=15,height=2,command=display).pack(padx=2,pady=2)
Button(f1,text="Update",bg="Goldenrod",font=fnt,width=15,height=2,command=update).pack(padx=2,pady=2)
Button(f1,text="Delete",bg="Goldenrod",font=fnt,width=15,height=2,command=delete_data).pack(padx=2,pady=2)
Button(f1,text="Reset",bg="Goldenrod",font=fnt,width=15,height=2,command=reset).pack(padx=2,pady=2)

columns = ("ID", "Name", "Gender", "Address","Contact No.")
tree = ttk.Treeview(root, columns=columns, show="headings",height=10)
for col in columns:
    tree.heading(col, text=col)  # Set the column title
    tree.column(col,anchor="center", width=100)  # Adjust column width
tree.place(x=420,y=1,height=510,width=730)
tree.bind("<Double-1>",double_click)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", background="Gainsboro", foreground="Dark Slate Gray", font=("Arial", 12, "bold"))
style.configure("Treeview", background="White", foreground="Black", rowheight=25, font=("Arial", 11))


root.mainloop()
conn.close()