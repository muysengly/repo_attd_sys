#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    # pass  # Windows system
elif os.name == "posix":  # POSIX: Portable Operating System Interface
    if "darwin" in os.sys.platform:
        pass  # macOS system
    else:
        # os.environ["DISPLAY"] = ":0"  # Set display
        # os.environ["QT_QPA_PLATFORM"] = "wayland"  # Set platform for Qt
        pass # Linux system
else:
    pass  # Other OS


# In[2]:


from FaceModel import fa  # NOTE: this library need to import first

from View import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cv2
import pickle
import numpy as np
import subprocess


# In[3]:


from FaceDatabase import FaceDataBase

database_face = FaceDataBase(path_depth + "database.sqlite")


# In[4]:


def is_ascii(text):
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


# In[5]:


table_name = "table_face"
face_names = database_face.read_face_names(table_name)


# In[6]:


class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(f"{path_depth}resource/asset/itc_logo.png"))
        self.setWindowTitle("Face Management Form")

        self.listView_name.setModel(QStringListModel(face_names))

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        self.showFullScreen()

        self.show()


# In[7]:


app = QApplication([])
win = Window()


win.pushButton_upload_image_1.setIcon(QIcon(f"{path_depth}resource/asset/image-upload.png"))
win.pushButton_upload_image_2.setIcon(QIcon(f"{path_depth}resource/asset/image-upload.png"))
win.pushButton_take_photo_1.setIcon(QIcon(f"{path_depth}resource/asset/photo-camera.png"))
win.pushButton_take_photo_2.setIcon(QIcon(f"{path_depth}resource/asset/photo-camera.png"))
win.pushButton_back.setIcon(QIcon(f"{path_depth}resource/asset/previous.png"))
win.pushButton_add.setIcon(QIcon(f"{path_depth}resource/asset/add_person.png"))
win.pushButton_delete.setText("")
win.pushButton_delete.setIcon(QIcon(f"{path_depth}resource/asset/delete.png"))
win.pushButton_clear_image_1.setText("")
win.pushButton_clear_image_1.setIcon(QIcon(f"{path_depth}resource/asset/delete.png"))
win.pushButton_clear_image_2.setText("")
win.pushButton_clear_image_2.setIcon(QIcon(f"{path_depth}resource/asset/delete.png"))

_name = ""


def on_button_add_click():

    win.listView_name.clearSelection()

    text = win.lineEdit_name.text()
    if text is not None:
        if text.strip() != "":
            if is_ascii(text):
                text = text.strip()
                if text.upper() not in database_face.read_face_names(table_name):
                    win.listView_name.model().insertRow(win.listView_name.model().rowCount())
                    index = win.listView_name.model().index(win.listView_name.model().rowCount() - 1)
                    win.listView_name.model().setData(index, text.upper())
                    win.listView_name.setCurrentIndex(win.listView_name.model().index(win.listView_name.model().rowCount() - 1, 0))
                    database_face.create_face_name(table_name, text.upper())

                else:
                    QMessageBox.warning(win, "Warning", "Name already exists!")
            else:
                QMessageBox.warning(win, "Warning", "Name must be ASCII characters only!")
        else:
            QMessageBox.warning(win, "Warning", "Name cannot be empty!")
    else:
        QMessageBox.warning(win, "Warning", "Name cannot be empty!")

    win.lineEdit_name.clear()
    win.lineEdit_name.setFocus()


win.pushButton_add.clicked.connect(on_button_add_click)
win.lineEdit_name.returnPressed.connect(on_button_add_click)


def on_listview_double_click():
    global _name
    if win.listView_name.selectedIndexes():
        seleted = win.listView_name.selectedIndexes()[0]
        _name = seleted.data()


win.listView_name.doubleClicked.connect(on_listview_double_click)


