# -*- coding: utf-8 -*- 
  
# ==============================
# @author: Joycat
# @time: 2024/04/28
# ==============================

###########################################################################
##
## PLEASE DO *NOT* EDIT THIS FILE!
##
###########################################################################
## RUN Main Functions
###########################################################################
from PyQt6.QtWidgets import QApplication
import myFrameWindow

if __name__ == '__main__':
    app = QApplication([])  
    window = myFrameWindow.ButtonEvents_MainWindow()
    window.show()  
    app.exec()
