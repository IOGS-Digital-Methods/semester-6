# -*- coding: utf-8 -*-
"""*start_gui.py* file.

*signal_gui* file contains a simple GUI with a signal

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on PyQt6 GUI development, see : https://iogs-lense-training.github.io/python-pyqt-gui/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 06/oct/2024
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """

    def __init__(self):
        """
        Default constructor of the main window.
        """
        super().__init__()

        self.setWindowTitle("LEnsE - Signal GUI - Digital Interface")
        self.setGeometry(50, 50, 600, 300)

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
        # Q: Change the title of the main section when second_button
        # button is clicked.
        if event == 'main':
            self.main_section.set_title('New Title')
        elif event == 'menu':
            self.main_menu.title_label.setText('New Click Menu')

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

        self.first_button = QPushButton('Click Me')
        self.layout.addWidget(self.first_button)
        self.first_button.clicked.connect(self.action_clicked)

        self.second_button = QPushButton('Click Me 2')
        self.layout.addWidget(self.second_button)
        self.second_button.clicked.connect(self.action_clicked)

    def action_clicked(self):
        """
        Action performed when a button of the menu is clicked.
        """
        sender = self.sender()
        # Q: Emit signal 'menu' or 'main' depending on the button
        # which is clicked.
        if sender == self.first_button:
            self.clicked_menu.emit('menu')
        elif sender == self.second_button:
            self.clicked_menu.emit('main')

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
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.title_label = QLabel("Main Section")
        self.layout.addWidget(self.title_label)


    # Q: Add a set_title method to the main section.
    def set_title(self, title: str):
        """
        Modify the title of the section.
        :param title: Title of the section.
        """
        self.title_label.setText(title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