def on_listview_data_changed():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]

        if selected.data().strip() == "":
            win.listView_name.model().removeRow(selected.row())
            database_face.delete_face_name(table_name, _name)

        elif selected.data().strip().upper() in database_face.read_face_names(table_name) and selected.data().strip() != _name:
            QMessageBox.warning(win, "Warning", "Name already exists!")
            win.listView_name.model().setData(selected, _name)

        elif selected.data().upper() != _name:
            win.listView_name.model().setData(selected, selected.data().strip().upper())
            database_face.update_face_name(table_name, _name, selected.data().strip().upper())


win.listView_name.model().dataChanged.connect(on_listview_data_changed)


def on_listview_single_clicked():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]

        img_1 = database_face.read_image_1(table_name, selected.data())
        if img_1 is not None and len(img_1) > 0:
            img_1 = cv2.resize(img_1, (win.label_image_1.width(), win.label_image_1.height()))
            img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
            q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB).data, img_1.shape[1], img_1.shape[0], QImage.Format.Format_RGB888))
            win.label_image_1.setPixmap(q_pixmap)

        else:
            win.label_image_1.clear()
            win.label_image_1.setText("No data")

        img_2 = database_face.read_image_2(table_name, selected.data())
        if img_2 is not None and len(img_2) > 0:
            img_2 = cv2.resize(img_2, (win.label_image_2.width(), win.label_image_2.height()))
            img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB)
            q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB).data, img_2.shape[1], img_2.shape[0], QImage.Format.Format_RGB888))
            win.label_image_2.setPixmap(q_pixmap)
        else:
            win.label_image_2.clear()
            win.label_image_2.setText("No data")


win.listView_name.selectionModel().selectionChanged.connect(on_listview_single_clicked)


def on_button_delete_clicked():
    if win.listView_name.selectedIndexes():

        selected = win.listView_name.selectedIndexes()[0]
        # print(selected)
        index = selected.row()
        name = selected.data()
        # print(name)

        win.listView_name.model().removeRow(selected.row())
        database_face.delete_face_name(table_name, name)

        # Clear images if no data left
        if len(database_face.read_face_names(table_name)) == 0:
            win.label_image_1.clear()
            win.label_image_1.setText("No data")
            win.label_image_2.clear()
            win.label_image_2.setText("No data")
        else:
            win.listView_name.setCurrentIndex(win.listView_name.model().index(index - 1 if index - 1 >= 0 else 0, 0))
            on_listview_single_clicked()


win.pushButton_delete.clicked.connect(on_button_delete_clicked)


