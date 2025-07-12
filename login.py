from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    if userNameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif userNameEntry.get() == 'Anu' or passwordEntry.get() == '1234':
        messagebox.showinfo('Login Successful', f"Welcome, {userNameEntry.get()}")
        window.destroy()
        import sms

    else:
        messagebox.showerror('Error', 'Please Enter Correct Username & Passowrd')

# Initialize main window
window = Tk()
window.geometry('1280x700+0+0')
window.title('Login System Of Student Management System')
window.resizable(False, False)

# Load and place background image
backgroundImage = ImageTk.PhotoImage(Image.open('bg.jpg').resize((1280, 700)))
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

# Create login frame
loginFrame = Frame(window, bg='white')
loginFrame.place(x=400, y=150)

# Logo
logoImage = PhotoImage(file='logo.png')
logoLabel = Label(loginFrame, image=logoImage, bg='white')
logoLabel.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

# Username field
usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white', bd=5, fg='royalblue')
usernameLabel.grid(row=1, column=0, padx=10, pady=10)

userNameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'),
                      bg='white', bd=5, fg='royalblue')
userNameEntry.grid(row=1, column=1, padx=10, pady=10)

# Password field
passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white', bd=5, fg='royalblue')
passwordLabel.grid(row=2, column=0, padx=10, pady=10)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'),
                      bg='white', bd=5, fg='royalblue', show='*')
passwordEntry.grid(row=2, column=1, padx=10, pady=10)

# Login button
loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=10,
                     fg='white', bg='cornflowerblue', cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)


window.mainloop()