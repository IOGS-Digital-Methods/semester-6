import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QWidget, QHBoxLayout, QVBoxLayout,
    QGridLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from pyqtgraph import PlotWidget, exporters, mkPen
import numpy as np

def is_float(list_str):
    """Return if a list of str is floatting number"""
    for s in list_str:
        try:
            float(s)
        except ValueError:
            return False
    return True

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """

    data_loaded = pyqtSignal(str)

    def __init__(self):
        """
        Default constructor of the main window.
        """
        super().__init__()

        self.setWindowTitle("LEnsE - Graph GUI - Digital Interface")
        self.setGeometry(50, 50, 1200, 600)

        # Main Widget and Layout
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()  # Grid layout
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # Widgets
        self.main_menu = MainMenuWidget(self)
        self.main_section = MainWidget(self)

        # Adding widget to the main window layout
        self.main_layout.addWidget(self.main_menu, 0, 0)
        self.main_layout.addWidget(self.main_section, 0, 3, 3, 3)

        # Signal on widget
        self.main_menu.menu_setting.connect(self.action_menu)

    def action_menu(self, event):
        """
        Action performed on a main menu event.
        :param event: Main menu event.
        """
        if event == 'load':
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Charger les donnees", "", "(*.csv *.txt)")
            if file_path:
                self.main_section.data = np.loadtxt(file_path, delimiter=",")
                self.data_loaded.emit('loaded')


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

        self.first_button = QPushButton('Load Data')
        self.layout.addWidget(self.first_button)
        self.first_button.clicked.connect(self.action_menu_setting)
        
        self.graph_range = RangeWidget(self)
        self.layout.addWidget(self.graph_range)

    def action_menu_setting(self):
        """
        Action performed when a setting is modified on the main menu
        """
        sender = self.sender()
        match sender:
            case self.first_button:
                self.menu_setting.emit('load')


class MainWidget(QWidget):
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
        self.data = None
        self.title = "Graph Title"

        # Plot
        self.plot_graph = PlotWidget()
        self.plot_graph.setBackground("w")
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setTitle(self.title, color="k", size="12pt")
        self.plot_graph.setLabel("left", "y (au)")
        self.plot_graph.setLabel("bottom", "x", bottom=True)

        # Layout of this widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Graphical elements
        self.layout.addWidget(self.plot_graph)

        self.parent.data_loaded.connect(self.action_signal)

    def action_signal(self, event):
        if event == 'loaded':
            self.plot_graph.plot(self.data[:, 0], self.data[:, 1], 
                                pen=mkPen(color='b', width=3))


class RangeWidget(QWidget):
    """
    Widget defining the axis limits settings
    """
    def __init__(self, parent):
        """
        Default constructor of the widget.
        :param parent: parent widget or window of this widget.
        """
        super().__init__(parent=parent)
        self.parent = parent

        self.setStyleSheet("border: 1px solid black")
        self.layout = QGridLayout()  # Grid layout
        self.setLayout(self.layout)

        self.label_xmin = QLabel(r"x_min")
        self.layout.addWidget(self.label_xmin, 0, 0)
        self.xmin = QLineEdit("0")
        self.xmin.setEnabled(False)
        self.layout.addWidget(self.xmin, 0, 1)
        self.label_xmax = QLabel(r"x_max")
        self.layout.addWidget(self.label_xmax, 1, 0)
        self.xmax = QLineEdit("1")
        self.xmax.setEnabled(False)
        self.layout.addWidget(self.xmax, 1, 1)

        self.label_ymin = QLabel(r"y_min")
        self.layout.addWidget(self.label_ymin, 0, 2)
        self.ymin = QLineEdit("0")
        self.ymin.setEnabled(False)
        self.layout.addWidget(self.ymin, 0, 3)
        self.label_ymax = QLabel(r"y_max")
        self.layout.addWidget(self.label_ymax, 1, 2)
        self.ymax = QLineEdit("1")
        self.ymax.setEnabled(False)
        self.layout.addWidget(self.ymax, 1, 3)
        self.label_ymax.setStyleSheet("border: 1px solid black;")

        #self.parent.data_loaded.connect(self.action_signal)

    def action_signal(self, event):
        if event == 'loaded':
            print('Data loaded')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())