import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, WARNING

#LMS Window GUI
window=tkinter.Tk()
window.title("Library Management System")
window.geometry("1100x500")
window['background']='#C4DFDF'

Book_Title = tkinter.StringVar()
Description= tkinter.StringVar()
Author=tkinter.StringVar()
Published_Date=tkinter.StringVar()
Category=tkinter.StringVar()

#Functionalities to manage library
class Library:
    def getData(self):
        selected_row = table.focus()
        data = table.item(selected_row)
        global row
        #return the selected data on the table.
        row = data["values"]

        Book_Title.set(row[1])
        Description.set(row[2])
        Author.set(row[3])
        Published_Date.set(row[4])
        Category.set(row[5])
    # fetch or display data in the table
    def fetch(self):
        conn = sqlite3.connect('LMS.db')

        fetch_data = "SELECT * FROM Books"
        table.delete(*table.get_children())
        cursor =conn.execute(fetch_data)
        rows = cursor.fetchall()
        for row in rows:
            table.insert('', tkinter.END, values=row)
        conn.close()
    def addBook(self):
        # Add book GUI
        addBookWindow =Toplevel(window)
        addBookWindow.title("Add New Book")
        addBookWindow.geometry("600x200")

        #Frame for inputs and labels
        details_input_frame=tkinter.LabelFrame(addBookWindow, text="Books Details")
        details_input_frame.grid(row=0, column=0, padx=20, pady=20)
        details_input_frame.pack()
        #Book Title Input
        Book_lbl = tkinter.Label(details_input_frame, text="Title")
        Book_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Book_input = tkinter.Entry(details_input_frame, textvariable=Book_Title, width=30)
        Book_input.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        #Book Description Input
        desc_lbl = tkinter.Label(details_input_frame, text="Description")
        desc_lbl.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        desc_input = tkinter.Entry(details_input_frame, textvariable=Description, width=30)
        desc_input.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        #Book Author Input
        author_lbl = tkinter.Label(details_input_frame, text="Author")
        author_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        author_input = tkinter.Entry(details_input_frame, textvariable=Author, width=30)
        author_input.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        #Published date input
        pblshd_date_lbl = tkinter.Label(details_input_frame, text="Published Date")
        pblshd_date_lbl.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        pblshd_date_input = tkinter.Entry(details_input_frame, textvariable=Published_Date, width=30)
        pblshd_date_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        # Category input
        category_lbl = tkinter.Label(details_input_frame, text="Catergory")
        category_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        category_input = tkinter.Entry(details_input_frame, textvariable=Category, width=30)
        category_input.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        def savebtn():
            conn = sqlite3.connect('LMS.db')
            if Book_input.get() == "" or desc_input.get() == "" or author_input.get() == "" or pblshd_date_input.get() == "" or category_input.get() == "":
                messagebox.showerror("Empty Field", "Please Fill All the Detailes")
                return

            book_title=Book_input.get()
            description=desc_input.get()
            author=author_input.get()
            published_date=pblshd_date_input.get()
            category=category_input.get()

            conn.execute("INSERT INTO Books(Book_Title, Description,Author,Published_Date, Category) "
                         "VALUES (?, ?, ?, ?, ?)", (str(book_title), str(description),str(author), str(published_date),str(category)))
            cursor = conn.execute("SELECT Book_Title, Description,Author,Published_Date, Category from Books")
            conn.commit()
            messagebox.showinfo("New Book Added", "New book successfully added!")

            Library().fetch()
            cursor.close()
            conn.close()
            addBookWindow.destroy()

            #print(book_title+" "+description+" "+author+" "+published_date+" "+category)

        saveBtn=tkinter.Button(addBookWindow, text="Save", command=savebtn,width=20)
        saveBtn.place(x=440,y=150)

    def updateBooK(self):
        try:
            selected_row = table.focus()
            data = table.item(selected_row)
            global row
            row = data["values"]
            #return the id of the selected data.
            id = row[0]

            # Add book GUI
            updateBookWindow = Toplevel(window)
            updateBookWindow.title("Update Book Details")
            updateBookWindow.geometry("600x200")

            # Frame for inputs and labels
            details_input_frame = tkinter.LabelFrame(updateBookWindow, text="Books Details")
            details_input_frame.grid(row=0, column=0, padx=20, pady=20)
            details_input_frame.pack()
            # Book Title Input
            Book_lbl = tkinter.Label(details_input_frame, text="Title")
            Book_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            Book_input = tkinter.Entry(details_input_frame, textvariable=Book_Title, width=30)
            Book_input.grid(row=1, column=1, padx=10, pady=10, sticky="w")
            # Book Description Input
            desc_lbl = tkinter.Label(details_input_frame, text="Description")
            desc_lbl.grid(row=1, column=2, padx=10, pady=10, sticky="w")
            desc_input = tkinter.Entry(details_input_frame, textvariable=Description, width=30)
            desc_input.grid(row=1, column=3, padx=10, pady=10, sticky="w")
            # Book Author Input
            author_lbl = tkinter.Label(details_input_frame, text="Author")
            author_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            author_input = tkinter.Entry(details_input_frame, textvariable=Author, width=30)
            author_input.grid(row=2, column=1, padx=10, pady=10, sticky="w")
            # Published date input
            pblshd_date_lbl = tkinter.Label(details_input_frame, text="Published Date")
            pblshd_date_lbl.grid(row=2, column=2, padx=10, pady=10, sticky="w")
            pblshd_date_input = tkinter.Entry(details_input_frame, textvariable=Published_Date, width=30)
            pblshd_date_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
            # Category input
            category_lbl = tkinter.Label(details_input_frame, text="Catergory")
            category_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            category_input = tkinter.Entry(details_input_frame, textvariable=Category, width=30)
            category_input.grid(row=3, column=1, padx=10, pady=10, sticky="w")

            def updateBook():
                conn = sqlite3.connect('LMS.db')
                if Book_input.get() == "" or desc_input.get() == "" or author_input.get() == "" or pblshd_date_input.get() == "" or category_input.get() == "":
                    messagebox.showerror("Empty Field", "Please Check All the Details")
                    return
                book_title = Book_input.get()
                description = desc_input.get()
                author = author_input.get()
                published_date = pblshd_date_input.get()
                category = category_input.get()

                conn.execute("UPDATE Books SET Book_Title=?, Description=?,Author=?,Published_Date=?, Category=? WHERE BookID=?",
                             (str(book_title), str(description), str(author), str(published_date), str(category), id,))
                cursor = conn.execute("SELECT Book_Title, Description,Author,Published_Date, Category from Books")
                conn.commit()
                messagebox.showinfo("Book Updated", "Book successfully updated!")

                Library().fetch()
                cursor.close()
                conn.close()
                updateBookWindow.destroy()

            updateBtn = tkinter.Button(updateBookWindow, text="Update", command=updateBook, width=20)
            updateBtn.place(x=440, y=150)

        except IndexError:
            messagebox.showerror("Error", "Please select the book you want to update")

    def deleteBook(self):
        conn = sqlite3.connect('LMS.db')
        try:
            selected_row = table.focus()
            data = table.item(selected_row)
            global row
            row = data["values"]
            id = row[0]
            print(id)

            answer = askokcancel(
                title='Confirmation',
                message='Are you sure you want to delete the book.',
                icon=WARNING)
            if answer:
                conn.execute("DELETE FROM Books WHERE BookID=?",(id,))
                cursor = conn.execute("SELECT Book_Title, Description,Author,Published_Date, Category from Books")
                conn.commit()

                Library().fetch()
                cursor.close()
                conn.close()
                showinfo(
                    title='Book Deleted',
                    message='The book is deleted successfully')

        except IndexError:
            messagebox.showerror("Error", "Please select the book you want to delete")

    def issueBook(self):
        # Add book GUI
        issueBookWindow = Toplevel(window)
        issueBookWindow.title("Issue Book")
        issueBookWindow.geometry("600x200")

        # Frame for inputs and labels
        details_input_frame = tkinter.LabelFrame(issueBookWindow, text="Issue Book Details")
        details_input_frame.grid(row=0, column=0, padx=20, pady=20)
        details_input_frame.pack()
        # Book Title Input
        BookID_lbl = tkinter.Label(details_input_frame, text="Book ID")
        BookID_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        BookID_input = tkinter.Entry(details_input_frame, textvariable=Book_Title, width=30)
        BookID_input.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        # Book Description Input
        desc_lbl = tkinter.Label(details_input_frame, text="Description")
        desc_lbl.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        desc_input = tkinter.Entry(details_input_frame, textvariable=Description, width=30)
        desc_input.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        # Book Author Inputu
        author_lbl = tkinter.Label(details_input_frame, text="Athor")
        author_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        author_input = tkinter.Entry(details_input_frame, textvariable=Author, width=30)
        author_input.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # Published date input
        pblshd_date_lbl = tkinter.Label(details_input_frame, text="Published Date")
        pblshd_date_lbl.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        pblshd_date_input = tkinter.Entry(details_input_frame, textvariable=Published_Date, width=30)
        pblshd_date_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        # Category input
        category_lbl = tkinter.Label(details_input_frame, text="Catergory")
        category_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        category_input = tkinter.Entry(details_input_frame, textvariable=Category, width=30)
        category_input.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    def viewBooks(self):
        table_frame.pack(pady=10, padx=10)

