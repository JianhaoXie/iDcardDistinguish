# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from PIL import Image
from PIL import ImageDraw
import pytesseract
from PIL import ImageEnhance
import re
import numpy as np
import pandas as pd
import cv2
from threading import Thread
import time
import CropLines

#   识别文本
def OCR_text(content):
    try:
        return pytesseract.image_to_string(content, "chi_sim", config="-psm 7")
    except Exception:
        return "未识别"
class TextOCR(Thread):
    def __init__(self,content):
        Thread.__init__(self)
        self.content = content

    def run(self):
        self.result = OCR_text(self.content)

    def get_result(self):
        return self.result

# 识别地址
def OCR_addr(content):
    try:
        code = pytesseract.image_to_string(content, "chi_sim", config="-psm 7")
        addr = code.replace("\n", "").replace(" ", "")
        # print(addr)
        return addr
    except Exception as e:
        # print(e, "addr")
        return "未识别"
class AddrOCR(Thread):
    def __init__(self,content):
        Thread.__init__(self)
        self.content = content

    def run(self):
        self.result = OCR_addr(self.content)

    def get_result(self):
        return self.result

# 识别单个字符
def OCR_Character(content):
    try:
        return pytesseract.image_to_string(content, "chi_sim", config="-psm 6")
    except Exception:
        return "未识别"
class CharacterOCR(Thread):
    def __init__(self, content):
        Thread.__init__(self)
        self.content = content

    def run(self):
        self.result = OCR_Character(self.content)

    def get_result(self):
        return self.result

# 识别身份证号
def OCR_IDnum(content):
    try:
        IDnum = pytesseract.image_to_string(content,config="-psm 7")
        try:
            int(IDnum.replace("x",'1'))
            return IDnum
        except Exception:
            return pytesseract.image_to_string(content, 'chi_sim', config="-psm 7")
        # print(IDnum)
    except Exception as e:
        # print(e, "IDnum")
        return "未识别"
class IDnumOCR(Thread):
    def __init__(self, content):
        Thread.__init__(self)
        self.content = content

    def run(self):
        self.result = OCR_IDnum(self.content)

    def get_result(self):
        return self.result

# 识别出生日期
def OCR_birthday(content):
    try:
        r_data = re.compile(r'\d{1,4}')
        code = pytesseract.image_to_string(content, "chi_sim", config="-psm 7")
        birthday = "-".join(re.findall(r_data, code))
        return birthday
        # print(birthday)
    except Exception:
        # print(e, "birthday")
        return "未识别"
class BirthdayOCR(Thread):
    def __init__(self, content):
        Thread.__init__(self)
        self.content = content

    def run(self):
        self.result = OCR_birthday(self.content)

    def get_result(self):
        return self.result

