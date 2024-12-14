import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog,
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QImage
import pyqtgraph as pg
from pyqtgraph import exporters


class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    loaded_picture = pyqtSignal(str)

    def __init__(self):
        """
        Default constructor of the main window.
        """
        super().__init__()

        self.setWindowTitle("LEnsE - Image Filter GUI - Digital Interface")
        self.setGeometry(50, 50, 1800, 600)
        self.image_array = None
        self.magnitude_spectrum = None
        self.result_img = None
        self.dft_shift = None
        self.mask = None

        # Main Widget and Layout
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Widgets
        self.main_menu = MainMenuWidget(self)
        self.main_section = MainWidget(self)
        self.tf_section = GraphWidget(self)
        self.result_section = GraphWidget(self)

        # Adding widget to the main window layout
        self.main_layout.addWidget(self.main_menu, 0, 0)
        self.main_layout.addWidget(self.main_section, 0, 1, 3, 3)
        self.main_layout.addWidget(self.tf_section, 0, 4, 3, 3)
        self.main_layout.addWidget(self.result_section, 0, 7, 3, 3)

        # Signal on widget
        self.main_menu.menu_setting.connect(self.action_menu)

    def action_menu(self, event):
        """
        Action performed on a main menu event.
        :param event: Main menu event.
        """
        match event:
            case 'open':
                self.image_array = self.open_image()
                self.display_image(self.image_array, self.main_section)
            case 'save':
                exporter = exporters.ImageExporter(self.result_section.img.imageItem)
                exporter.export('result.png')
                print("Image saved as 'result.png'")

    def open_image(self) -> QPixmap:
        """
        Open an image and convert to pixmap.
        :return: Image in the pixmap format.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Ouvrir une image", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_path:
            image_array = cv2.imread(file_path)
            self.loaded_picture.emit('loaded')
            return cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            return None

    def display_image(self, image_array: np.ndarray, section: QWidget):
        """
        Display an image in the 'section' section.
        """
        channels = image_array.ndim
        if channels == 3:
            height, width, n = image_array.shape
            print(height, width)
            qimage_format = QImage.Format.Format_RGB888
        if channels == 2:
            n = 1
            height, width = len(image_array[:,0]), len(image_array[0])
            qimage_format = QImage.Format.Format_Grayscale8
        qimage = QImage(image_array.data, width, height, n * width, qimage_format)
        pixmap = QPixmap.fromImage(qimage)
        label_size = self.main_section.size()
        label_size.setWidth(label_size.width() - 20)
        label_size.setHeight(label_size.height() - 20)
        scaled_pixmap = pixmap.scaled(
            label_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        section.image_label.setPixmap(scaled_pixmap)


class MainMenuWidget(QWidget):
    """
    Widget containing the main menu of the application.
    """

    menu_setting = pyqtSignal(str)

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
        self.open_button.clicked.connect(self.action_menu_setting)

        self.save_button = QPushButton('Save Filtered Image to .jpg')
        self.layout.addWidget(self.save_button)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.action_menu_setting)

        self.parent.loaded_picture.connect(self.action_menu)

    def action_menu_setting(self):
        """
        Action performed when a button of the menu is clicked.
        """
        sender = self.sender()
        match sender:
            case self.open_button:
                self.menu_setting.emit('open')
            case self.save_button:
                self.menu_setting.emit('save')

    def action_menu(self, event):
        if event == 'loaded':
            print('Image loaded')


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


class GraphWidget(QWidget):
    """
    Widget containing the plot.
    """

    def __init__(self, parent):
        """
        Default constructor of the widget.
        :param parent: parent widget or window of this widget.
        """
        super().__init__(parent=parent)
        self.parent = parent
        self.img = None

        # Layout of this widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.img)

    def reset(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())