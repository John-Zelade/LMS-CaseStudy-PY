import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, WARNING

from tkcalendar import DateEntry

#LMS Window GUI
window=tkinter.Tk()
window.title("Library Management System")
window.geometry("1100x500")
window['background']='#C4DFDF'

#Books Details
Book_Title = tkinter.StringVar()
Description= tkinter.StringVar()
Author=tkinter.StringVar()
Published_Date=tkinter.StringVar()
Category=tkinter.StringVar()
#Issuing Book Details
bookID=tkinter.StringVar()
studID=tkinter.StringVar()
returnDate=tkinter.StringVar()
issueDate=tkinter.StringVar()
status=tkinter.StringVar()

#Functionalities to manage library
class Library:
    def getBooksData(self):
        selected_row = bookTable.focus()
        data = bookTable.item(selected_row)
        global row
        #return the selected data on the table.
        row = data["values"]

        Book_Title.set(row[1])
        Description.set(row[2])
        Author.set(row[3])
        Published_Date.set(row[4])
        Category.set(row[5])

    def getIssuedBooksData(self):
        selected_row = issuedBookTable.focus()
        data = issuedBookTable.item(selected_row)
        global row
        # return the selected data on the table.
        row = data["values"]

        bookID.set(row[0])
        studID.set(row[1])
        issueDate.set(row[2])
        returnDate.set(row[3])
        status.set(row[4])

    # fetch or display available books in the table
    def fetchBooks(self):
        conn = sqlite3.connect('LMS.db')

        fetch_data = "SELECT * FROM Books"
        bookTable.delete(*bookTable.get_children())
        cursor =conn.execute(fetch_data)
        rows = cursor.fetchall()
        for row in rows:
            bookTable.insert('', tkinter.END, values=row)
        conn.close()

    # fetch or display data of issued books in the table
    def fetchIssueBooks(self):
        conn = sqlite3.connect('LMS.db')

        fetch_data = "SELECT * FROM ReturnBorrowDate"
        issuedBookTable.delete(*issuedBookTable.get_children())
        cursor = conn.execute(fetch_data)
        rows = cursor.fetchall()
        for row in rows:
            issuedBookTable.insert('', tkinter.END, values=row)
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
        pblshd_date_input = DateEntry(details_input_frame, selectmode='day', date_pattern="mm/dd/yyyy" , textvariable=Published_Date, width=25)
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

            Library().fetchBooks()
            cursor.close()
            conn.close()
            addBookWindow.destroy()

            #print(book_title+" "+description+" "+author+" "+published_date+" "+category)

        def clr():
            Book_Title.set("")
            Description.set("")
            Author.set("")
            Category.set("")

        saveBtn=tkinter.Button(addBookWindow, text="Save", command=savebtn,width=10)
        saveBtn.place(x=510,y=150)
        clrBtn = tkinter.Button(addBookWindow, text="Clear",command=clr, width=10)
        clrBtn.place(x=420, y=150)

    def updateBooK(self):
        conn = sqlite3.connect('LMS.db')
        try:
            selected_row = bookTable.focus()
            data = bookTable.item(selected_row)
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
            pblshd_date_input = DateEntry(details_input_frame, selectmode='day', date_pattern="mm/dd/yyyy", textvariable=Published_Date, width=25)
            pblshd_date_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
            # Category input
            category_lbl = tkinter.Label(details_input_frame, text="Catergory")
            category_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            category_input = tkinter.Entry(details_input_frame, textvariable=Category, width=30)
            category_input.grid(row=3, column=1, padx=10, pady=10, sticky="w")

            def updateBook():
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

                Library().fetchBooks()
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
            selected_row = bookTable.focus()
            data = bookTable.item(selected_row)
            global row
            row = data["values"]
            id = row[0]

            answer = askokcancel(
                title='Confirmation',
                message='Are you sure you want to delete the book.',
                icon=WARNING)
            if answer:
                cursor = conn.execute( "SELECT * FROM ReturnBorrowDate WHERE BookID=?",(id,))
                book_row=cursor.fetchall()

                if(len(book_row) >= 1):
                    messagebox.showerror("Cannot Delete", "The book was borrowed.")
                else:
                    conn.execute("DELETE FROM Books WHERE BookID=?",(id,))
                    cursor = conn.execute("SELECT Book_Title, Description,Author,Published_Date, Category from Books")
                    conn.commit()

                    Library().fetchBooks()
                    cursor.close()
                    conn.close()
                    showinfo(
                        title='Book Deleted',
                        message='The book is deleted successfully')

        except IndexError:
            messagebox.showerror("Error", "Please select the book you want to delete")

    def issueBook(self):
        conn = sqlite3.connect('LMS.db')
        status.set("Borrowed")
        # Add book GUI
        issueBookWindow = Toplevel(window)
        issueBookWindow.title("Issue Book")
        issueBookWindow.geometry("600x200")

        # Frame for inputs and labels
        details_input_frame = tkinter.LabelFrame(issueBookWindow, text="Issue Book Details")
        details_input_frame.grid(row=0, column=0, padx=20, pady=20)
        details_input_frame.pack()
        # Book ID Input
        BookID_lbl = tkinter.Label(details_input_frame, text="Book ID")
        BookID_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        BookID_input = tkinter.Entry(details_input_frame, textvariable=bookID, width=30)
        BookID_input.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        # Student ID number Input
        studID_lbl = tkinter.Label(details_input_frame, text="Student ID")
        studID_lbl.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        studID_input = tkinter.Entry(details_input_frame, textvariable=studID, width=30)
        studID_input.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        # Issue Book Date Input
        issueDate_lbl = tkinter.Label(details_input_frame, text="Issue Date")
        issueDate_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        issueDate_input =  DateEntry(details_input_frame, selectmode='day', date_pattern="mm/dd/yyyy" , textvariable=issueDate, width=25)
        issueDate_input.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        # Return date input
        returnDate_lbl = tkinter.Label(details_input_frame, text="Return Date")
        returnDate_lbl.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        returnDate_input = DateEntry(details_input_frame, selectmode='day', date_pattern="mm/dd/yyyy" , textvariable=returnDate, width=25)
        returnDate_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        # set status input
        status_lbl = tkinter.Label(details_input_frame, text="Status:")
        status_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        book_status = tkinter.Label(details_input_frame, textvariable=status)
        book_status.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        def save():
            if BookID_input.get() == "" or studID_input.get() == "" or issueDate_input.get() == "" or returnDate_input.get() == "":
                messagebox.showerror("Empty Field", "Please Fill All the Details")
                return
            BookID=BookID_input.get()
            StudID=studID_input.get()
            IssueDate=issueDate_input.get()
            ReturnDate=returnDate_input.get()
            Status=status.get()

            cursor = conn.execute( "SELECT * FROM Books WHERE BookID=?",(BookID,))
            bookRow = cursor.fetchall()
            cursor = conn.execute("SELECT * FROM Students WHERE StudentID=?", (StudID,))
            studentRow = cursor.fetchall()
            if(len(bookRow)!=1):
                messagebox.showerror("Doesn't Exist", "The book id doesn't exist,")
            elif(len(studentRow)!=1):
                messagebox.showerror("Doesn't Exist", "The student id doesn't exist,")
            else:
                print(bookRow)
                print(studentRow)
                conn.execute("INSERT INTO ReturnBorrowDate(BookID, StudentID, IssueDate, ReturnDate, Status) VALUES (?, ?, ?, ?, ?)",
                             (str(BookID), str(StudID),str(IssueDate),str(ReturnDate),str(Status)))
                cursor = conn.execute("SELECT BookID, StudentID, IssueDate, ReturnDate, Status from ReturnBorrowDate")
                conn.commit()
                messagebox.showinfo("Success", "Book successfully borrowed.")

                Library().fetchIssueBooks()
                cursor.close()
                conn.close()
                issueBookWindow.destroy()
        def clr():
            bookID.set("")
            studID.set("")

        saveBtn = tkinter.Button(issueBookWindow, text="Save", command=save, width=10)
        saveBtn.place(x=510, y=150)
        clrBtn = tkinter.Button(issueBookWindow, text="Clear",command=clr, width=10)
        clrBtn.place(x=420, y=150)
    def returnBook(self):
        try:
            status.set("Returned")
            selected_row = issuedBookTable.focus()
            data = issuedBookTable.item(selected_row)
            global row
            row = data["values"]
            #return the id of the selected data.
            id = row[0]

            # Add book GUI
            issueBookWindow = Toplevel(window)
            issueBookWindow.title("Issue Book")
            issueBookWindow.geometry("600x200")

            # Frame for inputs and labels
            details_input_frame = tkinter.LabelFrame(issueBookWindow, text="Issue Book Details")
            details_input_frame.grid(row=0, column=0, padx=20, pady=20)
            details_input_frame.pack()
            # Book ID Input
            BookID_lbl = tkinter.Label(details_input_frame, text="Book ID")
            BookID_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            BookID_input = tkinter.Label(details_input_frame, textvariable=bookID, width=30)
            BookID_input.grid(row=1, column=1, padx=10, pady=10, sticky="w")
            # Student ID number Input
            studID_lbl = tkinter.Label(details_input_frame, text="Student ID")
            studID_lbl.grid(row=1, column=2, padx=10, pady=10, sticky="w")
            studID_input = tkinter.Label(details_input_frame, textvariable=studID, width=30)
            studID_input.grid(row=1, column=3, padx=10, pady=10, sticky="w")
            # Issue Book Date Input
            issueDate_lbl = tkinter.Label(details_input_frame, text="Issue Date")
            issueDate_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            issueDate_input = tkinter.Label(details_input_frame,
                                        textvariable=issueDate, width=25)
            issueDate_input.grid(row=2, column=1, padx=10, pady=10, sticky="w")
            # Return date input
            returnDate_lbl = tkinter.Label(details_input_frame, text="Return Date")
            returnDate_lbl.grid(row=2, column=2, padx=10, pady=10, sticky="w")
            returnDate_input = tkinter.Label(details_input_frame,
                                         textvariable=returnDate, width=25)
            returnDate_input.grid(row=2, column=3, padx=10, pady=10, sticky="w")
            # set status input
            status_lbl = tkinter.Label(details_input_frame, text="Set Status To:")
            status_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
            book_status = tkinter.Label(details_input_frame, textvariable=status)
            book_status.grid(row=3, column=1, padx=10, pady=10, sticky="w")

            def bookReturned():
                conn = sqlite3.connect('LMS.db')
                Status=status.get()
                conn.execute(
                    "UPDATE ReturnBorrowDate SET Status=? WHERE BookID=?",
                    (str(Status), id,))
                cursor = conn.execute("SELECT Status from ReturnBorrowDate")
                conn.commit()
                messagebox.showinfo("Book Returned", "Book successfully returned!")

                Library().fetchIssueBooks()
                cursor.close()
                conn.close()
                issueBookWindow.destroy()

            returnBtn = tkinter.Button(issueBookWindow, text="Return", command=bookReturned, width=20)
            returnBtn.place(x=440, y=150)
        except IndexError:
            messagebox.showerror("Error", "Please select the book you want to return")
    def deleteIssuedBook(self):
        conn = sqlite3.connect('LMS.db')
        try:
            selected_row = issuedBookTable.focus()
            data = issuedBookTable.item(selected_row)
            global row
            row = data["values"]
            BookID= row[0]
            StudID = row[1]
            print(BookID, StudID)
            answer = askokcancel(
                title='Confirmation',
                message='Are you sure you want to delete the book.',
                icon=WARNING)
            if answer:
                    conn.execute("DELETE FROM ReturnBorrowDate WHERE BookID=? and StudentID=?", (BookID, StudID))
                    cursor = conn.execute("SELECT IssueDate, ReturnDate, Status from ReturnBorrowDate")
                    conn.commit()

                    Library().fetchIssueBooks()
                    cursor.close()
                    conn.close()
                    showinfo(
                        title='Record Deleted',
                        message='Record is deleted successfully')

        except IndexError:
            messagebox.showerror("Error", "Please select the record you want to delete")

    def viewBooks(self):
        table_book_frame.pack(pady=10, padx=10)
        table_Issuedbooks_frame.pack_forget()
        img_frame.pack_forget()
    def viewIssueBooks(self):
        table_Issuedbooks_frame.pack(pady=10, padx=10)
        table_book_frame.pack_forget()
        img_frame.pack_forget()
