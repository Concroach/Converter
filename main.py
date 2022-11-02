from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
from PIL import Image
from webptools import dwebp
import os
import glob
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('design.ui', self)
        uic.loadUi(r'C:\Users\Artur\OneDrive\YL\convert\design.ui', self)
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Конвертер')
        # Кнопка загрузки фото
        self.browse.clicked.connect(self.browse_file)
        # Кнопка скачивания фото
        self.convert.clicked.connect(self.convert_func)
    
    
    # Функция загрузки файла в программу
    def browse_file(self):
        self.lb_output.clear()
        self.fname = QFileDialog.getOpenFileName(self, 'Выберите файл')
        self.filetype = list(self.fname)
        self.filetype = self.filetype[0].split('.')
        # root - путь до файла
        self.root = self.fname[0]
        # format - разрешение файла
        self.format = self.filetype[-1]
        # name - имя файла без формата
        self.name = self.filetype[0].split('/')[-1]
        # filename - имя загружаемого файла с форматом
        self.filename = self.root.split('/')[-1]
        # проверка загружаемого формата
        if self.format not in 'pngjpgwebpsvgbmp':
            QMessageBox.about(self, 'Ошибка', "Формат изображения не подлежит конвертации\nВыберите другой файл")
            self.lb_filename.setText('Ошибка, формат не поддерживается')
        else: 
            # Qlabel загрузки файла
            if self.filename == '':
                pass
            else:
                self.lb_filename.setText(self.filename + ' - загружен')
        
    
    # Проверка QRadioButton
    def convert_func(self):
        if self.lb_filename.text() == '':
            QMessageBox.about(self, 'Ошибка', "Не выбран файл для конвертации")
        else:
            if self.png.isChecked():
                self.output_format = 'png'
                if self.format == 'png':
                    self.same_formats()
                else:
                    self.convert2png()
            elif self.jpg.isChecked():
                self.output_format = 'jpg'
                if self.format == 'jpg':
                    self.same_formats()
                else:
                    self.convert2jpg()
            elif self.webp.isChecked():
                self.output_format = 'webp'
                if self.format == 'webp':
                    self.same_formats()
                else:
                    self.convert2webp()
            elif self.bmp.isChecked():
                self.output_format = 'bmp'
                if self.format == 'bmp':
                    self.same_formats()
                else:
                    self.convert2bmp()
            elif self.ascii.isChecked():
                self.output_format = 'txt'
                if self.format == 'txt':
                    self.same_formats()
                elif self.format == 'webp':
                    self.convertwebp2png()
                elif self.format == 'svg':
                    self.convertsvg2png()
                else:
                    self.convert2ascii()
            else:
                QMessageBox.about(self, 'Ошибка', "Не выбран формат для конвертации")


    def same_formats(self):
        QMessageBox.about(self, 'Ошибка', "Выбраны одинаковые форматы")        


    def convert2png(self):
        if self.format == 'jpg':
            image = Image.open(self.root, mode='r')
            image_name = self.root.split('.')[0]
            image_full_name = image_name + '.png'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            image.close()
            self.save()
        elif self.format == 'webp':
            filename = self.root
            outname = filename[:-4] + "png"
            dwebp(input_image=filename, output_image=outname, option="-o", logging="-v")
            self.save()
        elif self.format == 'svg':
            drawing = svg2rlg(self.root)
            renderPM.drawToFile(drawing, f"{self.filetype[0]}.png", fmt='PNG')
            self.save()
        elif self.format == 'bmp':
            for img in glob.glob(self.root):
                Image.open(img).save(os.path.join(f"{self.filetype[0]}.png"))
            self.save()
        else:
            self.error_type()
    
    
    def convert2jpg(self):
        if self.format == 'png':
            image = Image.open(self.root, mode='r')
            rgb_im = image.convert('RGB')
            rgb_im.save(self.root.split('.')[0] + '.' 'jpg')
            image.close()
            self.save()
        elif self.format == 'webp':
            image = Image.open(self.root, mode='r')
            image_name = self.root.split('.')[0]
            image_full_name = image_name + '.jpg'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            self.save()
        elif self.format == 'svg':
            drawing = svg2rlg(self.root)
            renderPM.drawToFile(drawing, f"{self.filetype[0]}.jpg", fmt='JPG')
            self.save()
        elif self.format == 'bmp':
            for img in glob.glob(self.root):
                Image.open(img).save(os.path.join(f"{self.filetype[0]}.jpg"))
            self.save()
        else:
            self.error_type()


    def convert2webp(self):
        if self.format == 'jpg':
            image = Image.open(self.root, mode='r')
            image_name = self.root.split('.')[0]
            image_full_name = image_name + '.webp'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            image.close()
            self.save()
        elif self.format == 'png':
            image = Image.open(self.root, mode='r')
            image_name = self.root.split('.')[0]
            image_full_name = image_name + '.webp'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            image.close()
            self.save()
        elif self.format == 'svg':
            drawing = svg2rlg(self.root)
            renderPM.drawToFile(drawing, f"{self.filetype[0]}1.png", fmt='PNG')
            image = Image.open(f"{self.filetype[0]}1.png", mode='r')
            image_name = self.root.split('.')[0]
            image_full_name = image_name + '.webp'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            image.close()
            path_for_remove = f"{self.filetype[0]}1.png"
            os.remove(path_for_remove) 
            self.save()
        elif self.format == 'bmp':
            for img in glob.glob(self.root):
                Image.open(img).save(os.path.join(f"{self.filetype[0]}1.jpg"))
            image = Image.open((f"{self.filetype[0]}1.jpg"), mode='r')
            image_name = self.filetype[0]
            image_full_name = image_name + '.webp'
            save_path = os.path.join(image_full_name)
            image.save(save_path)
            image.close()
            path_for_remove = f"{self.filetype[0]}1.jpg"
            os.remove(path_for_remove) 
            self.save()
        else:
            self.error_type()


    def convert2bmp(self):
        if self.format == 'jpg':
            Image.open(self.root).save(self.filetype[0] + '.bmp')
            self.save()
        elif self.format == 'png':
            Image.open(self.root).save(self.filetype[0] + '.bmp')
            self.save()
        elif self.format == 'webp':
            Image.open(self.root).save(self.filetype[0] + '.bmp')
            self.save()
        elif self.format == 'svg':
            drawing = svg2rlg(self.root)
            renderPM.drawToFile(drawing, f"{self.filetype[0]}1.png", fmt='PNG')
            Image.open(f"{self.filetype[0]}1.png").save(self.filetype[0] + '.bmp')
            path_for_remove = f"{self.filetype[0]}1.png"
            os.remove(path_for_remove) 
            self.save()
        else:
            self.error_type()


    def resize_image(self, image):
        width, height = image.size
        ratio = height/width
        resized_image = image.resize((100, 50))
        return(resized_image)


    def grayify(self, image):
        grayscale_image = image.convert("L")
        return(grayscale_image)
        

    def pixels_to_ascii(self, image):
        ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        pixels = image.getdata()
        characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
        return(characters)    


    def convert2ascii(self, new_width=100):
        if self.format in 'pngjpgwebpsvgbmp':
            image = Image.open(self.root)
            new_image_data = self.pixels_to_ascii(self.grayify(self.resize_image(image)))
            pixelc = len(new_image_data)  
            ascii_image = "\n".join([new_image_data[index: (index + new_width)] for index in range(0, pixelc, new_width)])   
            with open(f"{self.filetype[0]}.txt", "w") as f:
                f.write(ascii_image)
            self.save()
        else:
            self.error_type()

    # Конвертация webp в png для последующей конвертации в ascii
    def convertwebp2png(self):
        filename = self.root
        outname = self.filetype[0] + '1.' + "png"
        dwebp(input_image=filename, output_image=outname, option="-o", logging="-v")
        self.root = outname
        self.convert2ascii()
        path_for_remove = f"{self.filetype[0]}1.png"
        os.remove(path_for_remove) 


    # Конвертация svg в png для последующей конвертации в ascii
    def convertsvg2png(self):
        pic = svg2rlg(self.root)
        renderPM.drawToFile(pic, f"{self.filetype[0]}1.png", fmt='PNG')
        self.root = f"{self.filetype[0]}1.png"
        self.convert2ascii()
        path_for_remove = f"{self.filetype[0]}1.png"
        os.remove(path_for_remove) 


    # Qlabel в конце с информацией о загрузке файла
    def save(self):
        self.lb_output.setText(f"{self.name}.{self.output_format} - загружен")


    # функция обработки ошибки
    def error_type(self): 
        QMessageBox.about(self, 'Ошибка', "Формат файла не поддерживается")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())