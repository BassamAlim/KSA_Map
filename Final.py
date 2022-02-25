# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mosaa\PycharmProjects\KSA_Map\Should_Be_The_Final_Version.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import time

from PyQt5 import QtCore, QtGui, QtWidgets

import process

with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)

regions = ['جميع المناطق', 'منطقة الرياض', 'منطقة مكة المكرمة', 'منطقة المدينة المنورة', 'منطقة القصيم',
           'المنطقة الشرقية', 'منطقة ابها', 'منطقة تبوك', 'منطقة حائل', 'منطقة عرعر', 'منطقة جازان', 'منطقة نجران',
           'منطقة الباحة', 'منطقة سكاكا']

_translate = QtCore.QCoreApplication.translate


def formulate_route(route):
    string = str()
    for element in route:
        string += cities[element.cid]['name'] + ' -> '
    return string[:-3]


def get_index(name):
    for city in cities:
        if city['name'] == name:
            return city['cid']


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Arabic, QtCore.QLocale.SaudiArabia))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(630, 320, 250, 60))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.comboBox_Region_From = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Region_From.setGeometry(QtCore.QRect(100, 140, 220, 40))
        self.comboBox_Region_From.setObjectName("comboBox_Region_From")
        self.comboBox_Region_From.currentTextChanged.connect(self.start_region_changed)
        self.comboBox_City_From = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_City_From.setGeometry(QtCore.QRect(350, 140, 220, 40))
        self.comboBox_City_From.setObjectName("comboBox_City_From")
        self.from_region_label = QtWidgets.QLabel(self.centralwidget)
        self.from_region_label.setGeometry(QtCore.QRect(170, 90, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.from_region_label.setFont(font)
        self.from_region_label.setAlignment(QtCore.Qt.AlignCenter)
        self.from_region_label.setObjectName("label")
        self.from_city_label = QtWidgets.QLabel(self.centralwidget)
        self.from_city_label.setGeometry(QtCore.QRect(400, 90, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.from_city_label.setFont(font)
        self.from_city_label.setAlignment(QtCore.Qt.AlignCenter)
        self.from_city_label.setObjectName("label_2")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(500, 10, 440, 50))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setObjectName("label_3")
        self.bfs_label = QtWidgets.QLabel(self.centralwidget)
        self.bfs_label.setGeometry(QtCore.QRect(180, 430, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.bfs_label.setFont(font)
        self.bfs_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bfs_label.setObjectName("label_4")
        self.ucs_label = QtWidgets.QLabel(self.centralwidget)
        self.ucs_label.setGeometry(QtCore.QRect(680, 430, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ucs_label.setFont(font)
        self.ucs_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ucs_label.setObjectName("label_5")
        self.ids_label = QtWidgets.QLabel(self.centralwidget)
        self.ids_label.setGeometry(QtCore.QRect(1200, 430, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ids_label.setFont(font)
        self.ids_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ids_label.setObjectName("label_6")
        self.from_label = QtWidgets.QLabel(self.centralwidget)
        self.from_label.setGeometry(QtCore.QRect(280, 20, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.from_label.setFont(font)
        self.from_label.setAlignment(QtCore.Qt.AlignCenter)
        self.from_label.setObjectName("label_7")
        self.to_city_label = QtWidgets.QLabel(self.centralwidget)
        self.to_city_label.setGeometry(QtCore.QRect(1200, 90, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.to_city_label.setFont(font)
        self.to_city_label.setAlignment(QtCore.Qt.AlignCenter)
        self.to_city_label.setObjectName("label_8")
        self.comboBox_City_To = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_City_To.setGeometry(QtCore.QRect(1160, 140, 220, 40))
        self.comboBox_City_To.setObjectName("comboBox_City_To")
        self.comboBox_Region_To = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Region_To.setGeometry(QtCore.QRect(910, 140, 220, 40))
        self.comboBox_Region_To.setObjectName("comboBox_Region_To")
        self.comboBox_Region_To.currentTextChanged.connect(self.destination_region_changed)
        self.to_label = QtWidgets.QLabel(self.centralwidget)
        self.to_label.setGeometry(QtCore.QRect(1080, 20, 120, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.to_label.setFont(font)
        self.to_label.setAlignment(QtCore.Qt.AlignCenter)
        self.to_label.setObjectName("label_9")
        self.region_to_label = QtWidgets.QLabel(self.centralwidget)
        self.region_to_label.setGeometry(QtCore.QRect(970, 90, 111, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.region_to_label.setFont(font)
        self.region_to_label.setAlignment(QtCore.Qt.AlignCenter)
        self.region_to_label.setObjectName("label_10")
        self.BFS_Frame = QtWidgets.QFrame(self.centralwidget)
        self.BFS_Frame.setGeometry(QtCore.QRect(50, 480, 400, 311))
        self.BFS_Frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.BFS_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BFS_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BFS_Frame.setObjectName("BFS_Frame")
        self.Distance_lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Distance_lable_BFS.setGeometry(QtCore.QRect(30, 20, 100, 40))
        self.Distance_lable_BFS.setText("Distance:")
        self.Distance_lable_BFS.setObjectName("Distance_lable_BFS")
        self.Number_Of_Nodes_Lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Number_Of_Nodes_Lable_BFS.setGeometry(QtCore.QRect(30, 60, 150, 40))
        self.Number_Of_Nodes_Lable_BFS.setText("Generated Nodes:")
        self.Number_Of_Nodes_Lable_BFS.setObjectName("Number_Of_Nodes_Lable_BFS")
        self.Fringe_Max_Size_Lable_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Fringe_Max_Size_Lable_BFS.setGeometry(QtCore.QRect(30, 100, 200, 40))
        self.Fringe_Max_Size_Lable_BFS.setText("Largest Fringe Size:")
        self.Fringe_Max_Size_Lable_BFS.setObjectName("Fringe_Max_Size_Lable_BFS")
        self.Fringe_Max_Size_Result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Fringe_Max_Size_Result_BFS.setGeometry(QtCore.QRect(250, 100, 50, 40))
        self.Fringe_Max_Size_Result_BFS.setObjectName("Fringe_Max_Size_Result_BFS")
        self.Numbe_Of_Nodes_Result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Numbe_Of_Nodes_Result_BFS.setGeometry(QtCore.QRect(250, 60, 100, 40))
        self.Numbe_Of_Nodes_Result_BFS.setObjectName("Numbe_Of_Nodes_Result_BFS")
        self.Distannce_result_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Distannce_result_BFS.setGeometry(QtCore.QRect(250, 20, 50, 40))
        self.Distannce_result_BFS.setObjectName("Distannce_result_BFS")
        self.Route_BFS = QtWidgets.QLabel(self.BFS_Frame)
        self.Route_BFS.setGeometry(QtCore.QRect(30, 130, 350, 180))
        self.Route_BFS.setText("Route:")
        self.Route_BFS.setObjectName("Route_BFS")
        self.Route_BFS.setWordWrap(True)
        self.UCS_Frame = QtWidgets.QFrame(self.centralwidget)
        self.UCS_Frame.setGeometry(QtCore.QRect(550, 480, 400, 311))
        self.UCS_Frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.UCS_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UCS_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UCS_Frame.setObjectName("UCS_Frame")
        self.Distance_lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Distance_lable_UCS.setGeometry(QtCore.QRect(30, 20, 100, 40))
        self.Distance_lable_UCS.setText("Distance:")
        self.Distance_lable_UCS.setObjectName("Distance_lable_UCS")
        self.Number_Of_Nodes_Lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Number_Of_Nodes_Lable_UCS.setGeometry(QtCore.QRect(30, 60, 150, 40))
        self.Number_Of_Nodes_Lable_UCS.setText("Generated Nodes:")
        self.Number_Of_Nodes_Lable_UCS.setObjectName("Number_Of_Nodes_Lable_UCS")
        self.Fringe_Max_Size_Lable_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Fringe_Max_Size_Lable_UCS.setGeometry(QtCore.QRect(30, 100, 200, 40))
        self.Fringe_Max_Size_Lable_UCS.setText("Largest Fringe Size:")
        self.Fringe_Max_Size_Lable_UCS.setObjectName("Fringe_Max_Size_Lable_UCS")
        self.Fringe_Max_Size_Result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Fringe_Max_Size_Result_UCS.setGeometry(QtCore.QRect(250, 100, 50, 40))
        self.Fringe_Max_Size_Result_UCS.setObjectName("Fringe_Max_Size_Result_UCS")
        self.Numbe_Of_Nodes_Result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Numbe_Of_Nodes_Result_UCS.setGeometry(QtCore.QRect(250, 60, 100, 40))
        self.Numbe_Of_Nodes_Result_UCS.setObjectName("Numbe_Of_Nodes_Result_UCS")
        self.Distannce_result_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Distannce_result_UCS.setGeometry(QtCore.QRect(250, 20, 50, 40))
        self.Distannce_result_UCS.setObjectName("Distannce_result_UCS")
        self.Route_UCS = QtWidgets.QLabel(self.UCS_Frame)
        self.Route_UCS.setGeometry(QtCore.QRect(30, 130, 350, 180))
        self.Route_UCS.setText("Route:")
        self.Route_UCS.setObjectName("Route_UCS")
        self.Route_UCS.setWordWrap(True)
        self.IDS_Frame = QtWidgets.QFrame(self.centralwidget)
        self.IDS_Frame.setGeometry(QtCore.QRect(1050, 480, 400, 311))
        self.IDS_Frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.IDS_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.IDS_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.IDS_Frame.setObjectName("BFS_Frame_3")
        self.Distance_lable_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Distance_lable_IDS.setGeometry(QtCore.QRect(30, 20, 100, 40))
        self.Distance_lable_IDS.setText("Distance:")
        self.Distance_lable_IDS.setObjectName("Distance_lable_IDS")
        self.Number_Of_Nodes_Lable_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Number_Of_Nodes_Lable_IDS.setGeometry(QtCore.QRect(30, 60, 150, 40))
        self.Number_Of_Nodes_Lable_IDS.setText("Generated Nodes:")
        self.Number_Of_Nodes_Lable_IDS.setObjectName("Number_Of_Nodes_Lable_IDS")
        self.Fringe_Max_Size_Lable_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Fringe_Max_Size_Lable_IDS.setGeometry(QtCore.QRect(30, 100, 200, 40))
        self.Fringe_Max_Size_Lable_IDS.setText("Largest Fringe Size:")
        self.Fringe_Max_Size_Lable_IDS.setObjectName("Fringe_Max_Size_Lable_IDS")
        self.Fringe_Max_Size_Result_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Fringe_Max_Size_Result_IDS.setGeometry(QtCore.QRect(250, 100, 50, 40))
        self.Fringe_Max_Size_Result_IDS.setObjectName("Fringe_Max_Size_Result_IDS")
        self.Numbe_Of_Nodes_Result_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Numbe_Of_Nodes_Result_IDS.setGeometry(QtCore.QRect(250, 60, 100, 40))
        self.Numbe_Of_Nodes_Result_IDS.setObjectName("Numbe_Of_Nodes_Result_IDS")
        self.Distannce_result_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Distannce_result_IDS.setGeometry(QtCore.QRect(250, 20, 50, 40))
        self.Distannce_result_IDS.setObjectName("Distannce_result_IDS")
        self.Route_IDS = QtWidgets.QLabel(self.IDS_Frame)
        self.Route_IDS.setGeometry(QtCore.QRect(30, 130, 350, 180))
        self.Route_IDS.setText("Route:")
        self.Route_IDS.setObjectName("Route_IDS")
        self.Route_IDS.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1282, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Distance Calculator"))
        self.pushButton.setText(_translate("MainWindow", "إبحث"))
        self.pushButton.clicked.connect(self.on_click)
        self.from_region_label.setText(_translate("MainWindow", "المنطقة"))
        self.from_city_label.setText(_translate("MainWindow", "المدينة"))
        self.title_label.setText(_translate("MainWindow", "أختر المنطقة و المدينة لحساب المسافة"))
        self.bfs_label.setText(_translate("MainWindow", "BFS"))
        self.ucs_label.setText(_translate("MainWindow", "UCS"))
        self.ids_label.setText(_translate("MainWindow", "IDS"))
        self.from_label.setText(_translate("MainWindow", "من"))
        self.to_city_label.setText(_translate("MainWindow", "المدينة"))
        self.to_label.setText(_translate("MainWindow", "إلى"))
        self.region_to_label.setText(_translate("MainWindow", "المنطقة"))
        for region in regions:
            self.comboBox_Region_From.addItem(_translate("MainWindow", region))
            self.comboBox_Region_To.addItem(_translate("MainWindow", region))

    def on_click(self):
        start_city = get_index(self.comboBox_City_From.currentText())
        destination_city = get_index(self.comboBox_City_To.currentText())
        processor = process
        before = time.time()
        bfs_output = processor.bfs(start_city, destination_city)
        print("BFS: " + str(time.time()-before))
        if bfs_output[0] == 'success':
            self.show_bfs(bfs_output[1])
        before = time.time()
        ucs_output = processor.ucs(start_city, destination_city)
        print("UCS: " + str(time.time()-before))
        if ucs_output[0] == 'success':
            self.show_ucs(ucs_output[1])
        before = time.time()
        ids_output = processor.ids(start_city, destination_city)
        print("IDS: " + str(time.time()-before))
        if ids_output[0] == 'success':
            self.show_ids(ids_output[1])

    def start_region_changed(self):
        index = self.comboBox_Region_From.currentIndex()
        self.comboBox_City_From.clear()
        for city in cities:
            if index == 0:
                self.comboBox_City_From.addItem(_translate("MainWindow", city['name']))
            elif city['rid'] == index - 1:
                self.comboBox_City_From.addItem(_translate("MainWindow", city['name']))

    def destination_region_changed(self):
        index = self.comboBox_Region_To.currentIndex()
        self.comboBox_City_To.clear()
        for city in cities:
            if index == 0:
                self.comboBox_City_To.addItem(_translate("MainWindow", city['name']))
            elif city['rid'] == index - 1:
                self.comboBox_City_To.addItem(_translate("MainWindow", city['name']))

    def show_bfs(self, output):
        self.Route_BFS.setText(formulate_route(output.route))
        self.Distannce_result_BFS.setText(str(output.distance))
        self.Numbe_Of_Nodes_Result_BFS.setText(str(output.nodes_num))
        self.Fringe_Max_Size_Result_BFS.setText(str(output.fringe_max_size))

    def show_ucs(self, output):
        self.Route_UCS.setText(formulate_route(output.route))
        self.Distannce_result_UCS.setText(str(output.distance))
        self.Numbe_Of_Nodes_Result_UCS.setText(str(output.nodes_num))
        self.Fringe_Max_Size_Result_UCS.setText(str(output.fringe_max_size))

    def show_ids(self, output):
        self.Route_IDS.setText(formulate_route(output.route))
        self.Distannce_result_IDS.setText(str(output.distance))
        self.Numbe_Of_Nodes_Result_IDS.setText(str(output.nodes_num))
        self.Fringe_Max_Size_Result_IDS.setText(str(output.fringe_max_size))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
