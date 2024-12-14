# -*- coding: utf-8 -*-
"""*image_gui.py* file.

*image_gui* file contains a GUI that opens an image in a QLabel

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on PyQt6 GUI development, see : https://iogs-lense-training.github.io/python-pyqt-gui/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 06/oct/2024
"""

import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog,
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """

    def __init__(self):
        """
        Default constructor of the main window.
        """
        super().__init__()

        self.setWindowTitle("LEnsE - Image GUI - Digital Interface")
        self.setGeometry(50, 50, 600, 300)
        self.image_array = None

        # Main Widget and Layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()    # Horizontal Layout
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Widgets
        self.main_menu = MainMenuWidget(self)
        self.main_section = MainWidget(self)

        # Adding widget to the main window layout
        self.main_layout.addWidget(self.main_menu)
        self.main_layout.addWidget(self.main_section)

        # Signal on widget
        self.main_menu.clicked_menu.connect(self.action_menu)

    def action_menu(self, event):
        """
        Action performed on a main menu event.
        :param event: Main menu event.
        """
        print(event)
        if event == 'open':
            self.image_array = self.open_image()
            self.display_image(self.image_array)
            self.main_menu.invert_button.setEnabled(True)
            self.main_menu.data_button.setEnabled(True)
        elif event == 'invert':
            self.display_image(255-self.image_array)
        elif event == 'data':
            if self.image_array is not None:
                mean = self.image_array.mean()
                print(f'Mean = {mean}')
                print(f'Shape = {self.image_array.shape}')
            else:
                print('No Image')


    def open_image(self) -> QPixmap:
        """
        Open an image and convert to pixmap.
        :return: Image in the pixmap format.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Ouvrir une image", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_path:
            image_array = cv2.imread(file_path)
            return cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        else:
            return None

    def display_image(self, image_array: np.ndarray):
        """
        Display an image in the main section.
        :param pixmap: Image to display.
        """
        height, width, channels = image_array.shape
        if channels == 3:  # Image en RGB (3 canaux)
            qimage_format = QImage.Format.Format_RGB888
        qimage = QImage(image_array.data, width, height, 3 * width, qimage_format)
        pixmap = QPixmap.fromImage(qimage)
        label_size = self.main_section.size()
        label_size.setWidth(label_size.width() - 20)
        label_size.setHeight(label_size.height() - 20)
        scaled_pixmap = pixmap.scaled(
            label_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.main_section.image_label.setPixmap(scaled_pixmap)

class MainMenuWidget(QWidget):
    """
    Widget containing the main menu of the application.
    """

    clicked_menu = pyqtSignal(str)

    def __init__(self, parent):
        """
        Default constructor of the widget.
        :param parent: parent widget or window of this menu.
        """
        super().__init__(parent=parent)
        self.parent = parent

        # Layout of this widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.title_label = QLabel("Main Menu")
        self.layout.addWidget(self.title_label)

        self.open_button = QPushButton('Open Image')
        self.layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.action_clicked)
        # Q. Add a button to inverse the image
        self.invert_button = QPushButton('Inverse Image')
        self.layout.addWidget(self.invert_button)
        self.invert_button.clicked.connect(self.action_clicked)
        self.invert_button.setEnabled(False)
        # Q. Add a button to display information about the image
        self.data_button = QPushButton('Infos Image')
        self.layout.addWidget(self.data_button)
        self.data_button.clicked.connect(self.action_clicked)
        self.data_button.setEnabled(False)

    def action_clicked(self):
        """
        Action performed when a button of the menu is clicked.
        """
        sender = self.sender()
        if sender == self.open_button:
            self.clicked_menu.emit('open')
        elif sender == self.invert_button:
            self.clicked_menu.emit('invert')
        elif sender == self.data_button:
            self.clicked_menu.emit('data')

class MainWidget(QWidget):
    """
    Widget containing the main section.
    """

    def __init__(self, parent):
        """
        Default constructor of the widget.
        :param parent: parent widget or window of this widget.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.setStyleSheet("background-color: gray")

        # Layout of this widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.image_label = QLabel('Image')
        self.layout.addWidget(self.image_label)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.resizeEvent = self.on_resize

    def on_resize(self, event):
        size = self.size()
        QWidget.resizeEvent(self, event)
        self.image_label.setFixedSize(size.width()-20, size.height()-20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
