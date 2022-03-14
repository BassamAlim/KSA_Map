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


class UiMainWindow(object):
    def __init__(self):
        self.cost_greedy = None
        self.number_of_nodes_label_greedy = None
        self.fringe_max_size_label_greedy = None
        self.distance_result_greedy = None
        self.cost_result_greedy = None
        self.number_of_nodes_result_greedy = None
        self.fringe_max_size_result_greedy = None
        self.route_greedy = None
        self.distance_label_a_star = None
        self.cost_a_star = None
        self.number_of_nodes_label_a_star = None
        self.fringe_max_size_label_a_star = None
        self.distance_result_a_star = None
        self.cost_result_a_star = None
        self.number_of_nodes_result_a_star = None
        self.fringe_max_size_result_a_star = None
        self.route_a_star = None
        self.distance_label_greedy = None
        self.a_star_frame = None
        self.greedy_frame = None
        self.a_star_label = None
        self.greedy_label = None
        self.price_field = None
        self.price_label = None
        self.cost_result_bfs = None
        self.cost_result_ucs = None
        self.from_region_label = None
        self.from_city_label = None
        self.to_region_label = None
        self.to_city_label = None
        self.comboBox_region_from = None
        self.comboBox_city_from = None
        self.comboBox_region_to = None
        self.comboBox_city_to = None
        self.push_button = None
        self.bfs_label = None
        self.ucs_label = None
        self.ids_label = None
        self.bfs_frame = None
        self.ucs_frame = None
        self.ids_frame = None
        self.distance_label_bfs = None
        self.number_of_nodes_label_bfs = None
        self.fringe_max_size_label_bfs = None
        self.cost_bfs = None
        self.fringe_max_size_Result_bfs = None
        self.number_Of_Nodes_Result_bfs = None
        self.distance_result_bfs = None
        self.route_bfs = None
        self.distance_label_ucs = None
        self.number_of_nodes_label_ucs = None
        self.fringe_max_size_label_ucs = None
        self.cost_ucs = None
        self.number_of_nodes_result_ucs = None
        self.distance_result_ucs = None
        self.route_ucs = None
        self.distance_label_ids = None
        self.number_of_nodes_label_ids = None
        self.fringe_max_size_label_ids = None
        self.cost_ids = None
        self.fringe_max_size_result_ids = None
        self.number_of_nodes_result_ids = None
        self.distance_result_ids = None
        self.cost_result_ids = None
        self.route_ids = None
        self.to_label = None
        self.from_label = None
        self.title_label = None
        self.central_widget = None
        self.fringe_max_size_result_ucs = None

    def setupUi(self, GMainWindow):
        font = QtGui.QFont()
        
        GMainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Arabic, QtCore.QLocale.SaudiArabia))
        GMainWindow.setWindowTitle(_translate("MainWindow", "Distance Calculator"))
        
        self.central_widget = QtWidgets.QWidget(GMainWindow)
        GMainWindow.setCentralWidget(self.central_widget)
        
        self.title_label = QtWidgets.QLabel(self.central_widget)
        self.title_label.setGeometry(QtCore.QRect(330, 10, 1000, 60))
        self.title_label.setText(_translate("MainWindow", "اختر المنطقة و المدينة لحساب المسافة"))
        font.setPointSize(20)
        self.title_label.setFont(font)

        self.from_label = QtWidgets.QLabel(self.central_widget)
        self.from_label.setGeometry(QtCore.QRect(1400, 90, 120, 60))
        self.from_label.setText(_translate("MainWindow", "من"))
        font.setPointSize(18)
        self.from_label.setFont(font)
        self.from_label.setAlignment(QtCore.Qt.AlignCenter)

        self.to_label = QtWidgets.QLabel(self.central_widget)
        self.to_label.setGeometry(QtCore.QRect(440, 90, 120, 60))
        self.to_label.setText(_translate("MainWindow", "إلى"))
        self.to_label.setFont(font)
        self.to_label.setAlignment(QtCore.Qt.AlignCenter)

        self.from_region_label = QtWidgets.QLabel(self.central_widget)
        self.from_region_label.setGeometry(QtCore.QRect(1600, 170, 110, 50))
        self.from_region_label.setText(_translate("MainWindow", "المنطقة"))
        font.setPointSize(15)
        self.from_region_label.setFont(font)
        self.from_region_label.setAlignment(QtCore.Qt.AlignCenter)

        self.from_city_label = QtWidgets.QLabel(self.central_widget)
        self.from_city_label.setGeometry(QtCore.QRect(1200, 170, 110, 50))
        self.from_city_label.setText(_translate("MainWindow", "المدينة"))
        self.from_city_label.setFont(font)
        self.from_city_label.setAlignment(QtCore.Qt.AlignCenter)

        self.to_region_label = QtWidgets.QLabel(self.central_widget)
        self.to_region_label.setGeometry(QtCore.QRect(600, 170, 110, 50))
        self.to_region_label.setText(_translate("MainWindow", "المنطقة"))
        self.to_region_label.setFont(font)
        self.to_region_label.setAlignment(QtCore.Qt.AlignCenter)

        self.to_city_label = QtWidgets.QLabel(self.central_widget)
        self.to_city_label.setGeometry(QtCore.QRect(200, 170, 110, 50))
        self.to_city_label.setText(_translate("MainWindow", "المدينة"))
        self.to_city_label.setFont(font)
        self.to_city_label.setAlignment(QtCore.Qt.AlignCenter)

        self.comboBox_region_from = QtWidgets.QComboBox(self.central_widget)
        self.comboBox_region_from.setGeometry(QtCore.QRect(1500, 220, 300, 50))
        self.comboBox_region_from.setFont(font)
        self.comboBox_region_from.currentTextChanged.connect(self.start_region_changed)

        self.comboBox_city_from = QtWidgets.QComboBox(self.central_widget)
        self.comboBox_city_from.setGeometry(QtCore.QRect(1100, 220, 300, 50))
        self.comboBox_city_from.setFont(font)

        self.comboBox_region_to = QtWidgets.QComboBox(self.central_widget)
        self.comboBox_region_to.setGeometry(QtCore.QRect(520, 220, 300, 50))
        self.comboBox_region_to.setFont(font)
        self.comboBox_region_to.currentTextChanged.connect(self.destination_region_changed)

        self.comboBox_city_to = QtWidgets.QComboBox(self.central_widget)
        self.comboBox_city_to.setGeometry(QtCore.QRect(100, 220, 300, 50))
        self.comboBox_city_to.setFont(font)

        self.price_label = QtWidgets.QLabel(self.central_widget)
        self.price_label.setGeometry(QtCore.QRect(1620, 330, 150, 50))
        self.price_label.setText("سعر الوقود:")
        self.price_label.setFont(font)

        self.price_field = QtWidgets.QTextEdit(self.central_widget)
        self.price_field.setGeometry(QtCore.QRect(1400, 330, 200, 50))
        self.price_field.setFont(font)

        self.push_button = QtWidgets.QPushButton(self.central_widget)
        self.push_button.setGeometry(QtCore.QRect(850, 320, 250, 60))
        self.push_button.setText(_translate("MainWindow", "إبحث"))
        font.setPointSize(18)
        self.push_button.setFont(font)
        self.push_button.clicked.connect(self.on_click)

        self.bfs_label = QtWidgets.QLabel(self.central_widget)
        self.bfs_label.setGeometry(QtCore.QRect(150, 430, 160, 40))
        self.bfs_label.setText(_translate("MainWindow", "BFS"))
        font.setPointSize(16)
        self.bfs_label.setFont(font)
        self.bfs_label.setAlignment(QtCore.Qt.AlignCenter)

        self.ucs_label = QtWidgets.QLabel(self.central_widget)
        self.ucs_label.setGeometry(QtCore.QRect(520, 430, 160, 40))
        self.ucs_label.setText(_translate("MainWindow", "UCS"))
        self.ucs_label.setFont(font)
        self.ucs_label.setAlignment(QtCore.Qt.AlignCenter)

        self.ids_label = QtWidgets.QLabel(self.central_widget)
        self.ids_label.setGeometry(QtCore.QRect(920, 430, 100, 40))
        self.ids_label.setText(_translate("MainWindow", "IDS"))
        self.ids_label.setFont(font)
        self.ids_label.setAlignment(QtCore.Qt.AlignCenter)

        self.greedy_label = QtWidgets.QLabel(self.central_widget)
        self.greedy_label.setGeometry(QtCore.QRect(1270, 430, 100, 40))
        self.greedy_label.setText(_translate("MainWindow", "Greedy"))
        self.greedy_label.setFont(font)
        self.greedy_label.setAlignment(QtCore.Qt.AlignCenter)

        self.a_star_label = QtWidgets.QLabel(self.central_widget)
        self.a_star_label.setGeometry(QtCore.QRect(1650, 430, 100, 40))
        self.a_star_label.setText(_translate("MainWindow", "A*"))
        self.a_star_label.setFont(font)
        self.a_star_label.setAlignment(QtCore.Qt.AlignCenter)

        self.bfs_frame = QtWidgets.QFrame(self.central_widget)
        self.bfs_frame.setGeometry(QtCore.QRect(40, 480, 350, 450))
        self.bfs_frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.bfs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bfs_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.ucs_frame = QtWidgets.QFrame(self.central_widget)
        self.ucs_frame.setGeometry(QtCore.QRect(410, 480, 350, 450))
        self.ucs_frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.ucs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ucs_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.ids_frame = QtWidgets.QFrame(self.central_widget)
        self.ids_frame.setGeometry(QtCore.QRect(780, 480, 350, 450))
        self.ids_frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.ids_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ids_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.greedy_frame = QtWidgets.QFrame(self.central_widget)
        self.greedy_frame.setGeometry(QtCore.QRect(1150, 480, 350, 450))
        self.greedy_frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.greedy_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.greedy_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.a_star_frame = QtWidgets.QFrame(self.central_widget)
        self.a_star_frame.setGeometry(QtCore.QRect(1520, 480, 350, 450))
        self.a_star_frame.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.a_star_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.a_star_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.distance_label_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.distance_label_bfs.setGeometry(QtCore.QRect(20, 20, 130, 35))
        self.distance_label_bfs.setText("Distance:")
        font.setPointSize(14)
        self.distance_label_bfs.setFont(font)

        self.cost_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.cost_bfs.setGeometry(QtCore.QRect(20, 140, 200, 35))
        self.cost_bfs.setText("Cost:")
        self.cost_bfs.setFont(font)

        self.number_of_nodes_label_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.number_of_nodes_label_bfs.setGeometry(QtCore.QRect(20, 60, 230, 35))
        self.number_of_nodes_label_bfs.setText("Generated Nodes:")
        self.number_of_nodes_label_bfs.setFont(font)

        self.fringe_max_size_label_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.fringe_max_size_label_bfs.setGeometry(QtCore.QRect(20, 100, 250, 35))
        self.fringe_max_size_label_bfs.setText("Largest Fringe Size:")
        self.fringe_max_size_label_bfs.setFont(font)

        self.distance_result_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.distance_result_bfs.setGeometry(QtCore.QRect(280, 20, 80, 35))
        self.distance_result_bfs.setFont(font)

        self.cost_result_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.cost_result_bfs.setGeometry(QtCore.QRect(280, 140, 80, 35))
        self.cost_result_bfs.setFont(font)

        self.number_Of_Nodes_Result_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.number_Of_Nodes_Result_bfs.setGeometry(QtCore.QRect(280, 60, 80, 35))
        self.number_Of_Nodes_Result_bfs.setFont(font)

        self.fringe_max_size_Result_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.fringe_max_size_Result_bfs.setGeometry(QtCore.QRect(280, 100, 80, 35))
        self.fringe_max_size_Result_bfs.setFont(font)

        self.route_bfs = QtWidgets.QLabel(self.bfs_frame)
        self.route_bfs.setGeometry(QtCore.QRect(20, 170, 320, 250))
        self.route_bfs.setText("Route:")
        self.route_bfs.setFont(font)
        self.route_bfs.setWordWrap(True)

        self.distance_label_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.distance_label_ucs.setGeometry(QtCore.QRect(20, 20, 130, 35))
        self.distance_label_ucs.setText("Distance:")
        self.distance_label_ucs.setFont(font)

        self.cost_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.cost_ucs.setGeometry(QtCore.QRect(20, 140, 200, 35))
        self.cost_ucs.setText("Cost:")
        self.cost_ucs.setFont(font)

        self.number_of_nodes_label_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.number_of_nodes_label_ucs.setGeometry(QtCore.QRect(20, 60, 230, 35))
        self.number_of_nodes_label_ucs.setText("Generated Nodes:")
        self.number_of_nodes_label_ucs.setFont(font)

        self.fringe_max_size_label_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.fringe_max_size_label_ucs.setGeometry(QtCore.QRect(20, 100, 250, 35))
        self.fringe_max_size_label_ucs.setText("Largest Fringe Size:")
        self.fringe_max_size_label_ucs.setFont(font)

        self.distance_result_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.distance_result_ucs.setGeometry(QtCore.QRect(280, 20, 80, 35))
        self.distance_result_ucs.setFont(font)

        self.cost_result_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.cost_result_ucs.setGeometry(QtCore.QRect(280, 140, 80, 35))
        self.cost_result_ucs.setFont(font)

        self.number_of_nodes_result_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.number_of_nodes_result_ucs.setGeometry(QtCore.QRect(280, 60, 80, 35))
        self.number_of_nodes_result_ucs.setFont(font)

        self.fringe_max_size_result_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.fringe_max_size_result_ucs.setGeometry(QtCore.QRect(280, 100, 80, 35))
        self.fringe_max_size_result_ucs.setFont(font)

        self.route_ucs = QtWidgets.QLabel(self.ucs_frame)
        self.route_ucs.setGeometry(QtCore.QRect(20, 170, 320, 250))
        self.route_ucs.setText("Route:")
        self.route_ucs.setFont(font)
        self.route_ucs.setWordWrap(True)

        self.distance_label_ids = QtWidgets.QLabel(self.ids_frame)
        self.distance_label_ids.setGeometry(QtCore.QRect(20, 20, 130, 35))
        self.distance_label_ids.setText("Distance:")
        self.distance_label_ids.setFont(font)

        self.cost_ids = QtWidgets.QLabel(self.ids_frame)
        self.cost_ids.setGeometry(QtCore.QRect(20, 140, 200, 35))
        self.cost_ids.setText("Cost:")
        self.cost_ids.setFont(font)

        self.number_of_nodes_label_ids = QtWidgets.QLabel(self.ids_frame)
        self.number_of_nodes_label_ids.setGeometry(QtCore.QRect(20, 60, 230, 35))
        self.number_of_nodes_label_ids.setText("Generated Nodes:")
        self.number_of_nodes_label_ids.setFont(font)

        self.fringe_max_size_label_ids = QtWidgets.QLabel(self.ids_frame)
        self.fringe_max_size_label_ids.setGeometry(QtCore.QRect(20, 100, 250, 35))
        self.fringe_max_size_label_ids.setText("Largest Fringe Size:")
        self.fringe_max_size_label_ids.setFont(font)

        self.distance_result_ids = QtWidgets.QLabel(self.ids_frame)
        self.distance_result_ids.setGeometry(QtCore.QRect(280, 20, 80, 35))
        self.distance_result_ids.setFont(font)

        self.cost_result_ids = QtWidgets.QLabel(self.ids_frame)
        self.cost_result_ids.setGeometry(QtCore.QRect(280, 140, 80, 35))
        self.cost_result_ids.setFont(font)

        self.number_of_nodes_result_ids = QtWidgets.QLabel(self.ids_frame)
        self.number_of_nodes_result_ids.setGeometry(QtCore.QRect(280, 60, 80, 35))
        self.number_of_nodes_result_ids.setFont(font)

        self.fringe_max_size_result_ids = QtWidgets.QLabel(self.ids_frame)
        self.fringe_max_size_result_ids.setGeometry(QtCore.QRect(280, 100, 80, 35))
        self.fringe_max_size_result_ids.setFont(font)

        self.route_ids = QtWidgets.QLabel(self.ids_frame)
        self.route_ids.setGeometry(QtCore.QRect(20, 170, 320, 250))
        self.route_ids.setText("Route:")
        self.route_ids.setFont(font)
        self.route_ids.setWordWrap(True)

        self.distance_label_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.distance_label_greedy.setGeometry(QtCore.QRect(20, 20, 130, 35))
        self.distance_label_greedy.setText("Distance:")
        self.distance_label_greedy.setFont(font)

        self.cost_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.cost_greedy.setGeometry(QtCore.QRect(20, 140, 200, 35))
        self.cost_greedy.setText("Cost:")
        self.cost_greedy.setFont(font)

        self.number_of_nodes_label_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.number_of_nodes_label_greedy.setGeometry(QtCore.QRect(20, 60, 230, 35))
        self.number_of_nodes_label_greedy.setText("Generated Nodes:")
        self.number_of_nodes_label_greedy.setFont(font)

        self.fringe_max_size_label_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.fringe_max_size_label_greedy.setGeometry(QtCore.QRect(20, 100, 250, 35))
        self.fringe_max_size_label_greedy.setText("Largest Fringe Size:")
        self.fringe_max_size_label_greedy.setFont(font)

        self.distance_result_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.distance_result_greedy.setGeometry(QtCore.QRect(280, 20, 80, 35))
        self.distance_result_greedy.setFont(font)

        self.cost_result_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.cost_result_greedy.setGeometry(QtCore.QRect(280, 140, 80, 35))
        self.cost_result_greedy.setFont(font)

        self.number_of_nodes_result_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.number_of_nodes_result_greedy.setGeometry(QtCore.QRect(280, 60, 80, 35))
        self.number_of_nodes_result_greedy.setFont(font)

        self.fringe_max_size_result_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.fringe_max_size_result_greedy.setGeometry(QtCore.QRect(280, 100, 80, 35))
        self.fringe_max_size_result_greedy.setFont(font)

        self.route_greedy = QtWidgets.QLabel(self.greedy_frame)
        self.route_greedy.setGeometry(QtCore.QRect(20, 170, 320, 250))
        self.route_greedy.setText("Route:")
        self.route_greedy.setFont(font)
        self.route_greedy.setWordWrap(True)

        self.distance_label_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.distance_label_a_star.setGeometry(QtCore.QRect(20, 20, 130, 35))
        self.distance_label_a_star.setText("Distance:")
        self.distance_label_a_star.setFont(font)

        self.cost_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.cost_a_star.setGeometry(QtCore.QRect(20, 140, 200, 35))
        self.cost_a_star.setText("Cost:")
        self.cost_a_star.setFont(font)

        self.number_of_nodes_label_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.number_of_nodes_label_a_star.setGeometry(QtCore.QRect(20, 60, 230, 35))
        self.number_of_nodes_label_a_star.setText("Generated Nodes:")
        self.number_of_nodes_label_a_star.setFont(font)

        self.fringe_max_size_label_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.fringe_max_size_label_a_star.setGeometry(QtCore.QRect(20, 100, 250, 35))
        self.fringe_max_size_label_a_star.setText("Largest Fringe Size:")
        self.fringe_max_size_label_a_star.setFont(font)

        self.distance_result_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.distance_result_a_star.setGeometry(QtCore.QRect(280, 20, 80, 35))
        self.distance_result_a_star.setFont(font)

        self.cost_result_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.cost_result_a_star.setGeometry(QtCore.QRect(280, 140, 80, 35))
        self.cost_result_a_star.setFont(font)

        self.number_of_nodes_result_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.number_of_nodes_result_a_star.setGeometry(QtCore.QRect(280, 60, 80, 35))
        self.number_of_nodes_result_a_star.setFont(font)

        self.fringe_max_size_result_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.fringe_max_size_result_a_star.setGeometry(QtCore.QRect(280, 100, 80, 35))
        self.fringe_max_size_result_a_star.setFont(font)

        self.route_a_star = QtWidgets.QLabel(self.a_star_frame)
        self.route_a_star.setGeometry(QtCore.QRect(20, 170, 320, 250))
        self.route_a_star.setText("Route:")
        self.route_a_star.setFont(font)
        self.route_a_star.setWordWrap(True)

        self.fill_regions()
        QtCore.QMetaObject.connectSlotsByName(GMainWindow)

    def fill_regions(self):
        for region in regions:
            self.comboBox_region_from.addItem(_translate("MainWindow", region))
            self.comboBox_region_to.addItem(_translate("MainWindow", region))

    def on_click(self):
        start_city = get_index(self.comboBox_city_from.currentText())
        destination_city = get_index(self.comboBox_city_to.currentText())
        price = 2.18
        if len(self.price_field.toPlainText()) != 0:
            price = float(self.price_field.toPlainText())
        processor = process
        
        before = time.time()
        bfs_output = processor.bfs(start_city, destination_city)
        print("BFS: " + str(time.time()-before))
        if bfs_output[0] == 'success':
            self.show_bfs(bfs_output[1], price)
        
        before = time.time()
        ucs_output = processor.ucs(start_city, destination_city)
        print("UCS: " + str(time.time()-before))
        if ucs_output[0] == 'success':
            self.show_ucs(ucs_output[1], price)
        
        before = time.time()
        ids_output = processor.ids(start_city, destination_city)
        print("IDS: " + str(time.time()-before))
        if ids_output[0] == 'success':
            self.show_ids(ids_output[1], price)

        before = time.time()
        greedy_output = processor.greedy(start_city, destination_city)
        print("Greedy: " + str(time.time() - before))
        if greedy_output[0] == 'success':
            self.show_greedy(greedy_output[1], price)

        before = time.time()
        a_star_output = processor.a_star(start_city, destination_city)
        print("A*: " + str(time.time() - before))
        if a_star_output[0] == 'success':
            self.show_a_star(a_star_output[1], price)

    def start_region_changed(self):
        index = self.comboBox_region_from.currentIndex()
        self.comboBox_city_from.clear()
        for city in cities:
            if index == 0:
                self.comboBox_city_from.addItem(_translate("MainWindow", city['name']))
            elif city['rid'] == index - 1:
                self.comboBox_city_from.addItem(_translate("MainWindow", city['name']))

    def destination_region_changed(self):
        index = self.comboBox_region_to.currentIndex()
        self.comboBox_city_to.clear()
        for city in cities:
            if index == 0:
                self.comboBox_city_to.addItem(_translate("MainWindow", city['name']))
            elif city['rid'] == index - 1:
                self.comboBox_city_to.addItem(_translate("MainWindow", city['name']))

    def show_bfs(self, output, price):
        self.distance_result_bfs.setText(str(output.distance))
        self.cost_result_bfs.setText(str(int(output.distance * price)))
        self.number_Of_Nodes_Result_bfs.setText(str(output.nodes_num))
        self.fringe_max_size_Result_bfs.setText(str(output.fringe_max_size))
        self.route_bfs.setText(formulate_route(output.route))

    def show_ucs(self, output, price):
        self.distance_result_ucs.setText(str(output.distance))
        self.cost_result_ucs.setText(str(int(output.distance * price)))
        self.number_of_nodes_result_ucs.setText(str(output.nodes_num))
        self.fringe_max_size_result_ucs.setText(str(output.fringe_max_size))
        self.route_ucs.setText(formulate_route(output.route))

    def show_ids(self, output, price):
        self.distance_result_ids.setText(str(output.distance))
        self.cost_result_ids.setText(str(int(output.distance * price)))
        self.number_of_nodes_result_ids.setText(str(output.nodes_num))
        self.fringe_max_size_result_ids.setText(str(output.fringe_max_size))
        self.route_ids.setText(formulate_route(output.route))
        
    def show_greedy(self, output, price):
        self.distance_result_greedy.setText(str(output.distance))
        self.cost_result_greedy.setText(str(int(output.distance * price)))
        self.number_of_nodes_result_greedy.setText(str(output.nodes_num))
        self.fringe_max_size_result_greedy.setText(str(output.fringe_max_size))
        self.route_greedy.setText(formulate_route(output.route))
        
    def show_a_star(self, output, price):
        self.distance_result_a_star.setText(str(output.distance))
        self.cost_result_a_star.setText(str(int(output.distance * price)))
        self.number_of_nodes_result_a_star.setText(str(output.nodes_num))
        self.fringe_max_size_result_a_star.setText(str(output.fringe_max_size))
        self.route_a_star.setText(formulate_route(output.route))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
