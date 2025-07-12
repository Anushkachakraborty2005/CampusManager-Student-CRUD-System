from tkinter import *
import time
import pymysql
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import csv # Import for CSV export

# --- Global Variables for Buttons and Database Connection ---
addstudentButton = None
searchstudentButton = None
updatestudentButton = None
deletestudentButton = None
showstudentButton = None
exportstudentButton = None
exitButton = None

con = None # Global variable for database connection
mycursor = None # Global variable for database cursor

# --- Function to display all student data in the Treeview ---
def show_student():
    global mycursor, con
    if mycursor is None or con is None or not con.open:
        messagebox.showerror('Error', 'Database not connected. Please connect to the database first.')
        return

    try:
        query = 'SELECT * FROM student'
        mycursor.execute(query)
        fetch_data = mycursor.fetchall()

        # Clear existing data in the Treeview
        studentTable.delete(*studentTable.get_children())

        # Insert fetched data into the Treeview
        for data in fetch_data:
            studentTable.insert('', END, values=list(data))
    except pymysql.Error as e:
        messagebox.showerror('Database Error', f'Failed to fetch data: {e}')
    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred while showing data: {e}')


# --- Function to search for students ---
def search_student():
    def search_data():
        global mycursor, con
        if mycursor is None or con is None or not con.open:
            messagebox.showerror('Error', 'Database not connected. Please connect to the database first.', parent=search_window)
            return

        search_by = searchbyCombobox.get()
        search_text = searchEntry.get()

        if not search_text:
            messagebox.showwarning('Warning', 'Please enter a search term.', parent=search_window)
            return

        # Map combobox selection to actual column names in the database
        column_map = {
            'Student ID': 'ID',
            'Name': 'Name',
            'Mobile No': 'Mobile',
            'Email Id': 'Email',
            'Address': 'Address'
        }
        db_column = column_map.get(search_by)

        if not db_column:
            messagebox.showerror('Error', 'Invalid search category selected.', parent=search_window)
            return

        try:
            # Construct the search query
            query = f"SELECT * FROM student WHERE {db_column} LIKE %s"
            mycursor.execute(query, (f'%{search_text}%',)) # Use LIKE for partial matching
            fetch_data = mycursor.fetchall()

            studentTable.delete(*studentTable.get_children()) # Clear current display

            if not fetch_data:
                messagebox.showinfo('No Results', 'No matching records found.', parent=search_window)
            else:
                for data in fetch_data:
                    studentTable.insert('', END, values=list(data))
            search_window.destroy() # Close search window after displaying results
        except pymysql.Error as e:
            messagebox.showerror('Database Error', f'Failed to search data: {e}', parent=search_window)
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred during search: {e}', parent=search_window)

    search_window = Toplevel()
    search_window.title('Search Student')
    search_window.grab_set()
    search_window.resizable(False, False)

    searchbyLabel = Label(search_window, text='Search By', font=('times new roman', 15, 'bold'))
    searchbyLabel.grid(row=0, column=0, padx=10, pady=10)

    searchbyCombobox = ttk.Combobox(search_window, font=('roman', 12), state='readonly', width=15)
    searchbyCombobox['values'] = ('Student ID', 'Name', 'Mobile No', 'Email Id', 'Address')
    searchbyCombobox.grid(row=0, column=1, padx=10, pady=10)
    searchbyCombobox.set('Name') # Default search category

    searchEntry = Entry(search_window, font=('roman', 15), width=20)
    searchEntry.grid(row=0, column=2, padx=10, pady=10)

    searchButton = ttk.Button(search_window, text='Search', command=search_data)
    searchButton.grid(row=1, columnspan=3, pady=10)