#Image frame
bg=PhotoImage(file="images\Lms_bg.png")
img_frame=tkinter.Frame(window, height=600, width=900)
backgroung=tkinter.Label(img_frame,image=bg)
backgroung.place(x=0, y=0, relwidth=1, relheight=1)
bgText=tkinter.Label(img_frame, text="Library Management System", font=("", 25, "bold"))
bgText.place(x=20, y=20,)
#Button Frame
button_frame = tkinter.Frame(window, bg='#D2E9E9', height=600, width=200)
#Button
insertBtn=tkinter.Button(button_frame, text="Add New Book", command=Library().addBook, width=20)
insertBtn.place(x=25, y=25)
viewBtn=tkinter.Button(button_frame, text="View Books",command=Library().viewBooks, width=20)
viewBtn.place(x=25, y=55)
editBtn=tkinter.Button(button_frame, text="Edit Book", command=Library().updateBooK, width=20)
editBtn.place(x=25, y=85)
deleteBtn=tkinter.Button(button_frame, text="Delete Book", command=Library().deleteBook, width=20)
deleteBtn.place(x=25, y=115)
issueBtn=tkinter.Button(button_frame, text="Issue Book",command=Library().issueBook, width=20)
issueBtn.place(x=25, y=165)
viewIssuedBtn=tkinter.Button(button_frame, text="View Issued Books",command=Library().viewIssueBooks, width=20)
viewIssuedBtn.place(x=25, y=195)
returnBtn=tkinter.Button(button_frame, text="Return Book",command=Library().returnBook, width=20)
returnBtn.place(x=25, y=225)
deleteIssueBookBtn=tkinter.Button(button_frame, text="Delete Issued Book",command=Library().deleteIssuedBook, width=20)
deleteIssueBookBtn.place(x=25, y=255)


