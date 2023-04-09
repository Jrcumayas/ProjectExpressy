import pyrebase
from tkinter import *
from tkinter import messagebox

# Firebase integration
firebaseConfig = {
  'apiKey': "AIzaSyCp1j6SOELUcXswdaDzfO8vYU3mjtozahg",
  'authDomain': "expressylogin.firebaseapp.com",
  'databaseURL': "https://expressylogin-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "expressylogin",
  'storageBucket': "expressylogin.appspot.com",
  'messagingSenderId': "28849235839",
  'appId': "1:28849235839:web:19572b0862f508b31a1c4a"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Functions
def handleTextBox(event):
    textBox = event.widget
    if (textBox.name == 'login_Email' or textBox.name == 'create_Email'):
        if event.type == "9": # <FocusIn> event
            if textBox.get() == 'Email':
                textBox.delete(0, 'end')
                textBox.config(show = '')
        elif event.type == "10": # <FocusOut> event
            if textBox.get() == '':
                textBox.insert(0, 'Email')
    elif (textBox.name == 'login_Password' or textBox.name == 'create_Password' or textBox.name == 'create_rePassword'):
        if event.type == "9": # <FocusIn> event
            if textBox.get() == 'Password' or textBox.get() == 'Retype Password':
                textBox.delete(0, 'end')
                textBox.config(show='*')
        elif event.type == "10": # <FocusOut> event
            if textBox.get() == '':
                if (textBox.name == 'create_rePassword'):
                    textBox.insert(0, 'Retype Password')
                else:
                    textBox.insert(0, 'Password')
                textBox.config(show='')

def isEmailFound(account_Email):
    db = firebase.database()
    users = db.child("users").get().val()  # Retrieve all user data from the database
    for user_id, user_data in users.items():  # Iterate over each user in the data
        if user_data.get('email').lower() == account_Email.lower():  # Check if the email matches
            found = 1
            break
        else:
            found = 0
        
    if (found == 1):
        return True
    else:
        return False
    
def signIn(login_Email, login_Password):
    db = firebase.database()
    users = db.child("users").get().val()  # Retrieve all user data from the database
    for user_id, user_data in users.items():  # Iterate over each user in the data
        if user_data.get('email').lower() == (login_Email.get()).lower():  # Check if the email matches
            if user_data.get('password') == login_Password.get():
                found = 1
                break
        else:
            found = 0
        
    if (found == 1):
        displayHomeScreen()
    else:
        messagebox.showerror("Sign In", "Invalid account credentials.")

def signUp(create_Email, create_Password, create_rePassword):
    if (create_Email.get() != 'Email' and create_Email.get() != ''):
        if '@gmail.com' in create_Email.get():
            if isEmailFound(create_Email.get()) == False:
                if (create_Password.get() != 'Password' and create_Password.get() != ''): 
                    if len(create_Password.get()) >= 6:
                        if (create_rePassword.get() != 'Retype Password' and create_rePassword.get() != ''):
                            try:
                                if (create_Password.get() == create_rePassword.get()):
                                    db = firebase.database()
                                    user_data = {
                                        "email": create_Email.get(),
                                        "password": create_Password.get()
                                    }
                                    db.child("users").push(user_data)
                                    messagebox.showinfo("Login", "Account created succesfully!")
                                else:
                                    raise ValueError("Passwords should be the same.")
                            except ValueError as error:
                                messagebox.showerror("Sign Up", error)
                        else:
                            messagebox.showerror("Sign Up", "Retype password.")
                    else:
                        messagebox.showerror("Sign Up", "Password length must be 6 or more.")
                else:
                    messagebox.showerror("Sign Up", "Input password.")
            else:
                messagebox.showerror("Sign Up", "Account already created by a different user.")
        else:
            messagebox.showerror("Sign Up", "Input a valid Email.")
    else:
        messagebox.showerror("Sign Up", "Input an Email.")
        

def displayHomeScreen():
    homeScreen = Toplevel(root)
    homeScreen.title = ("Home")
    homeScreen.geometry('925x500+250+150')
    homeScreen.config(bg = 'white')
    homeScreen.resizable(False, False)

    Label(homeScreen, text = 'HomeScreen', bg = "#fff", font = ('Calibri(Body)', 50, 'bold')).pack(expand = True)

    homeScreen.mainloop()

def displaySignUpScreen():
    root.withdraw()

    signUpScreen = Toplevel(root)
    signUpScreen.title = ("Sign Up")
    signUpScreen.geometry('925x500+250+150')
    signUpScreen.config(bg = 'white')
    signUpScreen.resizable(False, False)

    background_image = PhotoImage(file = "C:\\Users\\jerick royce\\Documents\\Programming\\Python\\opencv journey\\ProjectExpressy\\images\\Expressy.png")
    Label(signUpScreen, image = background_image, bg = 'white').place(x = 1, y = 1)

    signUpFrame = Frame(signUpScreen, width = 350, height = 450, bg = "white")
    signUpFrame.place(x = 520, y = 70)

    heading = Label(signUpFrame, text = 'Sign up', fg = '#57a1f8', bg = 'white', font = ('Arial', 25, 'bold'))
    heading.place(x = 125, y = 20)

    create_Email = Entry(signUpFrame, name = "create_Email", width = 25, fg = 'black', border = 0, bg = 'white', font = ('Arial', 12))
    create_Email.place(x = 30, y = 100)
    create_Email.insert(0, 'Email')
    create_Email.name = "create_Email"
    create_Email.bind('<FocusIn>', handleTextBox)
    create_Email.bind('<FocusOut>', handleTextBox)
    Frame(signUpFrame, width = 295, height = 2, bg = 'black').place(x = 25, y = 130)

    create_Password = Entry(signUpFrame, name = "create_Password", width = 25, fg = 'black', border = 0, bg = 'white', font = ('Arial', 12))
    create_Password.place(x = 30, y = 170)
    create_Password.insert(0, 'Password')
    create_Password.name = "create_Password"
    create_Password.bind('<FocusIn>', handleTextBox)
    create_Password.bind('<FocusOut>', handleTextBox)
    Frame(signUpFrame, width = 295, height = 2, bg = 'black').place(x = 25, y = 200)

    create_rePassword = Entry(signUpFrame, name = "create_rePassword",  width = 25, fg = 'black', border = 0, bg = 'white', font = ('Arial', 12))
    create_rePassword.place(x = 30, y = 240)
    create_rePassword.insert(0, 'Retype Password')
    create_rePassword.name = "create_rePassword"
    create_rePassword.bind('<FocusIn>', handleTextBox)
    create_rePassword.bind('<FocusOut>', handleTextBox)
    Frame(signUpFrame, width = 295, height = 2, bg = 'black').place(x = 25, y = 270)

    Button(signUpFrame, width = 41, pady = 7, text = 'Sign Up', cursor = 'hand2', bg = '#57a1f8', fg = 'white', border = 0, command=lambda: signUp(create_Email, create_Password, create_rePassword)).place(x = 29, y = 300)

    back = Button(signUpFrame, width = 6, text = 'Back', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', font = ('Arial', 9), command = lambda: [signUpScreen.destroy(), root.deiconify()])
    back.place(x = 280, y = 350)

    signUpScreen.protocol("WM_DELETE_WINDOW", lambda: [signUpScreen.destroy(), root.deiconify()])
    signUpScreen.mainloop()

# MAIN
root = Tk()
root.title('Expressy Login')
root.geometry('925x500+250+150')
root.configure(bg = "#fff")
root.resizable(False, False)

# Main Login Screen with background image
background_image = PhotoImage(file = "C:\\Users\\jerick royce\\Documents\\Programming\\Python\\opencv journey\\ProjectExpressy\\images\\Expressy.png")
Label(root, image = background_image, bg = 'white').place(x = 1, y = 1)

# Login frame with Username and Password

frame = Frame(root, width = 350, height = 350, bg = "white")
frame.place(x = 520, y = 70)

heading = Label(frame, text = 'Sign in', fg = '#57a1f8', bg = 'white', font = ('Arial', 25, 'bold'))
heading.place(x = 125, y = 20)

# Username textbox
login_Email = Entry(frame, name = "login_Email",width = 25, fg = 'black', border = 0, bg = 'white', font = ('Arial', 12))
login_Email.place(x = 30, y = 100)
login_Email.insert(0, 'Email')
login_Email.name = 'login_Email'
login_Email.bind('<FocusIn>', handleTextBox)
login_Email.bind('<FocusOut>', handleTextBox)
Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 130)

# Password textbox
login_Password = Entry(frame, name = "login_Password", width = 25, fg = 'black', border = 0, bg = 'white', font = ('Arial', 12))
login_Password.place(x = 30, y = 170)
login_Password.insert(0, 'Password')
login_Password.name = 'login_Password'
login_Password.bind('<FocusIn>', handleTextBox)
login_Password.bind('<FocusOut>', handleTextBox)
Frame(frame, width = 295, height = 2, bg = 'black').place(x = 25, y = 200)

# Forgot password
fpassword = Button(frame, width = 25, text = 'Forgot your password?', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', font = ('Arial', 9))
fpassword.place(x = 165, y = 210)

# Login button
Button(frame, width = 41, pady = 7, text = 'Login', cursor = 'hand2', bg = '#57a1f8', fg = 'white', border = 0, command=lambda: signIn(login_Email, login_Password)).place(x = 29, y = 240)

label = Label(frame, text = "Don't have an account?", fg = 'black', bg = 'white', font = ('Arial', 9))
label.place(x = 75, y = 300)

# Sign up button
sign_up = Button(frame, width = 6, text = 'Sign up', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', font = ('Arial', 9), command = displaySignUpScreen)
sign_up.place(x = 210, y = 300)

################################

root.mainloop()

#KUTOB KOS PAG NAME SA VARIABLE ATAY INSAON MANA
