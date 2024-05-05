import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import threading
import queue
import serial
import time
from PyQt5 import QtCore, QtGui, QtWidgets

data = []
plot_shape = None
start_plot = 0

ser = serial.Serial('COM5', 9600)
odom_values = []
x, y, t = 0, 0, 0
data_queue = queue.Queue()

def serial_communication():
    global x, y, t
    try:
        while True:
            odom = ser.readline().decode('latin1').strip()
            try:
                tempo = odom.split(",")
                x = float(tempo[0])
                y = float(tempo[1])
                t = float(tempo[2])
                data_queue.put((x, y, t))
                print(x, y, t)
            except ValueError:
                print("Invalid odom value received")
    except KeyboardInterrupt:
        ser.close()

threading.Thread(target=serial_communication).start()

def draw():
    global plot_shape
    global x, y, t
    while True:
        try:
            if plot_shape:
                plot_shape.remove()
            plot_shape = plt.Rectangle((x, y), 50, 30, angle=np.degrees(t), color='blue')
            ax.add_patch(plot_shape)
            ax.set_xlim(-200, 200)
            ax.set_ylim(-200, 200)
            plt.draw()
            time.sleep(0.1)
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
        except queue.Empty:
            pass

app = QApplication(sys.argv)
window = QMainWindow()
central_widget = QWidget()
window.setGeometry((QtCore.QRect(870, 610, 256, 192)))
window.setCentralWidget(central_widget)
layout = QVBoxLayout(central_widget)

fig, ax = plt.subplots()
canvas = FigureCanvas(fig)
layout.addWidget(canvas)

threading.Thread(target=draw).start()

window.show()
sys.exit(app.exec_())
