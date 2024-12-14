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
            case 'tf':
                self.dft_shift = self.compute_ft()
                self.plot_image(self.tf_section, self.magnitude_spectrum.T, True)
                self.main_menu.filter_button.setEnabled(True)
                self.main_menu.reverse_mask_checkbox.setEnabled(True)
                self.main_menu.slider.setEnabled(True)
            case 'filter':
                self.apply_filter()
                self.plot_image(self.result_section, self.result_img.T, hide_hist=True)
                self.main_menu.save_button.setEnabled(True)
            case 'update_mask':
                self.update_mask()
                self.plot_image(self.tf_section, (self.magnitude_spectrum * self.mask[:, :, 0]).T, True)
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

    def compute_ft(self):
        dft = cv2.dft(np.float32(self.image_array), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        self.magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
        return dft_shift

    def apply_filter(self):
        self.update_mask()
        # apply mask and inverse DFT
        fshift = self.dft_shift * self.mask
        f_ishift = np.fft.ifftshift(fshift)
        img_back = cv2.idft(f_ishift)
        self.result_img = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    def update_mask(self):
        rows, cols = self.image_array.shape
        crow, ccol = rows // 2, cols // 2
        reverse = int(self.main_menu.reverse_mask_checkbox.isChecked())
        mask = reverse + np.zeros((rows, cols, 2), np.uint8)
        self.main_menu.slider.setMaximum(max(crow, ccol))
        r_ratio = crow / max(crow, ccol)
        c_ratio = ccol / max(crow, ccol)
        index_row = crow - int(self.main_menu.slider.value() * r_ratio)
        index_col = ccol - int(self.main_menu.slider.value() * c_ratio)
        mask[crow - index_row:crow + index_row + 1, ccol - index_col:ccol + index_col + 1] = 1-reverse
        self.mask = mask

    @staticmethod
    def plot_image(section, image: np.ndarray, hide_hist=False):
        section.img = pg.image(image)
        section.reset()
        if hide_hist:
            section.img.ui.histogram.hide()
            section.img.ui.roiBtn.hide()
            section.img.ui.menuBtn.hide()
        section.layout.addWidget(section.img)


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

        self.tf_button = QPushButton('Compute FT')
        self.layout.addWidget(self.tf_button)
        self.tf_button.clicked.connect(self.action_menu_setting)
        self.tf_button.setEnabled(False)

        self.filter_button = QPushButton('Apply Filter')
        self.layout.addWidget(self.filter_button)
        self.filter_button.clicked.connect(self.action_menu_setting)
        self.filter_button.setEnabled(False)

        self.reverse_mask_checkbox = QCheckBox('Reverse Mask')
        self.layout.addWidget(self.reverse_mask_checkbox)
        self.reverse_mask_checkbox.setEnabled(False)
        self.reverse_mask_checkbox.stateChanged.connect(self.action_menu_setting)

        self.slider_label = QLabel("Mask Size", alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.slider_label)

        self.slider = QSlider()
        self.slider.setFixedSize(QSize(200, 200))
        self.layout.addWidget(self.slider)
        self.slider.setEnabled(False)
        self.slider.sliderMoved.connect(self.action_menu_setting)

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
            case self.tf_button:
                self.menu_setting.emit('tf')
            case self.filter_button:
                self.menu_setting.emit('filter')
            case self.slider:
                self.menu_setting.emit('update_mask')
            case self.save_button:
                self.menu_setting.emit('save')
            case self.reverse_mask_checkbox:
                self.menu_setting.emit('update_mask')

    def action_menu(self, event):
        if event == 'loaded':
            self.tf_button.setEnabled(True)
            self.filter_button.setEnabled(False)
            self.reverse_mask_checkbox.setEnabled(False)
            self.slider.setValue(0)
            self.slider.setEnabled(False)
            self.save_button.setEnabled(False)
            self.parent.tf_section.reset()
            self.parent.result_section.reset()


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