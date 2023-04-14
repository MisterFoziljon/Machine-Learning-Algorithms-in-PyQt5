from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pandas as pd
from math import sqrt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.klass_label = QLabel(self)
        self.klass_label.setText("Class:")
        self.klass_label.setFont(QFont('Times New Roman', 14))
        self.klass_label.move(15,15)
        
        self.answer_label = QLabel(self)
        self.answer_label.setText("")
        self.answer_label.setFont(QFont('Times New Roman', 14))
        self.answer_label.move(15,15)

        self.klass_combo_box = QComboBox(self)
        self.klass_combo_box.move(15,15)

        self.proto_button = QPushButton('Prototip obyektlar', self)
        self.proto_button.move(10,10)
        self.proto_button.clicked.connect(self.prototip)

        self.table = QTableWidget(self)
        self.table.move(15,15)

        self.proto_table = QTableWidget(self)
        self.proto_table.move(15,15)

        self.object = QTableWidget(self)
        self.object.move(15,15)

        self.answer_table = QTableWidget(self)
        self.answer_table.move(15,15)
        
        self.answer_button = QPushButton('Aniqlash', self)
        self.answer_button.move(10,10)
        self.answer_button.clicked.connect(self.answer)
        
        self.file_button = QPushButton('Fayl yuklash', self)
        self.file_button.setFixedSize(200, 40)
        self.file_button.move(10,10)
        self.file_button.clicked.connect(self.load_data)
        self.file_button.setFont(QFont('Times New Roman', 12))       
        
        self.setWindowTitle('1-masala. Prototip obyektlar ichidagi eng yaqinini topish')
        
    def load_data(self):
        # --- Asosiy jadval --- #
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        if filename:
            file = pd.read_csv(filename)
            row,column = file.shape
            header = list(file.columns)
            
            self.table.setFixedHeight(850)
            self.table.setFixedWidth(685)
            self.table.setRowCount(row)
            self.table.setColumnCount(column)
            self.table.setHorizontalHeaderLabels(header)
            
            data = file.to_numpy().tolist()
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    cell = QTableWidgetItem(str(item))
                    self.table.setItem(i, j, cell)

            self.klass_label.move(100,930)
            self.klass_combo_box.addItems(header)
            self.klass_combo_box.setCurrentIndex(0)
            self.klass_combo_box.move(180,930)
            self.klass_combo_box.setFixedSize(200,30)
            self.klass_combo_box.setFont(QFont('Times New Roman', 12))
            self.proto_button.setFixedSize(200, 30)
            self.proto_button.setFont(QFont('Times New Roman', 12))
            self.proto_button.move(430,930)
            self.table.move(10,50)
    
    def prototip(self):
        # --- Prototip jadval --- #
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()
        
        data = []
        
        for row in range(self.table.rowCount()):
            rows=[]
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                rows.append(item.text())
            data.append(rows)

        columns=[]
        obj_rows = []
        for i in range(len(data[0])):
            columns.append(self.table.horizontalHeaderItem(i).text())
            if i!=class_column_index:
                obj_rows.append([self.table.horizontalHeaderItem(i).text(),""])
                
        data = pd.DataFrame(data,columns=columns)        
        classes = data.iloc[:,class_column_index].unique()
        classes_dict = {classes[i]:i for i in range(len(classes))}
        file = data.copy()
        file = file.replace(classes_dict)
        file = file.astype(float)
        mean_table = []
        columns.append("count")
        for i in range(len(classes)):
            count_classes = len(file[file[class_column_name]==i])
            row = list(file[file[class_column_name]==i].mean())
            row.append(count_classes)
            mean_table.append(row)

        for i in range(len(classes)):
            mean_table[i][class_column_index] = classes[int(mean_table[i][class_column_index])]
        
        self.proto_table.setFixedHeight(250)
        self.proto_table.setFixedWidth(775)
        self.proto_table.setRowCount(len(classes))
        self.proto_table.setColumnCount(len(mean_table[0]))
        self.proto_table.setHorizontalHeaderLabels(columns)
        self.proto_table.move(720,50)

        for i, row in enumerate(mean_table):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.proto_table.setItem(i, j, cell)

        self.object.setFixedHeight(200)
        self.object.setFixedWidth(275)
        self.object.setRowCount(len(obj_rows))
        self.object.setColumnCount(2)
        self.object.setHorizontalHeaderLabels(["Alomatlar","Qiymatlar"])
        
        for i, row in enumerate(obj_rows):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.object.setItem(i, j, cell)
        self.object.move(720,350)
        
        self.answer_button.setFixedSize(275, 30)
        self.answer_button.setFont(QFont('Times New Roman', 12))
        self.answer_button.move(720,560)

    def Evklid_distance(self,S1,S2):
        summa = 0
        for i in range(len(S1)):
            summa+=(S1[i]-S2[i])**2
        return sqrt(summa)
    
    def answer(self):
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()
        classes = []
        data = []
        for row in range(self.proto_table.rowCount()):
            rows=[]
            for column in range(self.proto_table.columnCount()-1):
                if column==class_column_index:
                    classes.append(self.proto_table.item(row, column).text())
                    continue
                item = self.proto_table.item(row, column)
                rows.append(float(item.text()))
            data.append(rows)
        
        obj = []
        for row in range(self.object.rowCount()):
            for column in range(self.object.columnCount()):
                item = self.object.item(row, column)
                if column==1:
                    obj.append(float(item.text()))
        
        evklid=[]
        for i in range(len(classes)):
            distance = self.Evklid_distance(data[i],obj)
            evklid.append(distance)

        index_min = min(range(len(evklid)), key=evklid.__getitem__)
        result = ["" for i in range(len(classes))]
        result[index_min]="+"

        ANSWER = []
        for i in range(len(classes)):
            ANSWER.append([classes[i],evklid[i],result[i]])
        self.answer_table.setFixedHeight(240)
        self.answer_table.setFixedWidth(495)
        self.answer_table.setRowCount(len(classes))
        self.answer_table.setColumnCount(3)
        self.answer_table.setHorizontalHeaderLabels(["Class nomi","Masofa","Tegishli"])
        self.answer_table.move(1000,350)
        
        for i, row in enumerate(ANSWER):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.answer_table.setItem(i, j, cell)

        text = "Kiritilgan nuqta "+classes[index_min]+" class ga tegishli"
        self.answer_label.setText(text)
        self.answer_label.move(720,800)
        self.answer_label.setGeometry(QRect(720,550, 800, 200))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1520,980)
    mainWindow.show()
    sys.exit(app.exec_())
