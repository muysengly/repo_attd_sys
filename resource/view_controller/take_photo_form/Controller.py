#!/usr/bin/env python
# coding: utf-8

# In[1]:


# TODO:
# - make sure only on person is in the image
# - make sure the face is big enough
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


os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["NO_ALBUMENTATIONS_UPDATE"] = "1"


if os.name == "nt":
    import ctypes

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my.app.id")


# In[3]:


from insightface.app import FaceAnalysis

from View import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import cv2
import pickle
import numpy as np


# In[4]:


fa = FaceAnalysis(name="buffalo_sc", root=f"{os.getcwd()}/{path_depth}resource/utility/", providers=["CPUExecutionProvider"])
fa.prepare(ctx_id=-1, det_thresh=0.5, det_size=(320, 320))


# In[5]:


cap = cv2.VideoCapture(0)


class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(f"{path_depth}resource/asset/my_logo.png"))
        self.setWindowTitle("Take Photo Form")

        self.faces = []
        self.SKIP_FRAMES = 10
        self.frame_count = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(int(1000 / 30))  # 30 FPS

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)

        self.show()

    def paintEvent(self, e):
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        self.frame_count += 1
        if self.frame_count % self.SKIP_FRAMES == 0:
            self.frame_count = 0
            self.faces = fa.get(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if len(self.faces) == 0:
            self.pushButton_take_photo.setEnabled(False)
            cv2.putText(img=frame, text="No face detected!", org=(10, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 0, 255), thickness=2)

        elif len(self.faces) == 1:
            # for face in self.faces:
            face = self.faces[0]
            box = face.bbox.astype(int)
            if (box[2] - box[0]) > 160 or (box[3] - box[1]) > 160:
                self.pushButton_take_photo.setEnabled(True)
                cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 0), thickness=2)
                cv2.putText(img=frame, text="Face detected!", org=(10, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 255, 0), thickness=2)
            else:
                self.pushButton_take_photo.setEnabled(False)
                cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 0, 255), thickness=2)
                cv2.putText(img=frame, text="Face too small!", org=(10, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 0, 255), thickness=2)

        else:
            self.pushButton_take_photo.setEnabled(False)
            cv2.putText(img=frame, text="Too many faces detected!", org=(10, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 0, 255), thickness=2)
            for face in self.faces:
                box = face.bbox.astype(int)
                cv2.rectangle(img=frame, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 0, 255), thickness=2)

        _image = cv2.resize(frame, (self.label_camera.width(), self.label_camera.height()))
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
        q_image = QImage(_image.data, _image.shape[1], _image.shape[0], _image.strides[0], QImage.Format_RGB888)
        q_pixmap = QPixmap.fromImage(q_image)
        self.label_camera.setPixmap(q_pixmap)


# In[6]:


app = QApplication([])
win = Window()

win.pushButton_back.setIcon(QIcon(f"{path_depth}resource/asset/previous.png"))
win.pushButton_take_photo.setIcon(QIcon(f"{path_depth}resource/asset/photo-camera.png"))


def take_photo():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    image = np.array(frame)
    pickle.dump(image, open(path_depth + "resource/variable/_photo.pkl", "wb"))

    win.close()


win.pushButton_take_photo.clicked.connect(take_photo)


def on_button_back_clicked():
    win.close()


win.pushButton_back.clicked.connect(on_button_back_clicked)


app.exec_()
app = None
cap.release()

