# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!



'''界面程序，及主函数用于连接各项功能'''
from PyQt5 import QtCore, QtGui
import sys
from PyQt5 import QtWidgets
# 识别程序
import OCR_Img
# 切图程序
import idCardRecognition


# UI界面， 主函数是 openWork，负责连接各个功能
class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(716, 580)
        self.birthday_text = QtWidgets.QTextEdit(Dialog)
        self.birthday_text.setGeometry(QtCore.QRect(330, 350, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.birthday_text.setFont(font)
        self.birthday_text.setObjectName("birthday_text")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(490, 310, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.button1 = QtWidgets.QPushButton(Dialog)
        self.button1.setGeometry(QtCore.QRect(540, 40, 131, 61))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(18)
        self.button1.setFont(font)
        self.button1.setObjectName("button1")
        self.button2 = QtWidgets.QPushButton(Dialog)
        self.button2.setGeometry(QtCore.QRect(540, 170, 131, 61))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(18)
        self.button2.setFont(font)
        self.button2.setObjectName("button2")
        self.name_text = QtWidgets.QTextEdit(Dialog)
        self.name_text.setGeometry(QtCore.QRect(10, 350, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.name_text.setFont(font)
        self.name_text.setObjectName("name_text")
        self.sex_text = QtWidgets.QTextEdit(Dialog)
        self.sex_text.setGeometry(QtCore.QRect(490, 350, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.sex_text.setFont(font)
        self.sex_text.setObjectName("sex_text")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 310, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(330, 310, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 420, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.addr_text = QtWidgets.QTextEdit(Dialog)
        self.addr_text.setGeometry(QtCore.QRect(110, 490, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.addr_text.setFont(font)
        self.addr_text.setObjectName("addr_text")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 310, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ID_text = QtWidgets.QTextEdit(Dialog)
        self.ID_text.setGeometry(QtCore.QRect(110, 420, 511, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ID_text.setFont(font)
        self.ID_text.setObjectName("ID_text")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 490, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.nation_text = QtWidgets.QTextEdit(Dialog)
        self.nation_text.setGeometry(QtCore.QRect(170, 350, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.nation_text.setFont(font)
        self.nation_text.setObjectName("nation_text")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 491, 281))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # image 文件夹位置 加载入self.path
        self.path = '../image/'

        self.NgImage = QtGui.QImage(self.path+"show.png")
        self.label_7.setPixmap(QtGui.QPixmap.fromImage(self.NgImage).scaled(self.label_7.size()))

        # 上传图片
        self.button1.clicked.connect(self.msg)
        # fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self,"打开图片","C:/","*.jpg;;*.png;;All Files (*);;Text Files (*.txt)")

        self.button2.clicked.connect(self.openWork)

        # Qt.KeepAspectRatio, Qt.SmoothTransformation

    def msg(self):
        '''选择图片上传'''
        # 选择图像文件
        self.filename = QtWidgets.QFileDialog.getOpenFileName(None, '选择要识别的图像', '', '(*.bmp *.jpeg *.jpg *.png)')[0]
        self.NgImage = QtGui.QImage(self.filename)
        self.label_7.setPixmap(QtGui.QPixmap.fromImage(self.NgImage).scaled(self.label_7.size()))


    def openWork(self):
        # pass
        '''传入一个json格式的数据，示例'''
        # self.filename 图片路径
        try:
            # 切图
            cimg = idCardRecognition.CutImg(self.filename)
            # 切图返回的路径
            des = cimg.cutImgMain("../image/dest.jpg")
            try:
                cimg = idCardRecognition.CutImg(des)
                # 切图返回的路径
                des = cimg.cutImgMain(des)
                try:
                    cimg = idCardRecognition.CutImg(des)
                    # 切图返回的路径
                    des = cimg.cutImgMain(des)
                    print("共切图三次")
                except Exception:
                    print("共切图两次")
            except Exception:
                print("共切图一次")
            finally:
                # 图片识别
                self.NgImage = QtGui.QImage(des)
                Im = OCR_Img.ImgProcess(des)
                self.data = Im.main()
        except Exception:
            print("不用切图")
            # 不切图，直接识别
            Im = OCR_Img.ImgProcess(self.filename)
            self.data = Im.main()
        #
        # self.oneforall_data = {"name":"name",
        #         "sex":"sex",
        #         "nation":"nation",
        #         "addr":"addr",
        #         "birthday":"birthday",
        #         "IDnum":"IDnum12345678998765432"}
        self.name_text.setText(self.data["name"])
        self.sex_text.setText(self.data["sex"])
        self.nation_text.setText(self.data["nation"])
        self.birthday_text.setText(self.data["birthday"])
        self.addr_text.setText(self.data["addr"])
        self.ID_text.setText(self.data["IDnum"])


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "性别"))
        self.button1.setText(_translate("Dialog", "上传证件"))
        self.button2.setText(_translate("Dialog", "开始解析"))
        self.label.setText(_translate("Dialog", "姓名"))
        self.label_3.setText(_translate("Dialog", "出生日期"))
        self.label_5.setText(_translate("Dialog", "身份证号"))
        self.label_2.setText(_translate("Dialog", "民族"))
        self.label_6.setText(_translate("Dialog", "地址"))


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    Form=QtWidgets.QWidget()
    ui=Ui_Dialog()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())