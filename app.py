import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QWizard,
    QWizardPage,
    QFileDialog,
    QListWidget,
    QLineEdit
)

selected_images = []

class MainWindow(QWizard):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("Lenitcular Image Creator")

        self.wizard = QWizard()

        self.addPage(WelcomePage())
        self.addPage(UploadPage())
        self.addPage(CropPage())
        self.addPage(InterlacePage())

class WelcomePage(QWizardPage):

    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)

        self.setTitle("Welcome")
        label = QLabel("This desktop application was made for a CPSC 490 senior project. \n \n The aim of the application is to create a lenticular image, "
                       "an image that has been pieced together from a max of X input image. Then, by using a lenticular lens photo frame the user can "
                       "place the iamge behind the lens and create \"motion\". \n \n Thank you for using the application!")
        label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class UploadPage(QWizardPage):

    def __init__(self, parent=None):
        super(UploadPage, self).__init__(parent)
        self.setTitle("Upload Images")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(
            "First, please select up to X images that you would like to piece together.")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.btn = QPushButton("Select images")
        self.btn.clicked.connect(self.launchFileDialog)
        self.btn.show()
        layout.addWidget(self.btn)

        self.label_images = QLabel("test")
        layout.addWidget(self.label_images)

    def launchFileDialog(self):
        file_filter = "Image File (*.png *.jpg *.xpm *.bmp)"
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption="Select an image file",
            dir=os.getcwd(),
            filter=file_filter
        )
        self.print_list(list(response[0]))
        return


    def print_list(self, selectedImages):
        if (selectedImages != None):
            for x in selectedImages:
                self.label_images.setText(f"Images:\n {selectedImages}\n")
        return



class CropPage(QWizardPage):

    def __init__(self, parent=None):
        super(CropPage, self).__init__(parent)

        self.setTitle("Crop Images")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(str(selected_images))
        layout.addWidget(self.label)


class InterlacePage(QWizardPage):

    def __init__(self, parent=None):
        super(InterlacePage, self).__init__(parent)

        self.setTitle("Interlace Images")
        label = QLabel("testing page 4")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
