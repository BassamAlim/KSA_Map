# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mosaa\PycharmProjects\KSA_Map\Should_Be_The_Final_Version.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1282, 931)
        MainWindow.setMinimumSize(QtCore.QSize(1282, 931))
        MainWindow.setMaximumSize(QtCore.QSize(1282, 931))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Arabic, QtCore.QLocale.SaudiArabia))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 320, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.comboBox_Region_From = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Region_From.setGeometry(QtCore.QRect(110, 140, 111, 31))
        self.comboBox_Region_From.setObjectName("comboBox_Region_From")
        self.comboBox_City_From = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_City_From.setGeometry(QtCore.QRect(260, 140, 111, 31))
        self.comboBox_City_From.setObjectName("comboBox_City_From")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(510, 10, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(150, 430, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(550, 430, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(960, 430, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(180, 20, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1060, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.comboBox_City_To = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_City_To.setGeometry(QtCore.QRect(1060, 140, 111, 31))
        self.comboBox_City_To.setObjectName("comboBox_City_To")
        self.comboBox_Region_To = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Region_To.setGeometry(QtCore.QRect(910, 140, 111, 31))
        self.comboBox_Region_To.setObjectName("comboBox_Region_To")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(980, 20, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(910, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.BFS_Frame = QtWidgets.QFrame(self.centralwidget)
        self.BFS_Frame.setGeometry(QtCore.QRect(50, 480, 381, 311))
        self.BFS_Frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.BFS_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BFS_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BFS_Frame.setObjectName("BFS_Frame")
        self.Distance_lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Distance_lable_BFS.setGeometry(QtCore.QRect(0, 0, 131, 41))
        self.Distance_lable_BFS.setText("")
        self.Distance_lable_BFS.setObjectName("Distance_lable_BFS")
        self.Number_Of_Nodes_Lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Number_Of_Nodes_Lable_BFS.setGeometry(QtCore.QRect(0, 40, 131, 41))
        self.Number_Of_Nodes_Lable_BFS.setText("")
        self.Number_Of_Nodes_Lable_BFS.setObjectName("Number_Of_Nodes_Lable_BFS")
        self.Fringe_Max_Size_Lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Fringe_Max_Size_Lable_BFS.setGeometry(QtCore.QRect(0, 80, 131, 41))
        self.Fringe_Max_Size_Lable_BFS.setText("")
        self.Fringe_Max_Size_Lable_BFS.setObjectName("Fringe_Max_Size_Lable_BFS")
        self.Fringe_Max_Size_Result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Fringe_Max_Size_Result_BFS.setGeometry(QtCore.QRect(160, 80, 131, 41))
        self.Fringe_Max_Size_Result_BFS.setText("")
        self.Fringe_Max_Size_Result_BFS.setObjectName("Fringe_Max_Size_Result_BFS")
        self.Numbe_Of_Nodes_Result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Numbe_Of_Nodes_Result_BFS.setGeometry(QtCore.QRect(160, 40, 131, 41))
        self.Numbe_Of_Nodes_Result_BFS.setText("")
        self.Numbe_Of_Nodes_Result_BFS.setObjectName("Numbe_Of_Nodes_Result_BFS")
        self.Distannce_result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Distannce_result_BFS.setGeometry(QtCore.QRect(160, 0, 131, 41))
        self.Distannce_result_BFS.setText("")
        self.Distannce_result_BFS.setObjectName("Distannce_result_BFS")
        self.Route_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Route_BFS.setGeometry(QtCore.QRect(0, 130, 381, 181))
        self.Route_BFS.setText("")
        self.Route_BFS.setObjectName("Route_BFS")
        self.UCS_Frame = QtWidgets.QFrame(self.centralwidget)
        self.UCS_Frame.setGeometry(QtCore.QRect(450, 480, 381, 311))
        self.UCS_Frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.UCS_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UCS_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UCS_Frame.setObjectName("UCS_Frame")
        self.Distance_lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Distance_lable_UCS.setGeometry(QtCore.QRect(0, 0, 131, 41))
        self.Distance_lable_UCS.setText("")
        self.Distance_lable_UCS.setObjectName("Distance_lable_UCS")
        self.Number_Of_Nodes_Lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Number_Of_Nodes_Lable_UCS.setGeometry(QtCore.QRect(0, 40, 131, 41))
        self.Number_Of_Nodes_Lable_UCS.setText("")
        self.Number_Of_Nodes_Lable_UCS.setObjectName("Number_Of_Nodes_Lable_UCS")
        self.Fringe_Max_Size_Lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Fringe_Max_Size_Lable_UCS.setGeometry(QtCore.QRect(0, 80, 131, 41))
        self.Fringe_Max_Size_Lable_UCS.setText("")
        self.Fringe_Max_Size_Lable_UCS.setObjectName("Fringe_Max_Size_Lable_UCS")
        self.Fringe_Max_Size_Result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Fringe_Max_Size_Result_UCS.setGeometry(QtCore.QRect(160, 80, 131, 41))
        self.Fringe_Max_Size_Result_UCS.setText("")
        self.Fringe_Max_Size_Result_UCS.setObjectName("Fringe_Max_Size_Result_UCS")
        self.Numbe_Of_Nodes_Result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Numbe_Of_Nodes_Result_UCS.setGeometry(QtCore.QRect(160, 40, 131, 41))
        self.Numbe_Of_Nodes_Result_UCS.setText("")
        self.Numbe_Of_Nodes_Result_UCS.setObjectName("Numbe_Of_Nodes_Result_UCS")
        self.Distannce_result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Distannce_result_UCS.setGeometry(QtCore.QRect(160, 0, 131, 41))
        self.Distannce_result_UCS.setText("")
        self.Distannce_result_UCS.setObjectName("Distannce_result_UCS")
        self.Route_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Route_UCS.setGeometry(QtCore.QRect(0, 130, 381, 181))
        self.Route_UCS.setText("")
        self.Route_UCS.setObjectName("Route_UCS")
        self.BFS_Frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.BFS_Frame_3.setGeometry(QtCore.QRect(850, 480, 381, 311))
        self.BFS_Frame_3.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.BFS_Frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BFS_Frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BFS_Frame_3.setObjectName("BFS_Frame_3")
        self.Distance_lable_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Distance_lable_IDS.setGeometry(QtCore.QRect(0, 0, 131, 41))
        self.Distance_lable_IDS.setText("")
        self.Distance_lable_IDS.setObjectName("Distance_lable_IDS")
        self.Number_Of_Nodes_Lable_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Number_Of_Nodes_Lable_IDS.setGeometry(QtCore.QRect(0, 40, 131, 41))
        self.Number_Of_Nodes_Lable_IDS.setText("")
        self.Number_Of_Nodes_Lable_IDS.setObjectName("Number_Of_Nodes_Lable_IDS")
        self.Fringe_Max_Size_Lable_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Fringe_Max_Size_Lable_IDS.setGeometry(QtCore.QRect(0, 80, 131, 41))
        self.Fringe_Max_Size_Lable_IDS.setText("")
        self.Fringe_Max_Size_Lable_IDS.setObjectName("Fringe_Max_Size_Lable_IDS")
        self.Fringe_Max_Size_Result_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Fringe_Max_Size_Result_IDS.setGeometry(QtCore.QRect(160, 80, 131, 41))
        self.Fringe_Max_Size_Result_IDS.setText("")
        self.Fringe_Max_Size_Result_IDS.setObjectName("Fringe_Max_Size_Result_IDS")
        self.Numbe_Of_Nodes_Result_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Numbe_Of_Nodes_Result_IDS.setGeometry(QtCore.QRect(160, 40, 131, 41))
        self.Numbe_Of_Nodes_Result_IDS.setText("")
        self.Numbe_Of_Nodes_Result_IDS.setObjectName("Numbe_Of_Nodes_Result_IDS")
        self.Distannce_result_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Distannce_result_IDS.setGeometry(QtCore.QRect(160, 0, 131, 41))
        self.Distannce_result_IDS.setText("")
        self.Distannce_result_IDS.setObjectName("Distannce_result_IDS")
        self.Route_IDS = QtWidgets.QLabel(self.BFS_Frame_3)
        self.Route_IDS.setGeometry(QtCore.QRect(0, 130, 381, 181))
        self.Route_IDS.setText("")
        self.Route_IDS.setObjectName("Route_IDS")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1282, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "إبحث"))
        self.label.setText(_translate("MainWindow", "المنطقة"))
        self.label_2.setText(_translate("MainWindow", "المدينة"))
        self.label_3.setText(_translate("MainWindow", "أختر المنطقة و المدينة لحساب المسافة"))
        self.label_4.setText(_translate("MainWindow", "BFS"))
        self.label_5.setText(_translate("MainWindow", "UCS"))
        self.label_6.setText(_translate("MainWindow", "IDS"))
        self.label_7.setText(_translate("MainWindow", "من"))
        self.label_8.setText(_translate("MainWindow", "المدينة"))
        self.label_9.setText(_translate("MainWindow", "إلى"))
        self.label_10.setText(_translate("MainWindow", "المنطقة"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
