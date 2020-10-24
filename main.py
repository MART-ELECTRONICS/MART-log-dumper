from sys import float_repr_style
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import data_handler
import ui


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Splitter (splits screen in two halves)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter.setHandleWidth(10)

        # Layout for pyqtgraph

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.widget = pg.PlotWidget()
        self.widget.setObjectName("widget")
        self.widget.showGrid(x=True, y=True)
        # self.widget.setBackground('w')

        self.horizontalLayout.addWidget(self.widget)

        # Right vertical layout (buttons, values, etc)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Load file button

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumWidth(200)
        self.pushButton_2.clicked.connect(lambda: openFileNamesDialog(self))
        self.verticalLayout.addWidget(self.pushButton_2)

        # Label for scroll area (column names)

        self.scroll_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.scroll_label.setObjectName("label")
        self.verticalLayout.addWidget(self.scroll_label)

        # Scroll area

        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 208, 424))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # Update button

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(
            lambda: plot_data(self, get_checkboxes(self)))

        # Cursor label

        self.cursor_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.cursor_label.setObjectName("cursor_label")
        self.verticalLayout.addWidget(self.cursor_label)

        # X-axis spinbox

        self.spinbox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.spinbox.setPrefix('Time: ')
        self.spinbox.setDecimals(2)
        self.spinbox.valueChanged.connect(lambda: set_cursor(self))
        self.spinbox.setSingleStep(0.01)
        self.verticalLayout.addWidget(self.spinbox)

        # Text area for cursor values

        self.cursor = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.cursor.setObjectName("cursor")
        self.cursor.setReadOnly(True)
        self.cursor.setMaximumHeight(90)
        # self.cursor.setBackgroundVisible(True)

        self.verticalLayout.addWidget(self.cursor)

        # Misc

        self.horizontalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.showMessage("No se ha cargado ningún archivo")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Functions

        def get_checkboxes(self):
            to_plot = []
            for i in self.checks:
                if i.isChecked():
                    to_plot.append(i.text())
            return to_plot

        def set_cursor(self):
            x = self.spinbox.value()
            try:
                self.vLine.setValue((x, 0))
            except:
                pass

        def set_spinbox(self):
            x = round(self.vLine.getXPos(), 2)
            self.spinbox.setValue(x)

        def set_cursor_values(self):
            columns = get_checkboxes(self)
            cursors = ""

            if self.spinbox.value() in self.df.index:
                for column in columns:
                    query = self.spinbox.value()
                    result = self.df.loc[query][column]
                    line = f"{column}: {result} {self.units_map[column]}\n"
                    cursors += line

                self.cursor.setPlainText(cursors)

        def openFileNamesDialog(self):
            options = QtWidgets.QFileDialog.Options()
            files, _ = QtWidgets.QFileDialog.getOpenFileNames(
                caption='Abrir archivo', filter='Archivos CSV (*.csv)', options=options)
            if files:
                print(files[0])
                self.filename = files[0]
                self.statusbar.showMessage(f'Se ha cargado {files[0]}')
                self.checks = []

                for i in data_handler.get_column_names(files[0]):
                    c = QtWidgets.QCheckBox(f"{i}")
                    self.verticalLayout_2.addWidget(c)
                    self.checks.append(c)

                self.df = data_handler.read_csv(files[0])
                self.spinbox.setMinimum(min(self.df.index))
                self.spinbox.setMaximum(max(self.df.index))
                self.spinbox.setValue(min(self.df.index))
                self.units_map = data_handler.map_units(files[0])

        # Update pyqtgraph

        def plot_data(self, to_plot):
            self.widget.clear()
            self.widget.addLegend()

            x = self.df.index

            j = 0
            for i in to_plot:
                # plot data: x, y values
                y = list(self.df[i])
                self.widget.plot(x, y, pen=pg.mkPen(
                    color=ui.plot_palette[j % len(ui.plot_palette)], width=2, name=i))
                j += 1

            self.vLine = pg.InfiniteLine(pos=0, angle=90, movable=True)
            self.vLine.sigPositionChanged.connect(lambda: set_spinbox(self))
            self.vLine.sigPositionChanged.connect(
                lambda: set_cursor_values(self))
            self.widget.addItem(self.vLine, ignoreBounds=True)
            self.vLine.setValue(min(self.df.index))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "MART TELEMETRY TOOL"))
        MainWindow.setWindowIcon(QtGui.QIcon('assets/icon.png'))
        self.scroll_label.setText(_translate("MainWindow", "Valores"))
        self.pushButton_2.setText(_translate("MainWindow", "Cargar archivo"))
        self.pushButton.setText(_translate("MainWindow", "Actualizar"))
        self.cursor_label.setText(_translate("MainWindow", "Cursor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = Ui_MainWindow()
    window.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
