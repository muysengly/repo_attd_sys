#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
        pass  # Linux system
else:
    pass  # Other OS


# In[2]:


from FaceModel import fa

from View import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cv2
import pickle
import zipfile
import requests
import subprocess
import numpy as np


from datetime import datetime as dt


# In[ ]:


log_folder = os.path.join(path_depth, "log")
if not os.path.exists(log_folder):
    os.makedirs(log_folder)


# In[3]:


from FaceDatabase import FaceDataBase

face_database = FaceDataBase(path_depth + "database.sqlite")

from AttendanceDatabase import AttendanceDatabase

# attd_db = AttendanceDatabase(path_depth + "attendance.sqlite")
attd_database = AttendanceDatabase(path_depth + "database.sqlite")


# In[4]:


# initialize variables

if not os.path.exists(f"{path_depth}resource/variable/_token.pkl"):
    pickle.dump([], open(f"{path_depth}resource/variable/_token.pkl", "wb"))

if not os.path.exists(f"{path_depth}resource/variable/_chat_id.pkl"):
    pickle.dump([], open(f"{path_depth}resource/variable/_chat_id.pkl", "wb"))

if not os.path.exists(f"{path_depth}resource/variable/_photo.pkl"):
    pickle.dump([], open(f"{path_depth}resource/variable/_photo.pkl", "wb"))

if not os.path.exists(f"{path_depth}resource/variable/_threshold.pkl"):
    pickle.dump(70, open(f"{path_depth}resource/variable/_threshold.pkl", "wb"))


# In[5]:


table_name = "table_face"

face_names = face_database.read_face_names(table_name)

threshold = pickle.load(open(path_depth + "resource/variable/_threshold.pkl", "rb"))


# In[6]:


def compare_faces_cosine(emb1, emb2):
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return similarity


# In[7]:


def send_telegram_message(chat_id, message, photo, token=pickle.load(open(f"{path_depth}resource/variable/_token.pkl", "rb"))):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    files = {"photo": open(photo, "rb")}
    data = {"chat_id": chat_id, "caption": message}
    response = requests.post(url, files=files, data=data)
    return response.json()


# In[8]:


cap = []


