# !/usr/bin/env python3
# -*- coding=utf-8 -*-

'''切图，用于将证件多余部分切除'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math


# 坐标点 数据类型
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tup = (x, y)


# 直线数据类型
class Line(object):
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        self._center = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


# 切图类：传入一个需要切图的路径，返回一个切割完成的图片路径
class CutImg(object):

    def __init__(self, imgPath):
        self.imgpath = imgPath

    def scare(self,b, g, r):
        return [b, g, r]

    # 对直线line的列表，以_center.y的大小，在原列表中进行升序排列 冒泡
    def sorty(self, list1):
        for j in range(1, len(list1)):
            for i in range(len(list1)-1,j-1, -1):
                if list1[i]._center.y < list1[i - 1]._center.y:
                    list1[i], list1[i - 1] = list1[i - 1], list1[i]

    # 对直线line的列表，以_center.x的大小，在原列表中进行升序排列
    def sortx(self, list1):
        for j in range(1, len(list1)):
            for i in range(len(list1)-1,j-1, -1):
                if list1[i]._center.x < list1[i - 1]._center.x:
                    list1[i], list1[i - 1] = list1[i - 1], list1[i]

    # 在列表中添加元素
    def push_back(self, list1, ele):
        return list1.append(ele)


    # 传入两个Line类型的直线参数,计算两直线交叉点，返回交叉点
    def computeIntersect(self, l1, l2):
        x1 = l1._p1.x
        x2 = l1._p2.x
        y1 = l1._p1.y
        y2 = l1._p2.y
        x3 = l2._p1.x
        x4 = l2._p2.x
        y3 = l2._p1.y
        y4 = l2._p2.y
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if d:
            ptx = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
            pty = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d
            return Point(ptx, pty)
        return Point(-1, -1)


    def getGrayImg(self):
        img = cv2.imread(self.imgpath)
        self.img = img
        # cv2.imshow("sss", img)
        # cv2.waitKey(0)

        print("读取图片完成！")
        print("图片大小：", img.shape)
        img_width = img.shape[1]
        img_heigh = img.shape[0]
        # img_plane_num = img.shape[2]

        min_w = 200
        scale = min(10.0, img_width * 1.0 / min_w)
        self.scale = scale
        self.w_proc = int(img_width * 1.0 / scale)
        self.h_proc = int(img_heigh * 1.0 / scale)

        img_proc = cv2.resize(img, (self.w_proc, self.h_proc), interpolation=cv2.INTER_LINEAR)
        self.img_proc = img_proc
        self.img_dis = img_proc.copy()

        # Otsu's binarization.
        gray = cv2.cvtColor(img_proc, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.blur(gray, (3, 3))
        # gray模糊化之后的灰度图  对应type=1
        return self.gray

    # 展示图片
    def ImageShow(self, image):
        plt.subplot(),plt.imshow(image)
        plt.title("图"), plt.xticks([]), plt.yticks([])
        plt.show()

    # 获得二值图, 输出 high_thres与二值图
    def get2VImg(self):
        gray = self.getGrayImg()
        self.high_thres, self.thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # print type(ret),ret
        # thresh 二值图
        return self.high_thres, self.thresh

    # 获得边缘图，返回
    def getCannyImg(self):
        high_thres, thresh = self.get2VImg()
        low_thres = high_thres * 0.5
        self.canny = cv2.Canny(self.gray, low_thres, high_thres)
        # canny 边缘图 对应type=2
        return  self.canny

    # 抠图主程序, 输入需要输出的路径和图片名称，返回最后抠图所在最终路径
    def cutImgMain(self, outputImagePath='dst.jpg'):
        canny = self.getCannyImg()
        # 从边缘图中提取线条
        minLineLength = 200
        maxLineGap = 15
        # print(np.pi / 180,w_proc / 3,w_proc / 3)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, int(self.w_proc / 3), int(self.w_proc / 3), maxLineGap)
        # HoughLinesP(canny, lines, 1, CV_PI / 180, w_proc / 3(80), w_proc / 3(200), 20);

        # 遍历直线
        horizontals = []
        verticals = []
        debug = True
        for i in lines:
            v = i
            delta_x = v[0][0] - v[0][2]
            delta_y = v[0][1] - v[0][3]

            l = Line(Point(v[0][0], v[0][1]), Point(v[0][2], v[0][3]))
            if (math.fabs(delta_x) > math.fabs(delta_y)):
                self.push_back(horizontals, l)
                if debug:
                    img_proc = cv2.line(self.img_proc, (v[0][0], v[0][1]), (v[0][2], v[0][3]), self.scare(0, 0, 255), 3)
                    # Line(img_proc,tpoint(v[0],v[1]))
                    self.img_proc = img_proc
            else:
                self.push_back(verticals, l)
                if debug:
                    img_proc = cv2.line(self.img_proc, (v[0][0], v[0][1]), (v[0][2], v[0][3]), self.scare(0, 255, 0), 3)
                    self.img_proc = img_proc

        # img_proc :
        # 边缘图中 没有检测到足够的线

        if len(horizontals) < 2:
            if len(horizontals) == 0 or horizontals[0]._center.y > self.h_proc / 2:
                self.push_back(horizontals, Line(Point(0, 0), Point(self.w_proc - 1, 0)))
            if len(horizontals) == 0 or horizontals[0]._center.y <= self.h_proc / 2:
                self.push_back(horizontals, Line(Point(0, self.h_proc - 1), Point(self.w_proc - 1, self.h_proc - 1)))

        if len(verticals) < 2:
            if len(verticals) == 0 or verticals[0]._center.x > self.w_proc / 2:
                self.push_back(verticals, Line(Point(0, 0), Point(0, self.h_proc - 1)))
            if len(verticals) == 0 or verticals[0]._center.x <= self.w_proc / 2:
                self.push_back(verticals, Line(Point(self.w_proc - 1, 0), Point(self.w_proc - 1, self.h_proc - 1)))

        # 按中心点排序
        self.sorty(horizontals)
        self.sortx(verticals)


        if debug:
            img_proc = cv2.line(self.img_proc, horizontals[0]._p1.tup, horizontals[0]._p2.tup, self.scare(0, 255, 0), 2, cv2.LINE_AA)
            img_proc = cv2.line(img_proc, horizontals[len(horizontals) - 1]._p1.tup,
                                horizontals[len(horizontals) - 1]._p2.tup, self.scare(0, 255, 0), 2, cv2.LINE_AA)
            img_proc = cv2.line(img_proc, verticals[0]._p1.tup, verticals[0]._p2.tup, self.scare(255, 0, 0), 2, cv2.LINE_AA)
            self.img_proc = cv2.line(img_proc, verticals[len(verticals) - 1]._p1.tup, verticals[len(verticals) - 1]._p2.tup,
                                self.scare(255, 0, 0), 2, cv2.LINE_AA)
            # img_proc = cv2.line(img_proc, (v[0][0], v[0][1]), (v[0][2], v[0][3]), scare(0, 0, 255), 3)

        # 透视变换
        w_a4 = 950
        h_a4 = 600

        dst = np.zeros([w_a4, h_a4, 3])

        dst_pts = []
        img_pts = []

        self.push_back(dst_pts, [0, 0])
        self.push_back(dst_pts, [w_a4 - 1, 0])
        self.push_back(dst_pts, [0, h_a4 - 1])
        self.push_back(dst_pts, [w_a4 - 1, h_a4 - 1])

        self.push_back(img_pts, list(self.computeIntersect(horizontals[0], verticals[0]).tup))
        self.push_back(img_pts, list(self.computeIntersect(horizontals[0], verticals[-1]).tup))
        self.push_back(img_pts, list(self.computeIntersect(horizontals[-1], verticals[0]).tup))
        self.push_back(img_pts, list(self.computeIntersect(horizontals[-1], verticals[-1]).tup))

        for i in range(len(img_pts)):
            if debug:
                # print(type(img_pts[i].x))
                cv2.circle(self.img_proc, (int(img_pts[i][0]), int(img_pts[i][1])), 10, self.scare(255, 255, 0), 3)
            img_pts[i][0] *= self.scale
            img_pts[i][1] *= self.scale
            img_pts[i] = tuple(img_pts[i])
        # print("img_pts [0]", img_pts[0][0])
        # 对 img_pts 和 dst_pts 进行格式转换
        img_pts = np.array(img_pts)
        img_pts = np.float32(img_pts)
        img_pts = np.array(img_pts)

        dst_pts = np.array(dst_pts)
        dst_pts = np.float32(dst_pts)
        dst_pts = np.array(dst_pts)

        # print(dst_pts)

        transmtx = cv2.getPerspectiveTransform(img_pts, dst_pts)

        row, col, ch = dst.shape
        # print(dst.shape)
        dst = cv2.warpPerspective(self.img, transmtx, (row, col))
        #
        cv2.imwrite(outputImagePath, dst)
        print("切图完成，路径：{}".format(outputImagePath))
        return outputImagePath

    def showAllImg(self):
        plt.subplot(2,2,1),plt.imshow(self.img)
        plt.title('Original'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 2), plt.imshow(self.gray)
        plt.title('gray'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 3), plt.imshow(self.canny)
        plt.title('canny'), plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 4), plt.imshow(self.img_proc)
        plt.title('img_proc'), plt.xticks([]), plt.yticks([])
        plt.show()

if __name__=="__main__":
    cimg = CutImg("../image/Card3_Y.jpg")
    print(cimg.cutImgMain("../image/dest1.jpg"))
    # gray = cimg.getGrayImg()
    # t = cimg.get2VImg()
    # cimg.ImageShow(gray)
    # cimg.showAllImg()