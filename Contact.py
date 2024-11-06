from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import tkinter.font as tkFont  # Importing font module

root = Tk()
root.title("Contact Management System")
root.geometry("800x600")
root.resizable(True, True)
root.config(bg="#a4dded")  # Set background color of the root window

# ============================FONT STYLE===================================
font_style = tkFont.nametofont("TkDefaultFont")
font_style.actual()
font_style.configure(family="Roboto", size=12)  # Set font to Roboto

# ============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()
SEARCH_TERM = StringVar()  # New variable for search term

# ============================DATABASE=====================================
def Database():
    try:
        conn = sqlite3.connect("contact_management.db")
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS member (
                mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                firstname TEXT,
                lastname TEXT,
                gender TEXT,
                age INTEGER,
                address TEXT,
                contact TEXT)"""
        )
        conn.commit()
        cursor.close()
        print("Database initialized.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def RefreshTree(search_query=""):
    try:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact_management.db")
        cursor = conn.cursor()

        # Modify query to search if search_query is provided
        if search_query:
            cursor.execute(
                "SELECT * FROM member WHERE firstname LIKE ? OR lastname LIKE ? OR contact LIKE ? ORDER BY lastname ASC",
                (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%',))
        else:
            cursor.execute("SELECT * FROM member ORDER BY lastname ASC")

        for data in cursor.fetchall():
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        print("Data refreshed in treeview.")
    except Exception as e:
        print(f"Error refreshing tree: {e}")

def SubmitData():
    if any(not var.get() for var in [FIRSTNAME, LASTNAME, GENDER, AGE, ADDRESS, CONTACT]):
        tkMessageBox.showwarning('Warning', 'Please complete the required fields.')
    else:
        try:
            conn = sqlite3.connect("contact_management.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO member (firstname, lastname, gender, age, address, contact) VALUES (?, ?, ?, ?, ?, ?)",
                (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), int(AGE.get()), ADDRESS.get(), CONTACT.get())
            )
            conn.commit()
            cursor.close()
            RefreshTree()
            ClearFields()
            print("Data submitted successfully.")
        except Exception as e:
            print(f"Error submitting data: {e}")

def UpdateData():
    if GENDER.get() == "":
        tkMessageBox.showwarning('Warning', 'Please complete the required fields.')
    else:
        try:
            conn = sqlite3.connect("contact_management.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE member SET firstname=?, lastname=?, gender=?, age=?, address=?, contact=? WHERE mem_id=?",
                (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), int(AGE.get()), ADDRESS.get(), CONTACT.get(), mem_id)
            )
            conn.commit()
            cursor.close()
            RefreshTree()
            ClearFields()
            print("Data updated successfully.")
        except Exception as e:
            print(f"Error updating data: {e}")

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please select a contact to delete.')
    else:
        result = tkMessageBox.askquestion('Delete', 'Are you sure you want to delete this contact?')
        if result == 'yes':
            try:
                curItem = tree.focus()
                contents = tree.item(curItem)
                selecteditem = contents['values']
                conn = sqlite3.connect("contact_management.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM member WHERE mem_id=?", (selecteditem[0],))
                conn.commit()
                cursor.close()
                RefreshTree()
                print("Data deleted successfully.")
            except Exception as e:
                print(f"Error deleting data: {e}")

def ClearFields():
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

def OnSelected(event):
    global mem_id
    curItem = tree.focus()
    contents = tree.item(curItem)
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])

# ============================SEARCH FUNCTIONALITY==========================
def SearchContact():
    query = SEARCH_TERM.get()
    RefreshTree(query)

# ============================CLEAR FUNCTIONALITY===========================
def ClearAll():
    ClearFields()
    RefreshTree()

# ============================EXIT FUNCTIONALITY===========================
def ExitApplication():
    root.quit()

# ============================GUI LAYOUT===================================
Top = Frame(root, bg="#a4dded", bd=5)  # Change background color of top frame
Top.pack(fill=X)

lbl_title = Label(Top, text="Contact Management System", font=('Roboto', 20), bg="#a4dded", fg="white")
lbl_title.pack(pady=10)

Mid = Frame(root, bg="#a4dded")  # Change background color of middle frame
Mid.pack(fill=BOTH, expand=True, padx=10, pady=10)

ContactForm = Frame(Mid, bg="#a4dded")  # Change background color of contact form frame
ContactForm.pack(pady=10, fill=X)

# Create and place labels and entries in a grid layout
labels = ["Firstname", "Lastname", "Gender", "Age", "Address", "Contact"]
variables = [FIRSTNAME, LASTNAME, GENDER, AGE, ADDRESS, CONTACT]
row_index = 0

for label, var in zip(labels, variables):
    lbl = Label(ContactForm, text=f"{label}:", font=('Roboto', 12), bg="#a4dded")  # Label background color change
    lbl.grid(row=row_index, column=0, padx=5, pady=5, sticky=W)

    if label == "Gender":
        Radiobutton(ContactForm, text="Male", variable=GENDER, value="Male", font=('Roboto', 12), bg="#a4dded").grid(row=row_index, column=1, sticky=W)
        Radiobutton(ContactForm, text="Female", variable=GENDER, value="Female", font=('Roboto', 12), bg="#a4dded").grid(row=row_index, column=1, columnspan=2)
    else:
        entry = Entry(ContactForm, textvariable=var, font=('Roboto', 12))
        entry.grid(row=row_index, column=1, padx=5, pady=5, sticky=W)

    row_index += 1

# ============================SEARCH BAR=====================================
SearchFrame = Frame(Mid, bg="#a4dded")  # Change background color of search frame
SearchFrame.pack(pady=10)

lbl_search = Label(SearchFrame, text="Search:", font=('Roboto', 12), bg="#a4dded")  # Label background color change
lbl_search.pack(side=LEFT, padx=5)

entry_search = Entry(SearchFrame, textvariable=SEARCH_TERM, font=('Roboto', 12))
entry_search.pack(side=LEFT, padx=5)

btn_search = Button(SearchFrame, text="Search", command=SearchContact, bg="#0078d4", fg="white", relief="flat",
                    bd=1, width=10, height=2, font=('Roboto', 12))
btn_search.pack(side=LEFT, padx=5)

# ============================BUTTONS=====================================
def round_button(master, text, command, **kwargs):
    """ Creates a button with rounded corners """
    canvas = Canvas(master, height=40, width=120, bg="#0078d4", bd=0, highlightthickness=0)
    canvas.create_oval(5, 5, 115, 35, fill="#0078d4", outline="")
    button = Button(master, text=text, command=command, relief="flat", font=("Roboto", 12), fg="white", bg="#0078d4",
                    width=10, height=2)
    canvas.create_window(60, 20, window=button)
    canvas.pack(side=LEFT, padx=10)

ButtonFrame = Frame(Mid, bg="#a4dded")  # Change background color of button frame
ButtonFrame.pack(pady=10)

round_button(ButtonFrame, "Add", SubmitData)
round_button(ButtonFrame, "Update", UpdateData)
round_button(ButtonFrame, "Delete", DeleteData)
round_button(ButtonFrame, "Clear", ClearAll)
round_button(ButtonFrame, "Exit", ExitApplication)

# ============================TABLES======================================
TableMargin = Frame(root, bg="#a4dded")  # Change background color of table frame
TableMargin.pack(pady=10)

tree = ttk.Treeview(TableMargin, columns=("ID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
                    show="headings", height=6)

tree.heading("ID", text="ID")
tree.heading("Firstname", text="Firstname")
tree.heading("Lastname", text="Lastname")
tree.heading("Gender", text="Gender")
tree.heading("Age", text="Age")
tree.heading("Address", text="Address")
tree.heading("Contact", text="Contact")

tree.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(TableMargin, orient=VERTICAL, command=tree.yview)
scrollbar.pack(side=RIGHT, fill=Y)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

tree.bind("<ButtonRelease-1>", OnSelected)

# ============================INITIALIZATION===============================
Database()
RefreshTree()

root.mainloop()
