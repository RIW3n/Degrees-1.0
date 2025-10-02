from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os 
import sys 
import time 
import serial
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import numpy as np
import threading
import queue
import math
import cv2
# import requests
import numpy as np
from io import BytesIO
from PIL import Image
# port = input("enter com port number: ")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_shape = None
        self.x, self.y, self.t = 0, 0, 0
        self.running = True

        self.draw_thread = Thread(target=self.draw)
        self.draw_thread.start()

    def draw(self):
        while self.running:
            try:
                response = requests.get('http://192.168.4.1:5678/get_data')
                # response = requests.get('http://192.168.134.250:5678/get_data')

                if response.status_code == 200:
                    data = response.json()
                    self.x = data['x']
                    self.y = data['y']
                    self.t = data['t']
                    print(self.x, self.y, self.t)
                    self.update_plot()
                else:
                    print("No data available")

                time.sleep(0.1)
            except Exception as e:
                print(f"Error fetching data: {e}")

    def update_plot(self):
        if self.plot_shape:
            self.plot_shape.remove()
        self.plot_shape = plt.Rectangle((self.x, self.y), 50, 30, angle=np.degrees(self.t), color='blue')
        self.ax.add_patch(self.plot_shape)
        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.canvas.draw_idle()
        self.canvas.flush_events()





class PlotWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.plot_widget = MatplotlibWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.plot_widget)




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # self.serial = serial.Serial(f'COM{port}', 9600, timeout=1) 
        self.data = []
        self.fig, self.ax = plt.subplots()
        self.plot_shape = None
        self.start_plot = 0
        self.odom_values = []
        self.x, self.y, self.t = 0, 0, 0
        self.data_queue = queue.Queue()


        # self.server_url = "http://192.168.1.130:5678/video_feed"
        self.server_url = "http://192.168.4.1:5678/send_command"
        # self.server_url = "http://192.168.134.250:5678/send_command"


        self.session = requests.Session()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe UI Black") 
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        MainWindow.setFont(self.font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 630, 93, 28))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe UI Black")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.pushButton.setFont(self.font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 680, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 680, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(130, 730, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.dial = QtWidgets.QDial(self.centralwidget)
        self.dial.setGeometry(QtCore.QRect(360, 680, 131, 91))
        self.dial.setObjectName("dial")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(610, 620, 22, 160))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(870, 610, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(869, 609, 251, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_19 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_19.setStyleSheet("background-color: red")
        self.verticalLayout.addWidget(self.pushButton_19)
        self.pushButton_7 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.pushButton_7)
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout.addWidget(self.pushButton_6)
        # self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser_2.setGeometry(QtCore.QRect(100, 120, 451, 241))
        # self.textBrowser_2.setObjectName("textBrowser_2")
        self.plot_widget = MatplotlibWidget(self.centralwidget)
        self.plot_widget.setGeometry(QtCore.QRect(100, 120, 451, 241))
        self.plot_widget.setObjectName("plot_widget")
        #self.textBrowser_2.setStyleSheet("background-color: white;")

        self.viewfinder = QtWidgets.QLabel(self.centralwidget)
        self.viewfinder.setGeometry(QtCore.QRect(670, 120, 431, 241))
        self.viewfinder.setObjectName("viewfinder")
        self.viewfinder.show()

        # self.fetch_video_feed()
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 20, 201, 31))
        self.label.setObjectName("label")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(410, 430, 160, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(220, 380, 93, 28))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe UI Black")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.pushButton_8.setFont(self.font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(310, 430, 93, 28))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(130, 430, 93, 28))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(220, 480, 93, 28))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(840, 430, 93, 28))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(750, 480, 93, 28))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(660, 430, 93, 28))
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(940, 430, 160, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_15.setGeometry(QtCore.QRect(750, 380, 93, 28))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe UI Black")
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.pushButton_15.setFont(self.font)
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_16.setGeometry(QtCore.QRect(130, 80, 51, 31))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setGeometry(QtCore.QRect(1022, 80, 51, 31))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_18.setGeometry(QtCore.QRect(560, 300, 91, 31))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.pushButton_18.setFont(self.font)
        self.pushButton_18.setObjectName("pushButton_18")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 90, 131, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_2.setFont(self.font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(740, 90, 131, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_3.setFont(self.font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(590, 790, 131, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_4.setFont(self.font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(420, 460, 131, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_5.setFont(self.font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(950, 470, 131, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(10)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_6.setFont(self.font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(480, 560, 231, 21))
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe Print")
        self.font.setPointSize(12)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_7.setFont(self.font)
        self.label_7.setObjectName("label_7")
        self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_20.setGeometry(QtCore.QRect(250, 630, 41, 41))
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_21 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_21.setGeometry(QtCore.QRect(60, 630, 41, 41))
        self.pushButton_21.setObjectName("pushButton_21")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 34))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.centralwidget.setStyleSheet("background-color: pink;")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.continuous_execution)

        self.pushButton.pressed.connect(self.start_forward)
        self.pushButton.released.connect(self.stop_movement)

        self.pushButton_2.pressed.connect(self.start_left)
        self.pushButton_2.released.connect(self.stop_movement)

        self.pushButton_3.pressed.connect(self.start_right)
        self.pushButton_3.released.connect(self.stop_movement)

        self.pushButton_4.pressed.connect(self.start_back)
        self.pushButton_4.released.connect(self.stop_movement)
        
        self.pushButton_16.clicked.connect(self.print_M_maximized)
        self.pushButton_16.clicked.connect(self.start_plotting)
        self.pushButton_17.clicked.connect(self.print_C_maximized)

        self.pushButton_7.clicked.connect(self.toggle_manual_button)
        self.pushButton_5.clicked.connect(self.toggle_auto_button)
        self.pushButton_6.clicked.connect(self.toggle_replay_button)

        self.pushButton_8.clicked.connect(self.print_M_up)
        self.pushButton_9.clicked.connect(self.print_M_right)
        self.pushButton_10.clicked.connect(self.print_M_left)
        self.pushButton_11.clicked.connect(self.print_M_down)

        self.pushButton_12.clicked.connect(self.print_C_right)
        self.pushButton_13.clicked.connect(self.print_C_down)
        self.pushButton_14.clicked.connect(self.print_C_left)
        self.pushButton_15.clicked.connect(self.print_C_up)

        self.pushButton_20.pressed.connect(self.start_w)
        self.pushButton_20.released.connect(self.stop_movement)

        self.pushButton_21.pressed.connect(self.start_u)
        self.pushButton_21.released.connect(self.stop_movement)

        self.horizontalSlider.valueChanged.connect(self.M_slider_value_changed)
        self.horizontalSlider_2.valueChanged.connect(self.C_slider_value_changed)

        self.verticalSlider.valueChanged.connect(self.Speed_slider_value_changed)

        self.pushButton_18.clicked.connect(self.toggle_record_button)
        self.pushButton_19.clicked.connect(self.toggle_off_button)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "^"))
        self.pushButton_2.setText(_translate("MainWindow", "<"))
        self.pushButton_3.setText(_translate("MainWindow", ">"))
        self.pushButton_4.setText(_translate("MainWindow", "-"))
        self.pushButton_19.setText(_translate("MainWindow", "OFF"))
        self.pushButton_7.setText(_translate("MainWindow", "MANUAL"))
        self.pushButton_5.setText(_translate("MainWindow", "AUTO"))
        self.pushButton_6.setText(_translate("MainWindow", "REPLAY"))
        self.label.setText(_translate("MainWindow", "DEGREES 1.0 ROBOT"))
        self.pushButton_8.setText(_translate("MainWindow", "^"))
        self.pushButton_9.setText(_translate("MainWindow", ">"))
        self.pushButton_10.setText(_translate("MainWindow", "<"))
        self.pushButton_11.setText(_translate("MainWindow", "-"))
        self.pushButton_12.setText(_translate("MainWindow", ">"))
        self.pushButton_13.setText(_translate("MainWindow", "-"))
        self.pushButton_14.setText(_translate("MainWindow", "<"))
        self.pushButton_15.setText(_translate("MainWindow", "^"))
        self.pushButton_16.setText(_translate("MainWindow", "M"))
        self.pushButton_17.setText(_translate("MainWindow", "M"))
        self.pushButton_18.setText(_translate("MainWindow", "record"))
        self.label_2.setText(_translate("MainWindow", "Map View"))
        self.label_3.setText(_translate("MainWindow", "Camera View"))
        self.label_4.setText(_translate("MainWindow", "Speed"))
        self.label_5.setText(_translate("MainWindow", "Scale"))
        self.label_6.setText(_translate("MainWindow", "Zoom"))
        self.label_7.setText(_translate("MainWindow", "Navigation CONTROL"))
        self.pushButton_20.setText(_translate("MainWindow", "~"))
        self.pushButton_21.setText(_translate("MainWindow", "~"))


    def start_plotting(self):
        self.plot_widget.update_plot()



    def print_u(self):
        print("U")

    def print_w(self):
        print("W")

    def print_M_maximized(self):
        print("M-Maximized")

    def print_C_maximized(self):
        print("C-Maximized")

    def print_forw(self):
        print("F")

    def print_back(self):
        print("B")

    def print_left(self):
        print("L")

    def print_right(self):
        print("R")


    def print_M_up(self):
            print("M-U")

    def print_M_down(self):
        print("M-D")

    def print_M_left(self):
        print("M-L")

    def print_M_right(self):
        print("M-R")


    def print_C_up(self):
            print("C-U")

    def print_C_down(self):
        print("C-D")

    def print_C_left(self):
        print("C-L")

    def print_C_right(self):
        print("C-R")


    def M_slider_value_changed(self, value):
        print(f"Map Slider value changed: {value}")

    def C_slider_value_changed(self, value):
        print(f"Camera Slider value changed: {value}")
    
    def Speed_slider_value_changed(self, value):
        print(f"Speed value changed: {int(value *2.575)}")
       

    def print_record (self):
        print("Recording")

    def print_off (self):
        print("Disarmed")
        self.send_command('O')

    def print_manual(self):
        print("Manual Mode")
        self.send_command('M')


    def print_auto(self):
        print("Auto Mode")


    def print_replay(self):
        print("Replay")



    def toggle_record_button(self):
        current_style = self.pushButton_18.styleSheet()
        
        if 'background-color: red' in current_style:
            
            self.pushButton_18.setStyleSheet("")
        else:
            self.pushButton_18.setStyleSheet("background-color: red")
            self.print_record()

    def toggle_off_button(self):
        
        current_style = self.pushButton_19.styleSheet()
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setFont(self.font)
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setFont(self.font)
        self.pushButton_19.setStyleSheet("")
        self.pushButton_19.setFont(self.font)
        self.pushButton_5.setStyleSheet("")
        self.pushButton_5.setFont(self.font)
        
        if 'background-color: red' in current_style:
            
            self.pushButton_19.setStyleSheet("")
        else:
            self.pushButton_19.setStyleSheet("background-color: red")
            self.print_off()

    def toggle_manual_button(self):
        self.pushButton_7.setStyleSheet("background-color: red")
        self.pushButton_5.setStyleSheet("")
        self.pushButton_5.setFont(self.font)
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setFont(self.font)
        self.pushButton_19.setStyleSheet("")
        self.pushButton_19.setFont(self.font)
        self.print_manual()

    def toggle_auto_button(self):
        self.pushButton_5.setStyleSheet("background-color: red")
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setFont(self.font)
        self.pushButton_6.setStyleSheet("")
        self.pushButton_6.setFont(self.font)
        self.pushButton_19.setStyleSheet("")
        self.pushButton_19.setFont(self.font)
        self.print_auto()     

    def toggle_replay_button(self):
        self.pushButton_6.setStyleSheet("background-color: red")
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setFont(self.font)
        self.pushButton_5.setStyleSheet("") 
        self.pushButton_5.setFont(self.font)
        self.pushButton_19.setStyleSheet("")
        self.pushButton_19.setFont(self.font)
        self.print_replay()  

    def start_forward(self):
        print("Start Forward")
        self.send_command('F')
        self.timer.function_to_call = self.print_forw
        self.timer.start(100)

    def start_left(self):
        print("Start Left")
        self.send_command('L')
        self.timer.function_to_call = self.print_left
        self.timer.start(100)

    def start_right(self):
        print("Start Right")
        self.send_command('R')
        self.timer.function_to_call = self.print_right
        self.timer.start(100)

    def start_back(self):
        print("Start Backward")
        self.send_command('B')
        self.timer.function_to_call = self.print_back
        self.timer.start(100)

    def start_u(self):
        print("Start turning left")
        self.send_command('U')
        self.timer.function_to_call = self.print_u
        self.timer.start(100)

    def start_w(self):
        print("Start turning right")
        self.send_command('W')
        self.timer.function_to_call = self.print_w
        self.timer.start(100)

    def stop_movement(self):
        print("Stop Movement")
        self.send_command('S')  
        self.timer.stop()

    def continuous_execution(self):
        if hasattr(self.timer, 'function_to_call'):
            self.timer.function_to_call()

    def send_command(self, command):
        try:
            self.session.post(self.server_url, json={"command": command})
        except requests.exceptions.RequestException as e:
            print(f"Error sending command: {e}")


    def fetch_video_feed(self):
        self.video_url = 'http://192.168.4.1:5678/video_feed'
        # self.video_url = 'http://192.168.134.250:5678/video_feed' 

        self.cap = cv2.VideoCapture(self.video_url)
        self.frame_timer = QtCore.QTimer()
        self.frame_timer.timeout.connect(self.update_frame)
        self.frame_timer.start(50)  

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_img)
                self.viewfinder.setPixmap(pixmap)
                self.viewfinder.setScaledContents(True)
            else:
                print("Failed to read frame")
        else:
            print("VideoCapture not opened")

    def closeEvent(self, event):
        self.cap.release()
        self.session.close()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Windows")
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.setWindowTitle("Degr%%s")
    MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |QtCore.Qt.WindowCloseButtonHint)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # threading.Thread(target=ui.serial_communication).start()
    # threading.Thread(target=ui.draw).start() 
    sys.exit(app.exec_())