# --- Function to add a new student ---
def add_student():
    def add_data():
        global mycursor, con
        if mycursor is None or con is None or not con.open:
            messagebox.showerror('Error', 'Database not connected. Please connect to the database first.', parent=add_window)
            return

        # Check if all required fields are filled
        if (idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or
            addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()==''):
            messagebox.showerror('Error','All Fields Are Required',parent=add_window)
        else:
            # Get current date and time in specified formats
            date = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')

            # Define the SQL INSERT query with placeholders for 9 values
            query = 'INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                # Execute the query, ensuring the correct variables (date and currenttime) are passed
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),
                                        addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
                con.commit() # Commit the changes to the database

                # Show success message and ask to clear the form
                result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clear the form?', parent=add_window)
                if result:
                    # Clear the entry fields
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    phoneEntry.delete(0,END)
                    emailEntry.delete(0,END)
                    addressEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    dobEntry.delete(0,END)
                show_student() # Refresh the Treeview after adding data
            except pymysql.IntegrityError:
                messagebox.showerror('Error', 'Student ID already exists. Please use a unique ID.', parent=add_window)
                con.rollback()
            except pymysql.Error as e:
                # Catch specific PyMySQL errors
                messagebox.showerror('Database Error', f'Failed to add data: {e}', parent=add_window)
                con.rollback() # Rollback changes on error
            except Exception as e:
                # Catch any other unexpected errors
                messagebox.showerror('Error', f'An unexpected error occurred: {e}', parent=add_window)
                con.rollback() # Rollback changes on error


    # Create the Toplevel window for adding student data
    add_window=Toplevel()
    add_window.title('Add New Student')
    add_window.resizable(False,False) # Set resizable property here
    add_window.grab_set() # Set grab_set property here

    # Labels and Entry fields for student details
    idLabel = Label(add_window,text='ID',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,pady=15,padx=10)

    nameLabel = Label(add_window,text='Name',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    nameEntry.grid(row=1,column=1,pady=15,padx=10)

    phoneLabel = Label(add_window,text='Phone',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    phoneEntry.grid(row=2,column=1,pady=15,padx=10)

    emailLabel = Label(add_window,text='Email',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    emailEntry.grid(row=3,column=1,pady=15,padx=10)

    addressLabel = Label(add_window,text='Address',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    addressEntry.grid(row=4,column=1,pady=15,padx=10)

    genderLabel = Label(add_window,text='Gender',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    genderEntry.grid(row=5,column=1,pady=15,padx=10)

    dobLabel = Label(add_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    dobEntry.grid(row=6,column=1,pady=15,padx=10)

    # Button to trigger data addition
    add_student_button=Button(add_window,text='ADD STUDENT',command=add_data)
    add_student_button.grid(row=7,columnspan=2,pady=15)


# --- Function to update student data ---
def update_student():
    global mycursor, con
    if mycursor is None or con is None or not con.open:
        messagebox.showerror('Error', 'Database not connected. Please connect to the database first.')
        return

    selected_item = studentTable.focus() # Get the currently selected item
    if not selected_item:
        messagebox.showwarning('Warning', 'Please select a student record to update.')
        return

    # Get data from the selected item
    data = studentTable.item(selected_item)['values']

    def save_updated_data():
        global mycursor, con
        if mycursor is None or con is None or not con.open:
            messagebox.showerror('Error', 'Database not connected. Please connect to the database first.', parent=update_window)
            return

        # Get updated values from entry fields
        updated_id = idEntry.get()
        updated_name = nameEntry.get()
        updated_phone = phoneEntry.get()
        updated_email = emailEntry.get()
        updated_address = addressEntry.get()
        updated_gender = genderEntry.get()
        updated_dob = dobEntry.get()
        updated_time = time.strftime('%H:%M:%S') # Update time on modification

        if (updated_id=='' or updated_name=='' or updated_phone=='' or updated_email=='' or
            updated_address=='' or updated_gender=='' or updated_dob==''):
            messagebox.showerror('Error','All Fields Are Required',parent=update_window)
            return

        try:
            # Construct UPDATE query
            query = """
                UPDATE student SET
                    ID = %s, Name = %s, Mobile = %s, Email = %s, Address = %s,
                    Gender = %s, DOB = %s, Time = %s
                WHERE ID = %s
            """
            # Pass updated values and the original ID for the WHERE clause
            mycursor.execute(query, (updated_id, updated_name, updated_phone, updated_email,
                                      updated_address, updated_gender, updated_dob, updated_time, data[0]))
            con.commit()
            messagebox.showinfo('Success', 'Student data updated successfully!', parent=update_window)
            update_window.destroy() # Close update window
            show_student() # Refresh the Treeview
        except pymysql.Error as e:
            messagebox.showerror('Database Error', f'Failed to update data: {e}', parent=update_window)
            con.rollback()
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred during update: {e}', parent=update_window)
            con.rollback()

    update_window = Toplevel()
    update_window.title('Update Student')
    update_window.grab_set()
    update_window.resizable(False, False)

    # Labels and Entry fields, pre-filled with selected student's data
    idLabel = Label(update_window,text='ID',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,pady=15,padx=10)
    idEntry.insert(0, data[0]) # Pre-fill with existing ID

    nameLabel = Label(update_window,text='Name',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    nameEntry.grid(row=1,column=1,pady=15,padx=10)
    nameEntry.insert(0, data[1]) # Pre-fill with existing Name

    phoneLabel = Label(update_window,text='Phone',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    phoneEntry.grid(row=2,column=1,pady=15,padx=10)
    phoneEntry.insert(0, data[2]) # Pre-fill with existing Phone

    emailLabel = Label(update_window,text='Email',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    emailEntry.grid(row=3,column=1,pady=15,padx=10)
    emailEntry.insert(0, data[3]) # Pre-fill with existing Email

    addressLabel = Label(update_window,text='Address',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    addressEntry.grid(row=4,column=1,pady=15,padx=10)
    addressEntry.insert(0, data[4]) # Pre-fill with existing Address

    genderLabel = Label(update_window,text='Gender',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    genderEntry.grid(row=5,column=1,pady=15,padx=10)
    genderEntry.insert(0, data[5]) # Pre-fill with existing Gender

    dobLabel = Label(update_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(update_window,font=('roman',15,'bold'),width=24)
    dobEntry.grid(row=6,column=1,pady=15,padx=10)
    dobEntry.insert(0, data[6]) # Pre-fill with existing DOB

    save_button=Button(update_window,text='SAVE CHANGES',command=save_updated_data)
    save_button.grid(row=7,columnspan=2,pady=15)


# --- Function to delete student data ---
def delete_student():
    global mycursor, con
    if mycursor is None or con is None or not con.open:
        messagebox.showerror('Error', 'Database not connected. Please connect to the database first.')
        return

    selected_items = studentTable.selection() # Get all selected items
    if not selected_items:
        messagebox.showwarning('Warning', 'Please select one or more student records to delete.')
        return

    confirm = messagebox.askyesno('Confirmation', f'Are you sure you want to delete {len(selected_items)} selected record(s)?')
    if confirm:
        try:
            for item in selected_items:
                student_id = studentTable.item(item)['values'][0] # Get ID from the first column
                query = "DELETE FROM student WHERE ID = %s"
                mycursor.execute(query, (student_id,))
            con.commit()
            messagebox.showinfo('Success', f'{len(selected_items)} record(s) deleted successfully.')
            show_student() # Refresh the Treeview
        except pymysql.Error as e:
            messagebox.showerror('Database Error', f'Failed to delete data: {e}')
            con.rollback()
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred during deletion: {e}')
            con.rollback()

# --- Function to export data to CSV ---
def export_data():
    global mycursor, con
    if mycursor is None or con is None or not con.open:
        messagebox.showerror('Error', 'Database not connected. Please connect to the database first.')
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", ".csv"), ("All files", ".*")])
    if not file_path:
        return # User cancelled

    try:
        query = "SELECT * FROM student"
        mycursor.execute(query)
        all_data = mycursor.fetchall()

        if not all_data:
            messagebox.showinfo('No Data', 'No student data available to export.')
            return

        # Get column names for the header
        column_names = [desc[0] for desc in mycursor.description]

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names) # Write header
            writer.writerows(all_data) # Write data rows

        messagebox.showinfo('Success', f'Data exported successfully to {file_path}')
    except pymysql.Error as e:
        messagebox.showerror('Database Error', f'Failed to export data: {e}')
    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred during export: {e}')


# --- Function to connect to database and initialize student table ---
def connect_database():
    def connect():
        global mycursor, con # Declare global variables for cursor and connection
        con = None # Initialize to None
        mycursor = None # Initialize to None
        try:
            # Establish connection to MySQL database
            con = pymysql.connect(
                host=hostnameEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get()
            )
            mycursor = con.cursor()

            # Create database if it doesn't exist
            mycursor.execute("CREATE DATABASE IF NOT EXISTS studentmanagementsystem")
            mycursor.execute("USE studentmanagementsystem") # Use the created database

            # Create student table if it doesn't exist
            mycursor.execute("""
                CREATE TABLE IF NOT EXISTS student (
                    ID INT NOT NULL PRIMARY KEY,
                    Name VARCHAR(100),
                    Mobile VARCHAR(15),
                    Email VARCHAR(100),
                    Address VARCHAR(255),
                    Gender VARCHAR(10),
                    DOB VARCHAR(20),
                    Date VARCHAR(20),  -- Column for date
                    Time VARCHAR(20)   -- Column for time
                )
            """)
            con.commit() # Commit table creation

            # Enable all main action buttons after successful connection and setup
            addstudentButton.config(state='normal')
            searchstudentButton.config(state='normal')
            updatestudentButton.config(state='normal')
            deletestudentButton.config(state='normal')
            showstudentButton.config(state='normal')
            exportstudentButton.config(state='normal')

            messagebox.showinfo('Success', 'Database connection established and setup complete!', parent=connectWindow)
            connectWindow.destroy() # Close the connection window
            show_student() # Display existing data after successful connection

        except pymysql.err.OperationalError as e:
            # Handle database connection errors (e.g., wrong credentials, server down)
            messagebox.showerror('Connection Error', f'{e}\nCheck credentials and server status.', parent=connectWindow)
            if con: con.rollback() # Rollback any pending transactions if connection exists
        except Exception as e:
            # Handle any other unexpected errors during connection/setup
            messagebox.showerror('Error', f'Unexpected error: {e}', parent=connectWindow)
            if con: con.rollback() # Rollback any pending transactions if connection exists
        finally:
            # Note: For long-running apps, it's generally better to keep the connection open
            # and reuse the global con and mycursor.
            # Closing here means reconnecting for every operation, which is inefficient.
            # However, for simplicity and to avoid resource leaks in this example,
            # we'll let the global con and mycursor persist after a successful connection.
            # The finally block here is primarily for cleanup if the initial connection fails.
            pass # Removed close here to keep connection open for subsequent operations


    # Create the Toplevel window for database connection
    connectWindow = Toplevel()
    connectWindow.grab_set() # Make this window modal
    connectWindow.geometry('470x250+730+230') # Set window size and position
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0) # Make window non-resizable

    # Labels and Entry fields for connection details
    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20, pady=10)
    hostnameEntry = Entry(connectWindow, font=('roman', 12, 'bold'), bd=2)
    hostnameEntry.grid(row=0, column=1, padx=40)
    hostnameEntry.insert(0, 'localhost') # Default host

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20, pady=10)
    usernameEntry = Entry(connectWindow, font=('roman', 12, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40)
    usernameEntry.insert(0, 'root') # Default user

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20, pady=10)
    passwordEntry = Entry(connectWindow, font=('roman', 12, 'bold'), bd=2, show='*') # Password field
    passwordEntry.grid(row=2, column=1, padx=40)

    # Button to initiate connection
    connectBtn = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectBtn.grid(row=3, columnspan=2, pady=20)

# --- GUI Functions ---
count = 0
text = ''
s = 'Student Management System'

def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# --- Main Window ---
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance') # Set a theme for the Tkinter window

root.geometry('1174x680+0+0') # Set window size and position
root.resizable(0, 0) # Make main window non-resizable
root.title('Student Management System')

# Date and Time label in the main window
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock() # Start the clock

# Slider text label in the main window
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=250, y=0)
slider() # Start the slider animation

# Button to connect to the database
connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

# --- Left Frame for buttons and logo ---
leftFrame = Frame(root, bd=2, relief=GROOVE)
leftFrame.place(x=50, y=80, width=300, height=600)

# Student Logo (with fallback if image not found)
try:
    logo_image = PhotoImage(file='student.png')
    logo_Label = Label(leftFrame, image=logo_image)
    logo_Label.grid(row=0, column=0, pady=10)
except TclError:
    logo_Label = Label(leftFrame, text='[Student Logo]', font=('arial', 14, 'bold'), width=20, height=5, relief=RIDGE)
    logo_Label.grid(row=0, column=0, pady=10)

# Action Buttons (initially disabled until database is connected)
addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state='disabled',command=add_student)
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state='disabled',command=search_student)
searchstudentButton.grid(row=2, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state='disabled',command=update_student)
updatestudentButton.grid(row=3, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state='disabled',command=delete_student)
deletestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state='disabled',command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Export Data', width=25, state='disabled',command=export_data)
exportstudentButton.grid(row=6, column=0, pady=20)

# Corrected command for Exit button
exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=root.destroy)
exitButton.grid(row=7, column=0, pady=20)

# --- Right Frame for student data display (Treeview) ---
rightFrame = Frame(root, bd=2, relief=GROOVE)
rightFrame.place(x=350, y=80, width=820, height=600)

# Scrollbars for the Treeview
scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

# Treeview widget to display student data
studentTable = ttk.Treeview(rightFrame, columns=('Student Id', 'Name', 'Mobile No', 'Email Id', 'Address', 'Gender', 'D.O.B', 'Date', 'Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

# Configure scrollbars to control the Treeview
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
studentTable.pack(fill=BOTH, expand=1) # Pack the Treeview to fill the frame

# Define headings for the Treeview columns
studentTable.heading('Student Id', text='Student Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile No', text='Mobile No')
studentTable.heading('Email Id', text='Email Id')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Date', text='Date')
studentTable.heading('Time', text='Time')
studentTable.config(show='headings') # Show only headings, not the default first empty column

# Configure column widths and alignment
studentTable.column('Student Id', width=80, anchor=CENTER)
studentTable.column('Name', width=150, anchor=W)
studentTable.column('Mobile No', width=100, anchor=CENTER)
studentTable.column('Email Id', width=150, anchor=W)
studentTable.column('Address', width=200, anchor=W)
studentTable.column('Gender', width=80, anchor=CENTER)
studentTable.column('D.O.B', width=100, anchor=CENTER)
studentTable.column('Date', width=100, anchor=CENTER)
studentTable.column('Time', width=100, anchor=CENTER)

root.mainloop() # Start the Tkinter event loop