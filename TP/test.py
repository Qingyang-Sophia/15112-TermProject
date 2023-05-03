# This demos app.getUserInput(prompt) and app.showMessage(message)

from cmu_112_graphics import *

def appStarted(app):
    app.message = 'Click the mouse to enter your name!'

def mousePressed(app, event):
    name = app.getUserInput('What is your name?')
    print(type(name))
    if (name == None):
        app.message = 'You canceled!'
    else:
        app.showMessage('You entered: ' + name)
        app.message = f'Hi, {name}!'

def redrawAll(app, canvas):
    font = 'Arial 24 bold'
    canvas.create_text(app.width/2,  app.height/2,
                       text=app.message, font=font, fill='black')

#runApp(width=500, height=300)

# from tkinter import *

# master = Tk()
# e = Entry(master)
# e.pack()

# e.focus_set()

# def callback():
#     print (e.get()) # This is the text you may want to use later

# b = Button(master, text = "OK", width = 10, command = callback)
# b.pack()

# mainloop()


# import tkinter as tk
# from tkinter import simpledialog

# ROOT = tk.Tk()

# ROOT.withdraw()
# # the input dialog
# USER_INP = simpledialog.askstring(title="Test",
#                                   prompt="What's your Name?:")

# # check it out
# print("Hello", USER_INP)

# from tkinter import *

# root = Tk()
# frame = Frame(root)
# frame.pack()

# bottomframe = Frame(root)
# bottomframe.pack( side = BOTTOM )

# redbutton = Button(frame, text="Red", fg="red")
# redbutton.pack( side = LEFT)

# greenbutton = Button(frame, text="green", fg="green")
# greenbutton.pack( side = LEFT )

# bluebutton = Button(frame, text="Blue", fg="blue")
# bluebutton.pack( side = LEFT )

# blackbutton = Button(bottomframe, text="Black", fg="black")
# blackbutton.pack( side = BOTTOM)

# root.mainloop()

# GUI = Tk()
# GUI.configure(background="#002E52")
# GUI.title('Templatewriter')
# GUI.geometry("1920x500")
# e = Entry(GUI)
# e.place(x=0, y=400)
# e.delete(0, END)
# e.insert(0, "Überschrift eingeben")
# box2 = Canvas(GUI, width=200, height=300)
# box2.pack()
# box2.place(x=0, y=0)
# box2.create_text((50, 25), text="Überschrift 1 ", fill="black")
# linie = Canvas(GUI, width=10, height=1080)
# linie.pack()
# # box1 = Canvas(GUI, width=1920, height=1080)
# # box1.pack()

# GUI.mainloop()

# from tkinter import *

# OPTIONS = [
# "Jan",
# "Feb",
# "Mar"
# ] #etc

# master = Tk()
# master.geometry("1920x500")
# variable = StringVar(master)
# variable.set(' Month ') # default value
# optFiles = OptionMenu(root, optVariable,*flist)
# optFiles.pack()
# optFiles.place(x=240,y=250)


# w = OptionMenu(master, variable, *OPTIONS)
# w.pack()

# mainloop()

# Import module
from tkinter import *
  
# Create object
root = Tk()
  
# Adjust size
root.geometry( "200x200" )
  
# Change the label text
def show():
    label.config( text = clicked.get() )
  
# Dropdown menu options
options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
  
# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set( "Monday" )
  
# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()
  
# Create button, it will change label text
button = Button( root , text = "click Me" , command = show ).pack()
  
# Create Label
label = Label( root , text = " " )
label.pack()
  
# Execute tkinter
root.mainloop()