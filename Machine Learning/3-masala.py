from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pandas as pd
from math import sqrt
import random
import numpy as np
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

        self.class_button = QPushButton('Ajratib olish', self)
        self.class_button.move(10,10)
        self.class_button.clicked.connect(self.prototip)

        self.table = QTableWidget(self)
        self.table.move(15,15)

        self.class_table = QTableWidget(self)
        self.class_table.move(15,15)

        self.object = QTableWidget(self)
        self.object.move(15,15)

        self.neighbours_table = QTableWidget(self)
        self.neighbours_table.move(15,15)
        
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
            self.class_button.setFixedSize(200, 30)
            self.class_button.setFont(QFont('Times New Roman', 12))
            self.class_button.move(430,930)
            self.table.move(10,50)
    
    def prototip(self):
        # --- Ajratib olingan class obyektlari jadval --- #
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
        obj_rows.append("K")
        data = pd.DataFrame(data,columns=columns)        
        classes = data.iloc[:,class_column_index].unique()
        
        selected_classes = []

        while not len(selected_classes)==2:
            rand = random.randint(0,len(classes)-1)
            if classes[rand] not in selected_classes:
                selected_classes.append(classes[rand])
        
        first = data[data[class_column_name]==selected_classes[0]]
        second = data[data[class_column_name]==selected_classes[1]]
        data = pd.concat([first,second],ignore_index=True)
        data = data.to_numpy().tolist()

        self.class_table.setFixedHeight(450)
        self.class_table.setFixedWidth(685)
        self.class_table.setRowCount(len(data))
        self.class_table.setColumnCount(len(data[0]))
        self.class_table.setHorizontalHeaderLabels(columns)
        self.class_table.move(710,50)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.class_table.setItem(i, j, cell)
                
        self.object.setFixedHeight(220)
        self.object.setFixedWidth(275)
        self.object.setRowCount(len(obj_rows))
        self.object.setColumnCount(2)
        self.object.setHorizontalHeaderLabels(["Alomatlar","Qiymatlar"])
        
        for i, row in enumerate(obj_rows):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.object.setItem(i, j, cell)
        self.object.move(710,540)
        
        self.answer_button.setFixedSize(275, 30)
        self.answer_button.setFont(QFont('Times New Roman', 12))
        self.answer_button.move(710,770)

    def Normalization(self,maximum,minimum,son):
        return (son-minimum)/(maximum-minimum)
    
    def Evklid_distance_with_norm(self,S1,S2,maximum,minimum):
        S1 = np.array(S1)
        S2 = np.array(S2)
        #print(S1,S2)
        S1 = self.Normalization(maximum,minimum,S1)
        S2 = self.Normalization(maximum,minimum,S2)
        print("Normal: ",S1,S2)
        summa = 0
        for i in range(len(S1)):
            summa+=(S1[i]-S2[i])**2
        return sqrt(summa)

    def Evklid_distance_without_norm(self,S1,S2):
        summa = 0
        for i in range(len(S1)):
            summa+=(S1[i]-S2[i])**2
        return sqrt(summa)

    def Max_Min(self,data,obj):        
        normal = np.array(data).T
        normal = normal.tolist()
        
        for i in range(len(normal)):
            normal[i].append(obj[i])
            
        normal = np.array(normal)
        
        max_num = np.max(normal, axis=1)
        min_num = np.min(normal, axis=1)
        
        return np.array(max_num),np.array(min_num)
        
    def answer(self):
        
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()
        classes = []
        data = []
        for row in range(self.class_table.rowCount()):
            rows=[]
            for column in range(self.class_table.columnCount()):
                if column==class_column_index:
                    classes.append(self.class_table.item(row, column).text())
                    continue
                item = self.class_table.item(row, column)
                rows.append(float(item.text()))
            data.append(rows)

        obj = []
        K=0
        for row in range(self.object.rowCount()):
            for column in range(self.object.columnCount()):
                item = self.object.item(row, column)
                if column==1:
                    obj.append(float(item.text()))
        
        K=int(obj.pop(-1))
        max_num,min_num = self.Max_Min(data,obj)
        print(max_num,min_num)
        evklid=[]
        for i in range(len(data)):
            print("Haqiqiy:",data[i],obj)
            distance = [i,self.Evklid_distance_with_norm(data[i],obj,max_num,min_num)]
            #distance = [i,self.Evklid_distance_without_norm(data[i],obj)]
            evklid.append(distance)

        evklid = pd.DataFrame(evklid,columns=['data','distance'])
        evklid = evklid.sort_values('distance').to_numpy().tolist()

        matrix = []
        for i in range(self.class_table.rowCount()):
            row=[]
            for j in range(self.class_table.columnCount()+1):
                if j==self.class_table.columnCount():
                    row.append(evklid[i][1])
                else:
                    item = self.class_table.item(int(evklid[i][0]), j).text()
                    row.append(item)
            matrix.append(row)
        columns=[]
        for i in range(len(data[0])+1):
            columns.append(self.table.horizontalHeaderItem(i).text())
        columns.append('distance')
        
        self.neighbours_table.setFixedHeight(260)
        self.neighbours_table.setFixedWidth(495)
        self.neighbours_table.setRowCount(K)
        self.neighbours_table.setColumnCount(len(columns))
        self.neighbours_table.setHorizontalHeaderLabels(columns)
        self.neighbours_table.move(1000,540)
        
        for i, row in enumerate(matrix[:K]):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.neighbours_table.setItem(i, j, cell)
        classes = [matrix[i][class_column_index] for i in range(K)]
        class_name = list(set(classes))
        
        count_classes = []
        for i in range(len(class_name)):
            count_classes.append([class_name[i],classes.count(class_name[i])])
        print(count_classes)

        max_son = count_classes[0][1]
        name_class = count_classes[0][0]

        for i in range(1,len(class_name)):
            if max_son<count_classes[i][1]:
                max_son = count_classes[i][1]
                name_class = count_classes[i][0]
        text = "Kiritilgan nuqta "+name_class+" class ga tegishli"
        self.answer_label.setText(text)
        self.answer_label.setGeometry(QRect(1000,800, 800, 200))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1520,980)
    mainWindow.show()
    sys.exit(app.exec_())