def on_button_upload_image_1_clicked():

    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]

        file_name, _ = QFileDialog.getOpenFileName(win, "Open Image File", "", "Images (*.jpg);")
        if file_name:

            image = np.array(cv2.imread(file_name))
            faces = fa.get(image)

            if len(faces) == 1:
                face = faces[0]
                box = face.bbox.astype(int)
                if (box[2] - box[0]) > 160 or (box[3] - box[1]) > 160:
                    database_face.create_image_1_from_path(table_name, selected.data(), file_name)
                    database_face.create_emb_1(table_name, selected.data(), faces[0].embedding)

                    _image = cv2.resize(image, (win.label_image_1.width(), win.label_image_1.height()))
                    q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(_image, cv2.COLOR_BGR2RGB).data, _image.shape[1], _image.shape[0], QImage.Format.Format_RGB888))
                    win.label_image_1.setPixmap(q_pixmap)
                else:
                    msg = QMessageBox(win)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Face is too small!")
                    msg.setWindowTitle("Database Error")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()

            elif len(faces) == 0:

                msg = QMessageBox(win)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("No face detected!")
                msg.setWindowTitle("Database Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

            else:
                msg = QMessageBox(win)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Too many faces detected!")
                msg.setWindowTitle("Database Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()


win.pushButton_upload_image_1.clicked.connect(on_button_upload_image_1_clicked)


def on_button_upload_image_2_clicked():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]

        file_name, _ = QFileDialog.getOpenFileName(win, "Open Image File", "", "Images (*.jpg)")
        if file_name:

            image = np.array(cv2.imread(file_name))
            faces = fa.get(image)
            if len(faces) == 1:

                face = faces[0]
                box = face.bbox.astype(int)
                if (box[2] - box[0]) > 160 or (box[3] - box[1]) > 160:

                    database_face.create_image_2_from_path(table_name, selected.data(), file_name)
                    database_face.create_emb_2(table_name, selected.data(), faces[0].embedding)

                    _image = cv2.resize(image, (win.label_image_2.width(), win.label_image_2.height()))
                    q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(_image, cv2.COLOR_BGR2RGB).data, _image.shape[1], _image.shape[0], QImage.Format.Format_RGB888))
                    win.label_image_2.setPixmap(q_pixmap)

                else:
                    msg = QMessageBox(win)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Face is too small!")
                    msg.setWindowTitle("Database Error")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()

            elif len(faces) == 0:
                msg = QMessageBox(win)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("No face detected!")
                msg.setWindowTitle("Database Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

            else:
                msg = QMessageBox(win)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Too many faces detected!")
                msg.setWindowTitle("Database Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()


win.pushButton_upload_image_2.clicked.connect(on_button_upload_image_2_clicked)


def on_button_take_photo_1_clicked():

    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]
        # win.hide()

        pickle.dump(None, open(path_depth + "resource/variable/_photo.pkl", "wb"))

        os.system("python " + path_depth + "resource/view_controller/take_photo_form/Controller.py")

        photo = pickle.load(open(path_depth + "resource/variable/_photo.pkl", "rb"))

        if photo is not None:
            database_face.create_image_1_from_array(table_name, selected.data(), photo)
            database_face.create_emb_1(table_name, selected.data(), fa.get(photo)[0].embedding)
            _image = cv2.resize(photo, (win.label_image_1.width(), win.label_image_1.height()))
            q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(_image, cv2.COLOR_BGR2RGB).data, _image.shape[1], _image.shape[0], QImage.Format.Format_RGB888))
            win.label_image_1.setPixmap(q_pixmap)

        pickle.dump(None, open(path_depth + "resource/variable/_photo.pkl", "wb"))

        # win.show()


win.pushButton_take_photo_1.clicked.connect(on_button_take_photo_1_clicked)


def on_button_take_photo_2_clicked():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]
        # win.hide()

        pickle.dump(None, open(path_depth + "resource/variable/_photo.pkl", "wb"))

        os.system("python " + path_depth + "resource/view_controller/take_photo_form/Controller.py")

        photo = pickle.load(open(path_depth + "resource/variable/_photo.pkl", "rb"))

        if photo is not None:

            database_face.create_image_2_from_array(table_name, selected.data(), photo)
            database_face.create_emb_2(table_name, selected.data(), fa.get(photo)[0].embedding)

            _image = cv2.resize(photo, (win.label_image_2.width(), win.label_image_2.height()))
            q_pixmap = QPixmap.fromImage(QImage(cv2.cvtColor(_image, cv2.COLOR_BGR2RGB).data, _image.shape[1], _image.shape[0], QImage.Format.Format_RGB888))
            win.label_image_2.setPixmap(q_pixmap)

        pickle.dump(None, open(path_depth + "resource/variable/_photo.pkl", "wb"))

        # win.show()


win.pushButton_take_photo_2.clicked.connect(on_button_take_photo_2_clicked)


def on_button_clear_image_1_clicked():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]
        win.label_image_1.clear()
        win.label_image_1.setText("No data")

        database_face.delete_image_1(table_name, selected.data())
        database_face.delete_emb_1(table_name, selected.data())


win.pushButton_clear_image_1.clicked.connect(on_button_clear_image_1_clicked)


def on_button_clear_image_2_clicked():
    if win.listView_name.selectedIndexes():
        selected = win.listView_name.selectedIndexes()[0]

        win.label_image_2.clear()
        win.label_image_2.setText("No data")

        database_face.delete_image_2(table_name, selected.data())
        database_face.delete_emb_2(table_name, selected.data())


win.pushButton_clear_image_2.clicked.connect(on_button_clear_image_2_clicked)


def on_button_back_clicked():
    app.exit()


win.pushButton_back.clicked.connect(on_button_back_clicked)


app.exec_()
app = None