# Available Book Table
table_book_frame = tkinter.Frame(window, bg='#C4DFDF')

style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 12),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 12))  # Modify the font of the headings

bookTable = ttk.Treeview(table_book_frame, columns=('Book ID', 'Book Title', 'Description', 'Author', 'Published Date','Category'), show='headings', style="mystyle.Treeview")
bookTable.pack(pady=10, padx=10)
bookTable.heading('Book ID', text='Book ID')
bookTable.heading('Book Title', text='Book Title')
bookTable.heading('Description', text='Description')
bookTable.heading('Author', text='Author')
bookTable.heading('Published Date', text='Published Date')
bookTable.heading('Category', text='Category')

bookTable.column('Book ID', width=60, anchor="center")
bookTable.column('Book Title', width=150,anchor="center")
bookTable.column('Description', width=200, anchor="center")
bookTable.column('Author', width=150, anchor="center")
bookTable.column('Published Date', width=150,anchor="center")
bookTable.column('Category', width=100, anchor="center")
# mouse button where user click to set user input data
bookTable.bind("<ButtonRelease-1>", Library.getBooksData)
Library().fetchBooks()



# Issued Book Table
table_Issuedbooks_frame = tkinter.Frame(window, bg='#C4DFDF')

style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 12),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 12))  # Modify the font of the headings

issuedBookTable = ttk.Treeview(table_Issuedbooks_frame, columns=('Book ID', 'Student ID', 'Issue Date', 'Return Date', 'Status'), show='headings', style="mystyle.Treeview")
issuedBookTable.pack(padx=10,pady=10)
issuedBookTable.heading('Book ID', text='Book ID')
issuedBookTable.heading('Student ID', text='Student ID')
issuedBookTable.heading('Issue Date', text='Issue Date')
issuedBookTable.heading('Return Date', text='Return Date')
issuedBookTable.heading('Status', text='Status')

issuedBookTable.column('Book ID', width=60, anchor="center")
issuedBookTable.column('Student ID', width=150,anchor="center")
issuedBookTable.column('Issue Date', width=200, anchor="center")
issuedBookTable.column('Return Date', width=150, anchor="center")
issuedBookTable.column('Status', width=150,anchor="center")
# mouse button where user click to set user input data
issuedBookTable.bind("<ButtonRelease-1>", Library.getIssuedBooksData)
Library().fetchIssueBooks()

button_frame.pack(side='left')
img_frame.pack()
window.resizable(False,False)
window.mainloop()