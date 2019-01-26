# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import time

# 切行
class CropLines(object):
    # 切割前去噪， 传入Image对象，输出去噪完的Image对象
    def beforCrop(self,image):

        width, height = image.size  # 获取宽和高
        # 遍历每一列
        for x_column in range(width):
            count_x = 0  # 每列黑点数量
            for y_row in range(height):
                if image.getpixel((x_column, y_row)) == 0:
                    count_x += 1
            # 如果黑点小于等于2
            if count_x <= 2:
                for i in range(height):
                    image.putpixel((x_column, i), 255)
        self.image = image
        # self.image.save("../image/modified4.jpg", 'jpeg')
        return self.image

    # 传入一个 Image对象 对其进行切行， 输出每行的Image对象组成的列表
    def getCropLines(self, image):
        width,height = image.size # 获取宽和高
        ## 先将字符按行切开 去掉上下的冗余白边
        child_img_list_temp = []
        top = -1  # 每个字符上边的坐标
        is_bk = False  # 是否break跳出循环
        # 从最上边一列开始一行一行遍历
        for y_row in range(height):
            # 对每一行，遍历每一列
            for x_column in range(width):
                is_bk = False
                # 如果一个字符的最上边还没有定位
                # print(image.getpixel((x_column, y_row)))
                if top == -1 and image.getpixel((x_column, y_row)) == 0:  # 上边未定位，为黑色
                    top = y_row
                    is_bk = True
                    break
                elif top != -1 and image.getpixel((x_column, y_row)) == 0:  # 上边已经定位，等于黑色
                    is_bk = True
                    break
            # 上边已经定位,且此行全为白色
            if not is_bk and top != -1 and y_row - top > 10:
                child_img = image.crop((0, top, width, y_row))  # 切割一次
                # print('left:',0, 'top:',top,'right:',width,'bottom:',y_row )
                # 计算切出来的每个子图的黑色像素个数
                count_bp = 0
                for w in range(child_img.width):
                    for h in range(child_img.height):
                        if child_img.getpixel((w, h)) == 0:
                            count_bp += 1
                if y_row - top > 15 and count_bp > 20:
                    child_img_list_temp.append(child_img)  # 切割后的图像添加到list
                top = -1
                is_bk = False
        return child_img_list_temp

    # 去掉每行两边冗余空白, 传入每行Image对象列表
    def remvWhite(self, f_image):
        child_img_list = []
        for image in f_image:
            width, height = image.size  # 获取宽和高
            ## 去掉左边的冗余白边
            left = -1  # 每个字符左边的坐标
            # 从最左边一列开始一列一列遍历
            for x_column in range(width):
                count_col_bkz = 0
                # 对每一列，遍历每一行
                for y_row in range(height):
                    # 如果一个字符的最左边还没有定位
                    if left == -1 and image.getpixel((x_column, y_row)) == 0:  # 左边未定位 为黑色
                        count_col_bkz += 1
                        if count_col_bkz > 6: # 去除单列黑色像素点小于6的噪声
                            left = x_column-5
                            break
            # 去掉右边的冗余白边
            right = width-1
            for x_column_y in range(width-1,-1,-1):
                # count_col_bky = 0
                for y_row_y in range(height):
                    if right == width-1 and image.getpixel((x_column_y, y_row_y)) == 0:
                        # count_col_bky += 1
                        # if count_col_bky > 5:
                        right = x_column_y+5
                        break
            if left != -1 and right != width-1:
                child_img = image.crop((left,0,right,height))
                # child_img_list.append(child_img)

                # 计算切出来的每个子图的黑色像素个数
                count_bp = 0
                for w in range(child_img.width):
                    for h in range(height):
                        if child_img.getpixel((w, h)) == 0:
                            count_bp += 1
                if count_bp > 300:
                    child_img_list.append(child_img)
        return child_img_list

    def cropLinesMain(self, image):
        # 去噪
        # image = self.beforCrop(image)
        lineList = self.getCropLines(image)
        lineList = self.remvWhite(lineList)
        return lineList

if __name__ == "__main__":
    img = Image.open("test.jpg")
    img = img.convert('L')
    t1 = time.time()
    s = CropLines()
    lineList = s.getCropLines(img)
    lineList = s.remvWhite(lineList)
    t2 = time.time()
    print(t2-t1)
    for i in lineList:
        i.show()
