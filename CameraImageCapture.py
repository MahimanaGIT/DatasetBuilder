#!/usr/bin/env python3

import sys
import os

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

from glob import iglob
import cv2
import numpy as np

from UI_MainWindow import *

class CameraImageCapture(QWidget):
    # class constructor
    cam_index = 0

    database_url = "./data/images/"

    num_img = 0

    image = None

    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.get_start_num()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        self.ui.capture_bt.clicked.connect(self.capture)
        self.ui.capture_bt.setText("Unable to Capture, Please press Start")

    def get_start_num(self):
        print(list(map(os.path.basename,iglob(self.database_url+"*.jpg"))))
        print([os.path.basename(f) for f in  iglob(self.database_url+"*.jpg")])
        for f in  iglob(self.database_url+"*.jpg"):
            name = os.path.basename(f)
            if(str.__len__(name) == 9):
                num = int(name[:-4])
                if(num >= self.num_img):
                    self.num_img = num + 1

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, self.image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(self.cam_index)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")

            self.ui.capture_bt.setText("CAPTURE")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")

    def capture(self):
        if(np.shape(self.image)):
            number_str = str(self.num_img)
            self.num_img += 1
            zero_filled_number = number_str.zfill(5)
            cv2.imwrite(self.database_url+zero_filled_number+'.jpg', self.image)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    cameraImageCapture = CameraImageCapture()
    cameraImageCapture.show()

    sys.exit(app.exec_())