class Window(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(f"{path_depth}resource/asset/itc_logo.png"))
        self.setWindowTitle("Check Attendance Form")

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        self.showFullScreen()

        self.label_itc_logo.setPixmap(QPixmap(f"{path_depth}resource/asset/itc_logo.png").scaled(self.label_itc_logo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_gtr_logo.setPixmap(QPixmap(f"{path_depth}resource/asset/gtr_logo.png").scaled(self.label_gtr_logo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.listView_attd.setModel(QStringListModel([]))

        self.faces = []

        self.SKIP_FRAMES = 10
        self.frame_count = 0
        self.attd_timestamps = {}
        self.database = face_database.read_name_emb1_emb2(table_name)

        self.clockEvent()  # set initial clock
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clockEvent)
        self.clock.start(1000)  # update every second

        self.dateEvent()  # set initial date
        self.date = QTimer(self)
        self.date.timeout.connect(self.dateEvent)
        self.date.start(60 * 1000)  # update every minute

        self.show()

    def dateEvent(self):
        self.label_date.setText(dt.now().strftime("%Y-%m-%d"))

    def clockEvent(self):
        self.label_clock.setText(dt.now().strftime("%H:%M:%S"))

    def paintEvent(self, event):
        global cap

        if not cap:
            cap = cv2.VideoCapture(0)
        else:

            _, frame = cap.read()

            frame = cv2.flip(frame, 1)

            self.frame_count += 1
            if self.frame_count % self.SKIP_FRAMES == 0:
                self.frame_count = 0
                self.database = face_database.read_name_emb1_emb2(table_name)
                self.faces = fa.get(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if len(self.faces) > 0:
                for face in self.faces:

                    box = face.bbox.astype(int)

                    # check if face is too small
                    if (box[2] - box[0]) < 100 or (box[3] - box[1]) < 100:  # skip small faces
                        cv2.rectangle(img=frame, pt1=(box[0] - 20, box[1] - 20), pt2=(box[2] + 20, box[3] + 20), color=(0, 0, 255), thickness=2)
                        cv2.putText(img=frame, text="Too small!", org=(box[0] - 15, box[3] + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
                        continue

                    # check if face is in database
                    if len(self.database) == 0:
                        cv2.rectangle(img=frame, pt1=(box[0] - 20, box[1] - 20), pt2=(box[2] + 20, box[3] + 20), color=(0, 0, 255), thickness=2)
                        cv2.putText(img=frame, text="No database!", org=(box[0] - 15, box[3] + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
                        continue

                    # check if face out of screen
                    if box[0] - 20 < 0 or box[1] - 20 < 0 or box[2] + 20 > frame.shape[1] or box[3] + 20 > frame.shape[0]:
                        continue

                    # compare face with database
                    scores = [max(compare_faces_cosine(face.embedding, data[1]) if data[1] is not None else 0, compare_faces_cosine(face.embedding, data[2]) if data[2] is not None else 0) for data in self.database]

                    if np.max(scores) > threshold / 100:

                        cv2.rectangle(img=frame, pt1=(box[0] - 20, box[1] - 20), pt2=(box[2] + 20, box[3] + 20), color=(0, 255, 0), thickness=2)
                        cv2.putText(img=frame, text=f"{np.max(scores)*100:.0f}% {self.database[np.argmax(scores)][0]}", org=(box[0] - 15, box[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2)
                        cv2.putText(img=frame, text="Attended!", org=(box[0] - 15, box[3] + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0), thickness=2)

                        # Check if name is already in attendance list
                        if self.database[np.argmax(scores)][0] not in self.listView_attd.model().stringList():

                            # Add name to attendance list
                            self.listView_attd.model().insertRow(self.listView_attd.model().rowCount())

                            self.listView_attd.model().setData(self.listView_attd.model().index(self.listView_attd.model().rowCount() - 1), self.database[np.argmax(scores)][0])
                            self.listView_attd.scrollToBottom()

                            name = self.database[np.argmax(scores)][0]
                            self.attd_timestamps[name] = dt.now()

                            timer = QTimer(self)
                            timer.setSingleShot(True)
                            timer.timeout.connect(lambda n=name: (self.attd_timestamps.pop(n, None), getattr(self, "attd_timers", {}).pop(n, None), self.listView_attd.model().removeRow(self.listView_attd.model().stringList().index(n)) if n in self.listView_attd.model().stringList() else None))
                            timer.start(60 * 1000)  # 1 minute

                            if not hasattr(self, "attd_timers"):
                                self.attd_timers = {}
                            self.attd_timers[name] = timer

                            attd_database.add_data(self.database[np.argmax(scores)][0], dt.now().strftime("%Y-%m-%d"), dt.now().strftime("%H:%M:%S"))

                            log_path = f"{path_depth}log/log_{table_name}_{self.database[np.argmax(scores)][0]}_{dt.now().strftime('%Y%m%d')}{dt.now().strftime('%H%M%S')}.jpg"
                            cv2.imwrite(log_path, frame)

                            # Send Telegram message
                            if len(pickle.load(open(f"{path_depth}resource/variable/_token.pkl", "rb"))) > 0 and len(pickle.load(open(f"{path_depth}resource/variable/_chat_id.pkl", "rb"))) > 0:
                                for id in pickle.load(open(f"{path_depth}resource/variable/_chat_id.pkl", "rb")):
                                    message = f"Attendance Alert!\nName: {self.database[np.argmax(scores)][0]}\nTime: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                    send_telegram_message(id, message, log_path)

                    else:

                        cv2.rectangle(img=frame, pt1=(box[0] - 20, box[1] - 20), pt2=(box[2] + 20, box[3] + 20), color=(0, 0, 255), thickness=2)
                        cv2.putText(img=frame, text=f"{np.max(scores)*100:.0f}% {self.database[np.argmax(scores)][0]}", org=(box[0] - 15, box[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
                        cv2.putText(img=frame, text="Unknown!", org=(box[0] - 15, box[3] + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)

            _image = cv2.resize(frame, (self.label_camera.width(), self.label_camera.height()))
            _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
            q_image = QImage(_image.data, _image.shape[1], _image.shape[0], _image.strides[0], QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_image)

            self.label_camera.setPixmap(q_pixmap)


# In[9]:


cap = cv2.VideoCapture(0)
app = QApplication([])
win = Window()


win.spinBox_threshold.setValue(threshold)

version_string = open(path_depth + "resource/variable/_version.txt", "r").read().strip()
version_int = list(map(int, version_string.split(".")))
win.label_version.setText(f"{version_string}")


win.pushButton_telegram.setText(" Telegram")
win.pushButton_telegram.setIcon(QIcon(f"{path_depth}resource/asset/telegram.png"))

win.pushButton_query.setText(" Query")
win.pushButton_query.setIcon(QIcon(f"{path_depth}resource/asset/query.png"))

win.pushButton_update.setText(" Update")
win.pushButton_update.setIcon(QIcon(f"{path_depth}resource/asset/update.png"))

win.pushButton_register.setText(" Register")
win.pushButton_register.setIcon(QIcon(f"{path_depth}resource/asset/register.png"))

win.pushButton_close.setStyleSheet("background-color: red; color: white;")


def f_threshold_change():
    global threshold
    threshold = win.spinBox_threshold.value()
    pickle.dump(threshold, open(f"{path_depth}resource/variable/_threshold.pkl", "wb"))


win.spinBox_threshold.valueChanged.connect(f_threshold_change)


def f_register():
    # app.exit()
    # subprocess.Popen(["python", path_depth + "resource/view_controller/face_management_form/Controller.py"])
    # global cap
    # win.hide()
    # win.showMinimized()
    cap.release()
    os.system("python " + path_depth + "resource/view_controller/face_management_form/Controller.py")
    cap.open(0)
    # win.show()


win.pushButton_register.clicked.connect(f_register)


def f_query():
    # app.exit()
    # subprocess.Popen(["python", path_depth + "resource/view_controller/attendance_database_form/Controller.py"])
    # global cap
    # win.hide()
    cap.release()
    os.system("python " + path_depth + "resource/view_controller/attendance_database_form/Controller.py")
    cap.open(0)
    # win.show()


win.pushButton_query.clicked.connect(f_query)


def goto_telegram():
    # app.exit()
    # subprocess.Popen(["python", path_depth + "resource/view_controller/telegram_form/Controller.py"])
    # global cap
    # win.hide()
    cap.release()
    os.system("python " + path_depth + "resource/view_controller/telegram_form/Controller.py")
    cap.open(0)
    # win.show()


win.pushButton_telegram.clicked.connect(goto_telegram)


def f_update():
    try:
        headers = {"Accept": "application/vnd.github.v3.raw"}
        git_version_string = requests.get("https://api.github.com/repos/muysengly/repo_attendance_system_gtr/contents/resource/variable/_version.txt", headers=headers).text
        git_version_int = list(map(int, git_version_string.split(".")))

        if git_version_int > version_int:  # NOTE: 1.0.2 < 1.0.3 / 1.0.2 < 1.1.0 / 1.0.2 < 2.0.0
            reply = QMessageBox.question(win, "Update Available", f"Version {git_version_string} is available. \nDo you want to update?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:

                for _ in range(10):  # retry up to 10 times
                    response = requests.get("https://github.com/muysengly/repo_attendance_system_gtr/archive/refs/heads/main.zip", stream=True)
                    total_size = int(response.headers.get("content-length", 0))
                    if total_size > 0:
                        break

                if total_size > 0:
                    progress = QProgressDialog("Downloading update...", "Cancel", 0, 100, win)
                    progress.setWindowModality(Qt.WindowModal)
                    progress.setMinimumSize(400, 100)
                    progress.setWindowTitle("Update in progress")
                    progress.setValue(0)
                    downloaded = 0
                    with open(f"{path_depth}tmp.zip", "wb") as f:
                        for data in response.iter_content(1024):
                            if progress.wasCanceled():
                                response.close()
                                QMessageBox.warning(win, "Cancelled", "Update cancelled.")
                                return
                            f.write(data)
                            downloaded += len(data)
                            percent = int(downloaded * 100 / total_size)
                            progress.setValue(percent)
                    progress.setValue(100)

                    # extract the downloaded zip file
                    with zipfile.ZipFile(f"{path_depth}tmp.zip", "r") as zip_ref:
                        # TODO: unzip the file to the correct location
                        zip_ref.extractall(os.path.expanduser("~"))
                        os.remove(f"{path_depth}tmp.zip")

                    # show message box to inform the user
                    QMessageBox.information(win, "Update Complete", f"Updated to version {git_version_string}. \nPlease restart the application.")
                else:
                    QMessageBox.warning(win, "Download Error", "Failed to download the update. \nPlease try again later.")
        else:
            QMessageBox.information(win, "No Update", "You are already using the latest version.")

    except requests.RequestException as e:
        QMessageBox.critical(win, "Error", "No Internet Connection!")


win.pushButton_update.clicked.connect(f_update)

win.pushButton_update.deleteLater()


def f_close():
    global cap
    reply = QMessageBox.question(win, "Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        # cap.release()
        # win.close()
        app.quit()


win.pushButton_close.clicked.connect(f_close)


app.exec_()
app = None
cap.release()

