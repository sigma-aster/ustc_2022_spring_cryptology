import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial
import window
from decipher import decipher

def frequency(ui):
    input = ui.textEdit.toPlainText()
    if len(input) == 0:
        result = '请输入文本'
    else:
        result,letter_dict = decipher(input,1,input_dict)
        ui.textBrowser_2.setText(str(letter_dict))
    ui.textBrowser_1.setText(str(result))
    
def convert(ui):
    input = ui.textEdit.toPlainText()
    if len(input) == 0:
        result = '请输入文本'
    else:
        result,letter_dict = decipher(input,2,input_dict)
        ui.textBrowser_2.setText(str(letter_dict))
    ui.textBrowser_1.setText(str(result))

def add(ui):
    key = ui.lineEdit_1.text()
    value = ui.lineEdit_2.text()
    if len(key) == 1 and len(value) == 1:
        input_dict[key] = value
    result,letter_dict = decipher('',0,input_dict)
    ui.textBrowser_2.setText(str(letter_dict))

def delet(ui):
    word = ui.lineEdit_1.text()
    for key in list(input_dict.keys()):
        if key == word:
            del input_dict[word]
    result,letter_dict = decipher('',0,input_dict)
    ui.textBrowser_2.setText(str(letter_dict))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #实例化主窗口
    MainWindow = QMainWindow()
    main_ui = window.Ui_MainWindow()
    main_ui.setupUi(MainWindow)
    MainWindow.show()
    global input_dict
    input_dict = {}
    main_ui.pushButton_1.clicked.connect(partial(frequency, main_ui))
    main_ui.pushButton_2.clicked.connect(partial(convert, main_ui))
    main_ui.pushButton_3.clicked.connect(partial(add, main_ui))
    main_ui.pushButton_4.clicked.connect(partial(delet, main_ui))
    sys.exit(app.exec_())