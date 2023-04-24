### Python GUI testing

import sys
from random import choice

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu, QPushButton

# window_titles = [
#     'My App',
#     'My App',
#     'Still My App',
#     'Still My App',
#     'What on earth',
#     'What on earth',
#     'This is surprising',
#     'This is surprising',
#     'Something went wrong'
# ]

# Subclass QMainWindow to customize your application's main window
class CustomButton(QPushButton):
    def event(self, e):
        e.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def mousePressEvent(self, event):
        print("Mouse pressed!")
        super().mousePressEvent(event)

    def on_context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec_(self.mapToGlobal(pos))

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec_(e.globalPos())

    def the_button_was_clicked(self):
        print("Clicked.")
        new_window_title = choice(window_titles)
        print("Setting title:  %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

        print(self.button_is_checked)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()


# # https://www.tutorialspoint.com/how-to-place-an-image-into-a-frame-in-tkinter // GeeksForGeeks
# # Import required libraries
# from tkinter import *
# from PIL import ImageTk, Image
#
# # Create an instance of tkinter window
# win = Tk()
#
# # Define the geometry of the window
# win.title("Lenticular Image Creator")
# win.geometry("700x500")
#
# frame = Frame(win, width=600, height=400)
# frame.pack()
# frame.place(anchor='center', relx=0.5, rely=0.5)
#
# menu = Menu(win)
# item = Menu(menu)
# item.add_command(label='New')
# menu.add_cascade(label='File', menu=item)
# win.config(menu=menu)
#
# # adding a label to the root window
# lbl = Label(win, text="Ready to make an image?")
# lbl.grid()
#
# # adding Entry Field
# txt = Entry(win, width=10)
# txt.grid(column=1, row=0)
#
#
# # function to display user text when
# # button is clicked
# def clicked():
#     res = "You wrote" + txt.get()
#     lbl.configure(text=res)
#
#
# # button widget with red color text inside
# btn = Button(win, text="Click me",
#              fg="red", command=clicked)
# # Set Button Grid
# btn.grid(column=2, row=0)
#
# # Create an object of tkinter ImageTk
# img = ImageTk.PhotoImage(Image.open("images/alt1.png"))
#
# # Create a Label Widget to display the text or Image
# label = Label(frame, image = img)
# label.pack()
#
# win.mainloop()
