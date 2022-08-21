# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : vi0let
# @File    : QR.py
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask
# from MyQR import myqr
import os
from pyzbar import pyzbar
from PIL import Image, ImageEnhance, ImageFont,ImageDraw


# qrcode和myqr二选一，这里用的是qrcode


def menu():
    print('请输入你的选择:')
    print('1.制作二维码')
    print('2.读取二维码')
    print('3.exit')
    return


def menu_qr_make():
    print('请输入你的选择:')
    print('1.输入二维码信息')
    print('2.添加背景图片')
    print('3.添加标题文字(for 2)')
    print('4.导出的文件名')
    print('5.exit')
    return


def qr_make():
    while 1:
        menu_qr_make()
        choice = eval(input('->'))
        if choice == 1:
            # qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            context = input('->')
            img = qrcode.make(context)
            # 还有下面这种方法(二维纠错添加颜色)
            # qr.add_data(context)
            # img = qr.make_image(image_factory=StyledPilImage, color_mask=SquareGradiantColorMask())
            # img.show()
            img.save('tmp1.png')
        elif choice == 2:
            # 把二维码图片透明化
            if os.path.isfile('tmp1.png') == 0:
                print('你还没有创建二维码的信息哦，请重新输入QWQ')
                continue
            img_1 = Image.open('tmp1.png')
            img_1 = img_1.convert('RGBA')
            width, height = img_1.size  # 长度和宽度
            for i in range(0, width):  # 遍历所有长度的点
                for j in range(0, height):  # 遍历所有宽度的点
                    data = img_1.getpixel((i, j))  # 获取一个像素
                    if data.count(255) == 4:  # RGBA都是255，改成透明色
                        img_1.putpixel((i, j), (255, 255, 255, 0))
            # img_1.show()
            # 二维码和背景图片叠加
            print('请输入你想添加的背景图片')
            img_2 = input('->')
            if os.path.isfile(img_2) == 0:
                print('不存在该背景图片，请重新选择QWQ')
                continue
            img_2 = Image.open(img_2)
            r, g, b, a = img_1.split()
            img_2.paste(img_1, box=(2000 // 2 - 370 // 2, 1247 // 2 - 370 // 2 + 250, 2000 // 2 + 370 // 2, 1247 // 2 + 370 // 2 + 250),mask=a)
            # 这里的box参数是(x1,y1,x2,y2)左上角坐标和右下角坐标,生成的二维码大小是370x370,这里我选取的图片是2000x1247,注意这里参数必须是整数
            # img_2.show()
            img_2.save('tmp2.png')
        elif choice == 3:
            if os.path.isfile('tmp2.png') == 0:
                print('第二问还没有执行，请先执行第二问QWQ')
                continue
            img_3 = Image.open('tmp2.png')
            print('请输入标题文字')
            context = input('->')
            txt_font = ImageFont.truetype('font\\青呱石头体.ttf', 150)       # 可以指定字体，若是没有可注释掉
            draw = ImageDraw.Draw(img_3)
            draw.text((2000//2-800,1247//2-300),context,font=txt_font,fill=(255,250,250))
            img_3.show()
            img_3.save('tmp3.png')
        elif choice == 4:
            print('请输入导出的名字')
            save_name = input('->')
            if os.path.isfile('tmp3.png'):
                os.rename('tmp3.png',save_name)
                os.remove('tmp2.png')
                os.remove('tmp1.png')
            else:
                if os.path.isfile('tmp2.png'):
                    os.rename('tmp2.png', save_name)
                    os.remove('tmp1.png')  # 删除中间文件
                else:
                    if os.path.isfile('tmp1.png'):
                        os.rename('tmp1.png', save_name)
                    else:
                        print('你还没有创建二维码的信息哦，请重新输入QWQ')
        elif choice == 5:
            break
        else:
            print('输入错误，请重新输入QWQ')
    return


def qr_extract():
    print('请输入二维码文件名')
    img_path = input('->')
    if os.path.isfile(img_path):
        img = Image.open(img_path)
        # img.show()
        txt_list = pyzbar.decode(img)
        for i in txt_list:
            context = i.data.decode('utf-8')
            print(context)
    else:
        print('本地不存在该文件哦，请重新选择QWQ')
    return


if __name__ == '__main__':
    while 1:
        menu()
        choice = int(input('->'))
        if choice == 1:
            qr_make()
        elif choice == 2:
            qr_extract()
        elif choice == 3:
            break
        else:
            print('输入的选项错误，请重新选择')
