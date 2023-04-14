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

        self.class_button = QPushButton('Classga ajratish', self)
        self.class_button.move(10,10)
        self.class_button.clicked.connect(self.classlar_jadvali)

        self.table = QTableWidget(self)
        self.table.move(15,15)

        self.class_table = QTableWidget(self)
        self.class_table.move(15,15)

        self.count_class = QTextEdit(self)
        self.count_class.move(15,15)

        self.information = QTextEdit(self)
        self.information.move(15,15)
        
        self.file_button = QPushButton('Fayl yuklash', self)
        self.file_button.setFixedSize(200, 40)
        self.file_button.move(10,10)
        self.file_button.clicked.connect(self.load_data)
        self.file_button.setFont(QFont('Times New Roman', 12))       
        
        self.setWindowTitle('4-masala. Klasterlash yordamida obyektlarni sinflarga ajratish')
        
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

            self.klass_label.move(15,930)
            self.klass_combo_box.addItems(header)
            self.klass_combo_box.setCurrentIndex(0)
            self.klass_combo_box.move(80,930)
            self.klass_combo_box.setFixedSize(170,30)
            self.klass_combo_box.setFont(QFont('Times New Roman', 12))
            self.count_class.setFontPointSize(12)
            self.count_class.setPlaceholderText("Classlar soni")
            self.count_class.setFixedSize(170,30)
            self.count_class.move(350,930)
            self.class_button.setFixedSize( 170, 30)
            self.class_button.setFont(QFont('Times New Roman', 12))
            self.class_button.move(515,930)
            self.table.move(10,50)

    def classlar_jadvali(self):
        # --- Ajratib olingan class obyektlari jadval --- #
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()

        self.information.setFixedHeight(850)
        self.information.setFixedWidth(475)
        self.information.move(710,50)
        
        data = []
        
        for row in range(self.table.rowCount()):
            rows=[]
            for column in range(self.table.columnCount()):
                if not column==class_column_index:
                    item = self.table.item(row, column)
                    rows.append(item.text())
            data.append(rows)
        
        columns=[]
        for i in range(self.table.columnCount()):
            if not i==class_column_index:
                columns.append(self.table.horizontalHeaderItem(i).text())

        columns.append('klass')

        for i in range(self.table.rowCount()):
            data[i].append('-')
        
        #data = pd.DataFrame(data,columns=columns)
        #data = data.to_numpy().tolist()

        markazlar_soni = int(self.count_class.toPlainText())
        markazlar = []
        class_num = 0
        while not len(markazlar)==markazlar_soni:
            index = random.randint(0,len(data)-1)
            if data[index] not in markazlar:
                data[index][-1] = class_num
                markazlar.append(data[index])
                class_num+=1
                
        all_points = ""
        for k in range(len(markazlar)):
            points = "Class"+str(k+1)+": ( "+str(markazlar[k][0])+" , "
            for r in range(1,len(markazlar[k])):
                points+=" , "+str(markazlar[k][r])
            points+=" )"
            all_points+=points+"\n"
        self.information.insertPlainText("Tanlab olingan markazlar:\n"+all_points+'\n')
        self.information.insertPlainText("__________________________________________________\n")
        
        TEMP=[]
        iteration = 0
        while True:
            iteration+=1
            TEMP = markazlar.copy()

            markaz = [[0 for i in range(len(data[0]))] for j in range(len(markazlar))]
            soni = [0 for i in range(len(markazlar))]
        
            for i in range(len(data)):
                data[i][-1] = self.tegishli(markazlar,data[i])

            for nuqta in data:
                for klas in range(len(markazlar)):
                    if nuqta[-1]==klas:
                        markaz[klas] = self.Sum(markaz[klas],nuqta,klas)
                        soni[klas]+=1
            
        
            for x in range(len(markazlar)):
                markazlar[x] = [round(son,6) for son in self.division(markaz[x],soni[x])]

            if TEMP==markazlar:
                break

            
            for_iter = "Iteratsiya №"+str(iteration)
            all_points = ""
            for k in range(len(markazlar)):
                points = "Class"+str(k+1)+": ( "+str(markazlar[k][0])              
                for r in range(1,len(markazlar[k])):
                    points+=" , "+str(markazlar[k][r])
                points+=" ) [soni: "+str(soni[k])+"]"
                all_points+=points+"\n"
            self.information.insertPlainText(for_iter+"\n"+all_points+'\r\n')

        
        self.class_table.setFixedHeight(850)
        self.class_table.setFixedWidth(685)
        self.class_table.setRowCount(len(data))
        self.class_table.setColumnCount(len(data[0]))
        self.class_table.setHorizontalHeaderLabels(columns)
        self.class_table.move(1200,50)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.class_table.setItem(i, j, cell)

    def Evklid(self,S1,S2):
        summa = 0
        for i in range(len(S1)-1):
            summa += (float(S1[i])-float(S2[i]))**2
        return sqrt(summa)

    def tegishli(self,markaz,nuqta):
        masofa = []
        for i in range(len(markaz)):
            masofa.append(self.Evklid(markaz[i],nuqta))
        
        return masofa.index(min(masofa))

    def Sum(self,S1,S2,klas):
        summa = []
        for i in range(len(S1)-1):
            summa.append(float(S1[i])+float(S2[i]))
        summa.append(klas)
        return summa

    def division(self,S1,mean):
        son = S1.copy()
        for i in range(len(son)-1):
            if i==len(son)-1:
                continue
            son[i]=float(son[i])/float(mean)
        return son

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1900,980)
    mainWindow.show()
    sys.exit(app.exec_())
