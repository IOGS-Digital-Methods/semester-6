# -*- coding: utf-8 -*-
"""*draw_mask_gui.py* file.

*draw_mask_gui* file contains a GUI that opens an image in a QLabel and allows to draw points.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on PyQt6 GUI development, see : https://iogs-lense-training.github.io/python-pyqt-gui/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 06/oct/2024
"""

import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen


class DrawableLabel(QLabel):
    """
    QLabel personnalisé pour permettre de dessiner sur une image.
    """

    def __init__(self, parent=None):
        """Default Constructor."""
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.drawing = False
        self.last_point = QPoint()
        self.mask_pixmap = None  # Mask for drawing
        self.points = []
        self.mask = None

    def set_image(self, image_array):
        """
        Set the image to display.
        :param image_array: Array containing the image data to display.
        """
        self.image = image_array
        # Convert NumPy array to QImage
        height, width, channels = self.image.shape
        qimage = QImage(self.image.data, width, height, QImage.Format.Format_RGB888)
        # Convert QImage to QPixmap and set it in QLabel
        pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(pixmap)
        self.mask_pixmap = QPixmap(pixmap.size())
        self.mask_pixmap.fill(Qt.GlobalColor.transparent)  # Initially transparent mask

    def mousePressEvent(self, event):
        """Action performed when the mouse is pressed."""
        if event.button() == Qt.MouseButton.LeftButton:
            current_point = event.position().toPoint()
            self.points.append(current_point)
            self.draw_point(current_point)
            self.update()
            print(f'New point : x ={current_point.x()} / y ={current_point.y()}')
            if len(self.points) == 2:
                # Calculate coordinates
                x0, y0 = self.points[0].x(), self.points[0].y()
                x1, y1 = self.points[1].x(), self.points[1].y()
                # Draw the rectangle
                painter = QPainter(self.mask_pixmap)
                pen = QPen(Qt.GlobalColor.blue, 5)
                painter.setPen(pen)
                painter.drawRect(x0, y0, (x1 - x0), (y1 - y0))
                painter.end()
                # Create the mask
                self.mask = np.zeros_like(self.image)
                print(self.mask.shape)
                self.mask[y0:y1, x0:x1] = 1
                self.mask = self.mask > 0.5
                # Display image and mask in a new window
                new_window = MainWidget(None)
                new_window.set_image(self.image*self.mask)
                new_window.show()

    def draw_point(self, point: QPoint):
        """Draw a point on the point layer pixmap."""
        painter = QPainter(self.mask_pixmap)
        point_size = 10
        pen = QPen(Qt.GlobalColor.red, point_size)
        painter.setPen(pen)
        painter.drawPoint(point)
        painter.end()


    def paintEvent(self, event):
        """Draw on the image."""
        super().paintEvent(event)
        if self.mask_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.mask_pixmap)


class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Affichage d'image")
        self.main_widget = MainWidget(self)
        self.image_array = cv2.imread("bricks2.jpg")
        self.main_widget.set_image(self.image_array)
        self.setCentralWidget(self.main_widget)



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
        self.image_label = DrawableLabel(self)
        self.layout.addWidget(self.image_label)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_image(self, image_array: np.ndarray):
        """Set an image, by its array."""
        height, width = image_array.shape[:2]
        size = QSize(width, height)
        self.image_label.resize(size)
        self.image_label.set_image(image_array)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())