#Button Frame
button_frame = tkinter.Frame(window, bg='#D2E9E9', height=600, width=200)
#Button
insertBtn=tkinter.Button(button_frame, text="Add New Book", command=Library().addBook, width=20)
insertBtn.place(x=25, y=25)
issueBtn=tkinter.Button(button_frame, text="Issue Book", width=20)
issueBtn.place(x=25, y=55)
editBtn=tkinter.Button(button_frame, text="Edit Book", command=Library().updateBooK, width=20)
editBtn.place(x=25, y=85)
deleteBtn=tkinter.Button(button_frame, text="Delete Book", command=Library().deleteBook, width=20)
deleteBtn.place(x=25, y=115)
viewBtn=tkinter.Button(button_frame, text="View Books", command=Library().viewBooks, width=20)
viewBtn.place(x=25, y=145)
viewIssuedBtn=tkinter.Button(button_frame, text="View Issued Books", width=20)
viewIssuedBtn.place(x=25, y=175)
returnBtn=tkinter.Button(button_frame, text="Return Book", width=20)
returnBtn.place(x=25, y=205)

#Table
table_frame = tkinter.Frame(window, bg='#C4DFDF')

style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 12),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 12))  # Modify the font of the headings

table = ttk.Treeview(table_frame, columns=('Book ID', 'Book Title', 'Description', 'Author', 'Published Date','Category'), show='headings', style="mystyle.Treeview")

table.heading('Book ID', text='Book ID')
table.heading('Book Title', text='Book Title')
table.heading('Description', text='Description')
table.heading('Author', text='Author')
table.heading('Published Date', text='Published Date')
table.heading('Category', text='Category')

table.pack(pady=20, padx=10)

table.column('Book ID', width=60, anchor="center")
table.column('Book Title', width=150,anchor="center")
table.column('Description', width=200, anchor="center")
table.column('Author', width=150, anchor="center")
table.column('Published Date', width=150,anchor="center")
table.column('Category', width=100, anchor="center")
# mouse button where user click to set user input data
table.bind("<ButtonRelease-1>", Library.getData)
Library().fetch()

button_frame.pack(side='left')
window.mainloop()