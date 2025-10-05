#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys


path_depth = "../../../"  # adjust the current working directory

if "__file__" not in globals():  # check if running in Jupyter Notebook
    os.system("jupyter nbconvert --to script Controller.ipynb --output Controller")  # convert notebook to script

    from PyQt5 import uic

    with open("View.ui", "r", encoding="utf-8") as ui_file, open("View.py", "w", encoding="utf-8") as py_file:
        uic.compileUi(ui_file, py_file, execute=True)


sys.path.append(os.path.abspath(os.path.join(path_depth, "resource", "utility")))

os.environ["QT_SCALE_FACTOR"] = "1"  # Set scaling factor
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Enable automatic scaling
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"  # Set screen scaling

if os.name == "nt":  # Windows NT: Windows New Technology
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my.app.id")

    # pass  # Windows system
elif os.name == "posix":  # POSIX: Portable Operating System Interface
    if "darwin" in os.sys.platform:
        pass  # macOS system
    else:
        pass  # Linux system
else:
    pass  # Other OS


# In[ ]:


from View import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pickle


# In[ ]:


token = pickle.load(open(f"{path_depth}resource/variable/_token.pkl", "rb"))
# print(f"Token: {token}")
chat_id = pickle.load(open(f"{path_depth}resource/variable/_chat_id.pkl", "rb"))
# print(f"Chat ID: {chat_id}")


# In[5]:


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


# In[1]:


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
    app.exit()


win.pushButton_back.clicked.connect(on_button_back_clicked)

app.exec_()
app = None

