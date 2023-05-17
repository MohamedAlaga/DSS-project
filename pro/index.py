from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtMultimedia,QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import sys
import os
import numpy as np
import pandas as pd
import random

class MatplotlibWidget(Canvas):
    def __init__(self, parent=None, title='Title', xlabel='x label', ylabel='y label', dpi=100):
        super(MatplotlibWidget, self).__init__(Figure())
        self.setParent(parent)
        self.figure = Figure(dpi=dpi)
        self.canvas = Canvas(self.figure)
        self.theplot = self.figure.add_subplot(3,2,1)
        self.theplot.set_title(title)
        self.theplot.set_xlabel(xlabel)
        self.theplot.set_ylabel(ylabel)


    def plotDataPoints(self, x, y):
        self.theplot.plot(x, y)
        self.draw()

FORM_CLASS, _ = loadUiType("main.ui")


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self ,parent = None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tableDraw()
        self.initWidget()
        self.initWidget1()
        print(theta_1)
        self.preClick()
        self.video(".\\v1.mp4")
    def tableDraw(self):
        self.tableWidget.setHorizontalHeaderLabels(["ساعات المذاكرة", "الدرجه"])
        data = pd.read_csv('.\\dataset\\gpa_study_hours.csv')
        y = data['study_hours'].values
        x = data['gpa'].values
        self.tableWidget.setRowCount(len(data))
        for i in range(len(x)):
            pass
            newitem = QTableWidgetItem(str(x[i]))
            self.tableWidget.setItem(i, 1,newitem)
        for i in range(len(y)):
            pass
            newitem = QTableWidgetItem(str(y[i]))
            self.tableWidget.setItem(i, 0,newitem)
        ##self.tableWidget.setItem(item, 0, y)

    def initWidget(self,):
        self.mplwidget = MatplotlibWidget(self.widget_3)
        self.mplwidget.theplot.clear()
        data = pd.read_csv('.\\dataset\\gpa_study_hours.csv')
        x = data['study_hours'].values
        y = data['gpa'].values
        L_rate = 0.0001
        iterations = 250
        theta_1 = 0
        theta_0 = 0
        n = x.shape[0]
        losses = []
        for i in range(iterations):
            h_x = theta_0 + theta_1 * x

            # Keeping track of the error decrease
            mse = (1 / n) * np.sum((h_x - y) ** 2)
            losses.append(mse)

            # Derivatives
            d_theta0 = (2 / n) * np.sum(h_x - y)
            d_theta1 = (2 / n) * np.sum(x * (h_x - y))

            #     # Values update
            theta_1 = theta_1 - L_rate * d_theta1
            theta_0 = theta_0 - L_rate * d_theta0
        new_x = 9
        Prediction_Model = theta_0 + theta_1 * new_x
        x_line = np.linspace(0, 5, 70)
        y_line = theta_0 + theta_1 * x_line
        self.mplwidget.theplot.plot(losses)

    #--------------------------------------------------------lower-----------------------------------------------------#
    def initWidget1(self):
        self.mplwidget1 = MatplotlibWidget(self.widget_4)
        self.mplwidget1.theplot.clear()
        data = pd.read_csv('.\\dataset\\gpa_study_hours.csv')
        x = data['study_hours'].values
        y = data['gpa'].values
        L_rate = 0.0001
        iterations = 250
        global theta_1
        global theta_0
        theta_1 = 0
        theta_0 = 0
        n = x.shape[0]
        losses = []
        for i in range(iterations):
            h_x = theta_0 + theta_1 * x

            # Keeping track of the error decrease
            mse = (1 / n) * np.sum((h_x - y) ** 2)
            losses.append(mse)

            # Derivatives
            d_theta0 = (2 / n) * np.sum(h_x - y)
            d_theta1 = (2 / n) * np.sum(x * (h_x - y))

            #     # Values update
            theta_1 = theta_1 - L_rate * d_theta1
            theta_0 = theta_0 - L_rate * d_theta0
        new_x = 600
        Prediction_Model = theta_0 + theta_1 * new_x
        print('Score:', Prediction_Model)
        x_line = np.linspace(0, 50, 50)
        y_line = theta_0 + theta_1 * x_line
        self.mplwidget1.theplot.plot(x_line, y_line, c='r')
        self.mplwidget1.theplot.scatter(x, y, s=10)

    def preClick(self):
        self.pushButton_4.clicked.connect(self.pre)

    def pre(self):
        if(self.lineEdit.text() != "") :
            x = float(self.lineEdit.text())
            print(type(theta_1))
            y = float(theta_0) + float(theta_1)*x
            print (y)
            self.tabWidget.setCurrentIndex(1)

            if(y < 2):
               self.lineEdit_2.setText(str(round(y, 3)))
               x=['.\\vid\\v1.mp4','.\\vid\\v2.mp4','.\\vid\\v3.mp4','.\\vid\\v4.mp4','.\\vid\\v5.mp4','.\\vid\\v6.mp4']
               self.lineEdit_3.setText("صيف")
               self.video(x[random.randint(0,len(x))],state=True)

            else:
                self.lineEdit_2.setText(str(round(y, 3)))
                if (y > 5):
                    y = 5
                    self.lineEdit_2.setText(str(round(y, 3)))
                x = ['.\\vid\\v7.mp4', '.\\vid\\v8.mp4', '.\\vid\\v9.mp4', '.\\vid\\v10.mp4', '.\\vid\\v11.mp4']
                self.lineEdit_3.setText("صافي")
                self.video(x[random.randint(0, len(x))], state=True)


    def video(self,name= 'name',state = False):
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        file = os.path.join(os.path.dirname(__file__), name)
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file)))
        self.player.setVideoOutput(self.widget)
        self.player.play()
        if(state == False):
            self.player.setMuted(True)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()