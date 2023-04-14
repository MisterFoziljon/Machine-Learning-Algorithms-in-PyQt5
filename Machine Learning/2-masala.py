from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pandas as pd
from math import sqrt
import random
import tqdm
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.klass_label = QLabel(self)
        self.klass_label.setText("Class:")
        self.klass_label.setFont(QFont('Times New Roman', 14))
        self.klass_label.move(15,15)
        
        self.klass_combo_box = QComboBox(self)
        self.klass_combo_box.move(15,15)

        self.class_button = QPushButton('Ajratib olish', self)
        self.class_button.move(10,10)
        self.class_button.clicked.connect(self.classlar_jadvali)

        self.qobiq_button = QPushButton('Qobiq obyektlar', self)
        self.qobiq_button.move(10,10)
        self.qobiq_button.clicked.connect(self.qobiq_obyektlar)

        self.table = QTableWidget(self)
        self.table.move(15,15)

        self.class_table = QTableWidget(self)
        self.class_table.move(15,15)

        self.qobiq_table = QTableWidget(self)
        self.qobiq_table.move(15,15)

        self.qobiq = QTableWidget(self)
        self.qobiq.move(15,15)

        self.file_button = QPushButton('Fayl yuklash', self)
        self.file_button.setFixedSize(200, 40)
        self.file_button.move(10,10)
        self.file_button.clicked.connect(self.load_data)
        self.file_button.setFont(QFont('Times New Roman', 12))       
        
        self.setWindowTitle('2-masala. Qobiq obyektlarni aniqlash')
        
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

    def classlar_jadvali(self):
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
        for i in range(len(data[0])):
            columns.append(self.table.horizontalHeaderItem(i).text())
                
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
        
        self.class_table.setFixedHeight(550)
        self.class_table.setFixedWidth(685)
        self.class_table.setRowCount(len(data))
        self.class_table.setColumnCount(len(data[0]))
        self.class_table.setHorizontalHeaderLabels(columns)
        self.class_table.move(710,50)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.class_table.setItem(i, j, cell)

        self.qobiq_button.setFixedSize(200, 30)
        self.qobiq_button.setFont(QFont('Times New Roman', 12))
        self.qobiq_button.move(940,610)

    def Evklid(self,S1,S2,index):
        summa = 0
        for i in range(len(S1)):
            if i==index:
                continue
            summa+=(float(S1[i])-float(S2[i]))**2
        return sqrt(summa)

    def nearest_point(self,data,class_index):
        klass = data[0][0][class_index]
        ind = 0
        for index in range(len(data)):
            if not data[index][1][class_index]==klass:
                ind = index
                break
        objects = []
        for index in range(ind):
            objects.append([data[ind][1],data[index][1],self.Evklid(data[ind][1],data[index][1],class_index)])
        objects = pd.DataFrame(objects,columns=["S1","S2","distance"])
        objects = objects.sort_values('distance').values.tolist()
        return objects[0][1]
    
    def qobiq_obyektlar(self):
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()
        
        data = []
        for row in range(self.class_table.rowCount()):
            rows=[]
            for column in range(self.class_table.columnCount()):
                item = self.class_table.item(row, column)
                rows.append(item.text())
            data.append(rows)
        
        columns=[]
        for i in range(len(data[0])):
            columns.append(self.class_table.horizontalHeaderItem(i).text())

        data = pd.DataFrame(data,columns=columns)
        classes = data.iloc[:,class_column_index].unique()
        
        data = data.to_numpy().tolist()
        
        qobiqlar = []
        
        for i in tqdm.tqdm(range(len(data))):
            rows = []
            for j in range(len(data)):
                #print([data[i],data[j],self.Evklid(data[i],data[j],class_column_index)])
        
                rows.append([data[i],data[j],self.Evklid(data[i],data[j],class_column_index)])
                   
            rows = pd.DataFrame(rows,columns=["group1","group2","distance"])
            rows = rows.sort_values('distance').values.tolist()
        
            qobiqlar.append(self.nearest_point(rows,class_column_index))

        qobiqlar = pd.DataFrame(qobiqlar,columns=columns)
        qobiqlar = qobiqlar.drop_duplicates()
        qobiqlar = qobiqlar.to_numpy().tolist()
        
        self.qobiq_table.setFixedHeight(310)
        self.qobiq_table.setFixedWidth(685)
        self.qobiq_table.setRowCount(len(qobiqlar))
        self.qobiq_table.setColumnCount(len(columns))
        self.qobiq_table.setHorizontalHeaderLabels(columns)
        self.qobiq_table.move(710,650)
        
        for i, row in enumerate(qobiqlar):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.qobiq_table.setItem(i, j, cell)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1410,980)
    mainWindow.show()
    sys.exit(app.exec_())
