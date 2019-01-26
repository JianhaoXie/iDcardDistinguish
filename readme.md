# 切图与身份证识别
## 0.环境
* (1). 主要依靠python3的pillow与cv2来完成,通过PYQT5写的简陋的gui界面
* (2). 识别文字方面,依靠谷歌的 tesseract-OCR来识别,通过pytesseract来调用
* 注意,要记得给tesseract-OCR装中文依赖chi_sim,否则中文识别不出来,网上很多教程

## 1.目录结构
```
iDcardDistinguish
    ├── image # 存放一些测试身份证,与切图结果
    │   ├── 958.jpg
    │   ├── Card1_N.jpg
    │   ├── Card2_Y.jpg
    │   ├── Card3_Y.jpg
    │   ├── Card4_Y.jpg
    │   ├── Card5_N.jpg
    │   ├── Card6_YN.jpg
    │   ├── cutImg.jpg
    │   ├── cutImg1.jpg
    │   ├── cutImg2.jpg
    │   ├── dest.jpg
    │   ├── dest1.jpg
    │   ├── show.png
    │   └── test.jpg
    ├── main 主函数文件夹
    │   ├── CropLines.py  切行
    │   ├── OCR_Img.py  通过谷歌OCR识别主程序
    │   ├── __init__.py
    │   ├── idCardRecognition.py 切图程序,将图片除了身份证外多余的部分切除
    │   └── photoImg.py 主函数,包括gui界面
    └── readme.md
```
## 2. 切图
* 原图\
![avatar](https://github.com/JianhaoXie/iDcardDistinguish/blob/master/image/Card6_YN.jpg)
* 切图后\
![avatar](https://github.com/JianhaoXie/iDcardDistinguish/blob/master/image/dest.jpg)


## 3. 识别
* 起始gui结构\
![avatar](https://github.com/JianhaoXie/iDcardDistinguish/blob/master/image/gui1.png)
* 起始gui结构\
![avatar](https://github.com/JianhaoXie/iDcardDistinguish/blob/master/image/gui2.png)
* 起始gui结构\
![avatar](https://github.com/JianhaoXie/iDcardDistinguish/blob/master/image/gui3.png)