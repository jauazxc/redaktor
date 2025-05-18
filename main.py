from PyQt5.QtWidgets import *
from PIL import Image, ImageOps, ImageFilter
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

workdir = ''

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.savedir = "Modified/"

    def LoadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width, label_height = images_label.width(), images_label.height()
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        images_label.setPixmap(scaled_pixmap)
        images_label.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path)
                or os.path.isdir(path)):
                os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(self.dir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_levo(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_pravo(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(self.dir, self.savedir, self.filename)
        self.showImage(image_path)

    def do_rezkost(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.savedir, self.filename)
        self.showImage(image_path)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()




def ShowChoosenImage():
    if images_list.currentRow() >= 0:
        filename = images_list.currentItem().text()
        workimage.LoadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()

def filter(files, extensions):
    result = []
    for file in files:
        if file.endswith(extensions):
            result.append(file)
    return result


def showFilenamesList():
    chooseWorkdir() 
    files = filter(os.listdir(workdir), 'png')
    images_list.clear()
    for file in files:
        images_list.addItem(file)

app = QApplication([])
main_win = QWidget()

papka_button = QPushButton('papka')
levo_button = QPushButton('levo')
pravo_button = QPushButton('pravo')
mirror_button = QPushButton('mirror')
rezkost_button = QPushButton('rezkost')
gray_button = QPushButton('gray')
images_list = QListWidget()
images_label = QLabel('kartinka')

papka_button.clicked.connect(showFilenamesList)

main_layout = QHBoxLayout()
left_layout = QVBoxLayout()
right_layout = QVBoxLayout()
button_layout = QHBoxLayout()

button_layout.addWidget(levo_button)
button_layout.addWidget(pravo_button)
button_layout.addWidget(mirror_button)
button_layout.addWidget(rezkost_button)
button_layout.addWidget(gray_button)

right_layout.addWidget(images_label)
right_layout.addLayout(button_layout)

left_layout.addWidget(papka_button)
left_layout.addWidget(images_list)

main_layout.addLayout(left_layout)
main_layout.addLayout(right_layout)

images_list.currentRowChanged.connect(ShowChoosenImage)

gray_button.clicked.connect(workimage.do_bw)
levo_button.clicked.connect(workimage.do_levo)
pravo_button.clicked.connect(workimage.do_pravo)
mirror_button.clicked.connect(workimage.do_mirror)
rezkost_button.clicked.connect(workimage.do_rezkost)

main_win.setWindowTitle('redaktor')
main_win.setLayout(main_layout)
main_win.show()
main_win.resize(700, 500)
app.exec()
