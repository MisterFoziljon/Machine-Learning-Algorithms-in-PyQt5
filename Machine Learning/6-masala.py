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
        self.klass_combo_box.currentTextChanged.connect(self.klasslarni_chiqarish)

        self.proto_button = QPushButton('Tanlangan classlar', self)
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

        self.combo_table = QTableWidget(self)
        self.combo_table.move(15,15)

        self.information = QTextEdit(self)
        self.information.move(15,15)
        
        self.answer_button = QPushButton('Aniqlash', self)
        self.answer_button.move(10,10)
        self.answer_button.clicked.connect(self.answer)
        
        self.file_button = QPushButton('Fayl yuklash', self)
        self.file_button.setFixedSize(200, 40)
        self.file_button.move(10,10)
        self.file_button.clicked.connect(self.load_data)
        self.file_button.setFont(QFont('Times New Roman', 12))       
        
        self.setWindowTitle('6-masala. Nomi esimda yo')

    def load_data(self):
        # --- Asosiy jadval --- #
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)")
        if filename:
            file = pd.read_csv(filename)
            row,column = file.shape
            header = list(file.columns)
            
            self.table.setFixedHeight(550)
            self.table.setFixedWidth(685)
            self.table.setRowCount(row)
            self.table.setColumnCount(column)
            self.table.setHorizontalHeaderLabels(header)
            
            data = file.to_numpy().tolist()
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    cell = QTableWidgetItem(str(item))
                    self.table.setItem(i, j, cell)

            self.klass_label.move(200,620)
            self.klass_combo_box.addItems(header)
            self.klass_combo_box.setCurrentIndex(len(file.columns)-1)
            self.klass_combo_box.move(300,620)
            self.klass_combo_box.setFixedSize(200,30)
            self.klass_combo_box.setFont(QFont('Times New Roman', 12))
            self.proto_button.setFixedSize(200, 30)
            self.proto_button.setFont(QFont('Times New Roman', 12))
            self.proto_button.move(230,930)
            self.table.move(10,50)

    def klasslarni_chiqarish(self,class_name):
        
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

        classes = data[class_name].unique()
        self.combo_table.setFixedHeight(250)
        self.combo_table.setFixedWidth(685)
        self.combo_table.setRowCount(len(classes))
        self.combo_table.setColumnCount(2)
        self.combo_table.setHorizontalHeaderLabels(["Class nomi","Index"])
        self.combo_table.move(10,670)
        
        class_data = [[classes[i],""] for i in range(len(classes))]
        for i, row in enumerate(class_data):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.combo_table.setItem(i, j, cell)
    
    def prototip(self):
        # --- Ajratib olingan klasslar jadval --- #
        new_class = []
        for row in range(self.combo_table.rowCount()):
            rows=[]
            for column in range(self.combo_table.columnCount()):
                item = self.combo_table.item(row, column)
                rows.append(item.text())
            new_class.append(rows)

        class1_id = []
        class2_id = []
        
        for i in range(self.combo_table.rowCount()):
            if new_class[i][1]=="+":
                class1_id.append(new_class[i][0])
            elif new_class[i][1]=="-":
                class2_id.append(new_class[i][0])
                
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
        
        data1 = data.loc[data[class_column_name].isin(class1_id)]
        data2 = data.loc[data[class_column_name].isin(class2_id)]
        

        data1[class_column_name] = 1
        data2[class_column_name] = 2
        
        data = pd.concat([data1,data2],ignore_index=True)
        data = data.values.tolist()
        
        self.proto_table.setFixedHeight(400)
        self.proto_table.setFixedWidth(775)
        self.proto_table.setRowCount(len(data))
        self.proto_table.setColumnCount(len(columns))
        self.proto_table.setHorizontalHeaderLabels(columns)
        self.proto_table.move(720,50)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                cell = QTableWidgetItem(str(item))
                self.proto_table.setItem(i, j, cell)
              
        self.answer_button.setFixedSize(275, 30)
        self.answer_button.setFont(QFont('Times New Roman', 12))
        self.answer_button.move(950,460)
    
    def answer(self):
        self.information.setFixedHeight(450)
        self.information.setFixedWidth(775)
        self.information.move(720,500)
        self.information.setFont(QFont('Times New Roman', 12))
        class_column_name = self.klass_combo_box.currentText()
        class_column_index = self.klass_combo_box.currentIndex()
        
        classes = []
        data = []
        for row in range(self.proto_table.rowCount()):
            rows=[]
            for column in range(self.proto_table.columnCount()):
                item = self.proto_table.item(row, column)
                rows.append(float(item.text()))
            data.append(rows)
            
        columns=[]
        for i in range(len(data[0])):
            columns.append(self.table.horizontalHeaderItem(i).text())
        
        data = pd.DataFrame(data,columns=columns)
        
        for i in range(len(columns)):
            if columns[i]==class_column_name:
                continue
            sorted_data = data[[columns[i],class_column_name]].sort_values(columns[i],ascending=False)
            
            index = sorted_data[class_column_name].values.tolist()
            sss=sorted_data[columns[i]].values.tolist()

            u11,u12,u21,u22,sep,sigma = self.metrika(index,sss)
            print(sss[-1],sss[sep],sss[0])
            print(sss[0:sep])
            print(index[0:sep])
            print()
            print(sss[sep:])
            print(index[sep:])
            print("Vazn:",sigma)
            print("")
            for_visual = columns[i]+": \n1-interval: [1,...,"+str(sep+1)+"]\n2-interval:("+str(sep+1)+",...,"+str(len(data))+"]\n(u11,u12,u21,u22) = ("+str(u11)+","+str(u12)+","+str(u21)+","+str(u22)+")\r"
            
            self.information.insertPlainText("\n"+for_visual)
            self.information.insertPlainText("__________________________________________________________________\r\n")
            
        
    def metrika(self,x,sss):
        chegara = 1
        xu11 = x[0:chegara].count(1)
        xu12 = x[0:chegara].count(2)
        xu21 = x[chegara:].count(1)
        xu22 = x[chegara:].count(2)
        #print(x)
        #print("counter:"+str(xu11)+","+str(xu12)+","+str(xu21)+","+str(xu22))
        K1 = x.count(1)
        K2 = x.count(2)
        
        ifoda1 = (xu11*(xu11-1)+xu12*(xu12-1)+xu21*(xu21-1)+xu22*(xu22-1))/(K1*(K1-1)+K2*(K2-1))
        ifoda2 = (xu11*(K2-xu12)+xu12*(K1-xu11)+xu21*(K2-xu22)+xu11*(K1-xu12))/(2*K1*K2)
        
        sigma_max = ifoda1*ifoda2
        #print(sigma_max,ifoda1,ifoda2)
        for i in range(2,len(x)):
            if sss[i-1]==sss[i]:
                continue
            K1 = x.count(1)
            K2 = x.count(2)
            
            u11 = x[0:i].count(1)
            u12 = x[0:i].count(2)
            u21 = x[i:].count(1)
            u22 = x[i:].count(2)
            
            ifoda1 = (u11*(u11-1)+u12*(u12-1)+u21*(u21-1)+u22*(u22-1))/(K1*(K1-1)+K2*(K2-1))
            ifoda2 = (u11*(K2-u12)+u12*(K1-u11)+u21*(K2-u22)+u22*(K1-u21))/(2*K1*K2)
            
            sigma = ifoda1*ifoda2
            if sigma_max<sigma:
                sigma_max = sigma
                xu11 = u11
                xu12 = u12
                xu21 = u21
                xu22 = u22
                chegara=i

        return xu11,xu12,xu21,xu22,chegara,sigma_max
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1520,980)
    mainWindow.show()
    sys.exit(app.exec_())