# 身份证识别处理
class ImgProcess(object):

    # 传入图片路径
    def __init__(self, ImgPath):
        self.ImgPath = ImgPath
        # self.image_name = self.ImgPath.splt("\\").split("/")[-1]
        self.twoValue()

    # 输入两个图片地址，拼接图片， 返回拼接后图片路径
    def pngSplice(self, image1, image2):
        img1 = cv2.imread(image1)
        img2 = cv2.imread(image2)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # ====使用numpy的数组矩阵合并concatenate======

        # image = np.concatenate((gray1, gray2))
        # 纵向连接=np.vstack((gray1, gray2))
        # 横向连接image = np.concatenate([gray1, gray2], axis=1)

        # ====使用pandas数据集处理的连接concat========
        df1 = pd.DataFrame(gray1)
        df2 = pd.DataFrame(gray2)  # ndarray to dataframe

        # df = pd.concat([df1, df2])
        # 纵向连接, 拼接两次图像一，增加字数
        df = pd.concat([df1, df2], axis=1)

        # 横向连接
        im = np.array(df)  # dataframe to ndarray
        # cv2.imshow('image', im)
        # cv2.waitKey(0)

        saveFilePath = "../image/test.jpg"  # 拼接后的图片保存路径
        cv2.imwrite(saveFilePath, im, (cv2.IMWRITE_JPEG_QUALITY, 100))
        return saveFilePath

    # 二值化列表
    def twoValue(self):
        self.table = []
        threshold = 1
        for i in range(256):
            if i < threshold:
                self.table.append(0)
            else:
                self.table.append(1)
        return self.table

    # 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
    # 该函数也可以改成RGB判断的,具体看需求如何
    def getPixel(self, image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y - 1))
        else:
            return None

        # 降噪
        # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），
        # 	当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
        # G: Integer 图像二值化阀值
        # N: Integer 降噪率 0 <N <8
        # Z: Integer 降噪次数
        # 输出
        #  0：降噪成功
        #  1：降噪失败
    def filterNoise(self, image, G, N, Z):
        draw = ImageDraw.Draw(image)
        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = self.getPixel(image, x, y, G, N)
                    if color != None:
                        draw.point((x, y), color)

    # 图像处理
    def Img_main(self):
        # 截取彩色照片
        # img = Image.open(self.ImgPath)
        # w, h = img.size
        # imgbox = (w * 0.64, 0, w * 0.95, h * 0.75)

        # 增强图像 加灰度处理
        Im = Image.open(self.ImgPath) # Convert to grayscale
        Im = ImageEnhance.Contrast(Im).enhance(3.5)
        w, h = Im.size

        # 1.灰度图
        Im = Im.convert('L')

        # 2.图像二值化
        self.Im = Im.point(self.table, '1')  # strongly //Ad: Fast Dis: Over Filter
        # self.Im.show()
        img = self.Im
        # 性别
        sex = (w*0.2, h * 0.25, w * 0.24, h * 0.38)
        self.sex = img.crop(sex)
        # self.sex.show()


        # 民族
        nation = (w * 0.395, h * 0.25, w * 0.64, h * 0.38)
        self.nation = img.crop(nation)
        # self.nation.show()

        # 身份证号
        IDnumbox = (w * 0.35, h * 0.8, w*0.95, h*0.95)
        self.IDnum = img.crop(IDnumbox)
        # self.IDnum.show()

        # 姓名
        namebox = (w * 0.17, h*0.1, w * 0.64, h * 0.25)
        self.name = img.crop(namebox)
        # self.name.show()

        # 出生日期
        birthdaybox = (w * 0.17, h * 0.35, w * 0.64, h * 0.46)
        self.birthday = img.crop(birthdaybox)
        # self.birthday.show()

        # 地址
        addrbox = (w * 0.17, h * 0.46, w * 0.60, h * 0.8)
        self.addr = img.crop(addrbox)
        c = CropLines.CropLines()
        self.lineList = c.cropLinesMain(self.addr)

    # 采用多线程的方式
    def main(self):
        t1 = time.time()
        self.Img_main()
        IDnum = IDnumOCR(self.IDnum)
        name = TextOCR(self.name)
        sex = CharacterOCR(self.sex)
        nation = CharacterOCR(self.nation)
        birthday = BirthdayOCR(self.birthday)
        # addr = AddrOCR(self.addr)
        tList = [i for i in range(len(self.lineList))]
        # print(tList)
        for i in tList:
            tList[i] = TextOCR(self.lineList[i])

        for i in [IDnum, name, sex, nation, birthday]+tList:
            i.start()
        for i in [IDnum, name, sex, nation, birthday]+tList:
            i.join()
        addr = ''
        for i in tList:
            addr = addr + i.get_result().replace(' ',"")

        data = {
            "name": name.get_result(),
            "sex": sex.get_result(),
            "birthday": birthday.get_result(),
            "IDnum": IDnum.get_result(),
            "nation": nation.get_result(),
            "addr": addr
        }
        # 以字典形式输出及返回
        print(data)
        print("用时{}秒！！！".format(time.time() - t1))
        return data

    # 原先识别方法，速度慢
    def main1(self):
        self.Img_main()
        print(pytesseract.image_to_string(self.name, "chi_sim"))
        try:
            name = pytesseract.image_to_string(self.name, "chi_sim")
            # print(name)
        except Exception as e:
            # print(e, "name")
            name = "未识别"

        try:
            sex = pytesseract.image_to_string(self.sex, "chi_sim", config="-psm 6")
            # print(nation)

        except Exception as e:
            # print(e, "sex")
            sex = "未识别"

        try:
            nation = pytesseract.image_to_string(self.nation, "chi_sim", config="-psm 6")
            # print(nation)

        except Exception as e:
            # print(e, "sex")
            nation = "未识别"


        try:
            r_data = re.compile(r'\d{1,4}')
            code = pytesseract.image_to_string(self.birthday, "chi_sim")
            birthday = "-".join(re.findall(r_data, code))
            # print(birthday)
        except Exception as e:
            # print(e, "birthday")
            birthday = "未识别"

        try:
            code = pytesseract.image_to_string(self.addr, "chi_sim")
            addr = code.replace("\n", "").replace(" ", "")
            # print(addr)
        except Exception as e:
            # print(e, "addr")
            addr = "未识别"

        try:
            IDnum = pytesseract.image_to_string(self.IDnum)
            try:
                int(IDnum.replace("x",'1'))
            except Exception:
                IDnum = pytesseract.image_to_string(self.IDnum, 'chi_sim')
            # print(IDnum)
        except Exception as e:
            # print(e, "IDnum")
            IDnum = "未识别"

        data = {
            "name" : name,
            "sex" : sex,
            "birthday" : birthday,
            "IDnum" : IDnum,
            "nation" : nation,
            "addr" : addr
        }
        # 以字典形式输出及返回
        print(data)
        return data

if __name__ == "__main__":
    a = ImgProcess("../image/Card2_Y.jpg")
    a.main()