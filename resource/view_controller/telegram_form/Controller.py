#!/usr/bin/env python
# coding: utf-8

# In[1]:


# TODO: 
# - 
# - 
# - 
# - 
# - 


# In[2]:


import os
import sys


path_depth = "../../../"  # adjust the current working directory

if "__file__" not in globals():  # check if running in Jupyter Notebook
    os.system("jupyter nbconvert --to script Controller.ipynb --output Controller")  # convert notebook to script
    os.system("pyuic5 -x View.ui -o View.py")  # convert UI file to Python script


sys.path.append(os.path.abspath(os.path.join(path_depth, "resource", "utility")))


if os.name == "nt":  # Windows NT: Windows New Technology
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my.app.id")


# In[3]:


from View import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pickle


# In[4]:


token = pickle.load(open(f"{path_depth}resource/variable/_token.pkl", "rb"))
print(f"Token: {token}")


# In[5]:


# chat_id = ["fasdf", "asdfsadf"]
# pickle.dump(chat_id, open(f"{path_depth}resource/variable/_chat_id.pkl", "wb"))

chat_id = pickle.load(open(f"{path_depth}resource/variable/_chat_id.pkl", "rb"))
print(f"Chat ID: {chat_id}")


# In[ ]:


class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(f"{path_depth}resource/asset/itc_logo.png"))
        self.setWindowTitle("Telegram Form")
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        self.showFullScreen()

        self.listView_chat_id.setModel(QStringListModel(chat_id))

        self.show()


# In[7]:


app = QApplication([])
win = Window()


win.pushButton_back.setIcon(QIcon(f"{path_depth}resource/asset/previous.png"))

win.pushButton_delete.setText("")
win.pushButton_delete.setIcon(QIcon(f"{path_depth}resource/asset/delete.png"))


win.pushButton_add.setIcon(QIcon(f"{path_depth}resource/asset/add.png"))


def on_lineEdit_token_textChanged(text):
    global token
    token = text
    pickle.dump(token, open(f"{path_depth}resource/variable/_token.pkl", "wb"))
    print(f"Token: {token}")


win.lineEdit_token.textChanged.connect(on_lineEdit_token_textChanged)


def on_pushButton_add_chat_id_clicked():
    if win.lineEdit_add_id.text() and win.lineEdit_add_id.text().strip():
        global chat_id
        new_chat_id = win.lineEdit_add_id.text().strip()
        chat_id.append(new_chat_id)
        win.listView_chat_id.model().setStringList(chat_id)
        pickle.dump(chat_id, open(f"{path_depth}resource/variable/_chat_id.pkl", "wb"))
        print(f"Chat ID: {chat_id}")
        win.lineEdit_add_id.clear()


win.pushButton_add.clicked.connect(on_pushButton_add_chat_id_clicked)
win.lineEdit_add_id.returnPressed.connect(on_pushButton_add_chat_id_clicked)


def on_pushButton_delete_chat_id_clicked():
    if win.listView_chat_id.currentIndex().isValid():
        global chat_id
        index = win.listView_chat_id.currentIndex().row()
        chat_id.pop(index)
        win.listView_chat_id.model().setStringList(chat_id)
        pickle.dump(chat_id, open(f"{path_depth}resource/variable/_chat_id.pkl", "wb"))
        print(f"Chat ID: {chat_id}")


win.pushButton_delete.clicked.connect(on_pushButton_delete_chat_id_clicked)


def on_chat_id_data_changed():
    global chat_id
    chat_id = win.listView_chat_id.model().stringList()
    pickle.dump(chat_id, open(f"{path_depth}resource/variable/_chat_id.pkl", "wb"))
    print(f"Chat ID: {chat_id}")


win.listView_chat_id.model().dataChanged.connect(on_chat_id_data_changed)


def on_button_back_clicked():
    win.close()


win.pushButton_back.clicked.connect(on_button_back_clicked)

app.exec_()
app = None

