# -*- coding: utf-8 -*-
"""*serial_mini_gui.py* file.

Serial Communication / Example of a GUI to control LED intensity
----
Engineer training / Digital Interfaces


.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QPushButton, QSlider, QLabel,
                             QVBoxLayout, QWidget, QMessageBox)
import serial                             
                             
                             
class MainWindow(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """

    def __init__(self):
        """
        Initialisation of the main Window.
        """
        super().__init__()
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)        
        self.layout = QVBoxLayout()        
        self.main_widget.setLayout(self.layout)
        
        self.led_on_button = QPushButton("LED ON")
        self.led_on_button.setEnabled(True)
        self.led_on_button.clicked.connect(self.button_action)
        self.layout.addWidget(self.led_on_button)
        self.led_off_button = QPushButton("LED OFF")
        self.led_off_button.setEnabled(False)
        self.led_off_button.clicked.connect(self.button_action)
        self.layout.addWidget(self.led_off_button)
        
    def button_action(self):
        sender = self.sender()
        if sender == self.led_on_button:
            # Action to perform when led_on_button is clicked
            self.led_on_button.setEnabled(False)
            self.led_off_button.setEnabled(True)
        
    def closeEvent(self, event):
        """
        closeEvent redefinition. Use when the user clicks
        on the red cross to close the window
        """
        reply = QMessageBox.question(self, 'Quit', 'Do you really want to close ?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
        
# -------------------------------
# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())