import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
from webbrowser import open
from sys import exit
import pyqtgraph as pg
import data_handler
import ui


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)

        # Menu bar

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 26))
        self.menubar.setObjectName("menubar")

        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")

        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionSobre_MART = QtWidgets.QAction(MainWindow)
        self.actionSobre_MART.setObjectName("actionSobre_MART")
        self.actionSobre_MART.triggered.connect(lambda: webbrowser.open(ui.mart_url))
        mart_icon = QtGui.QIcon()
        mart_icon.addPixmap(QtGui.QPixmap("./assets/mart_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSobre_MART.setIcon(mart_icon)

        self.actionSobre_MLD = QtWidgets.QAction(MainWindow)
        self.actionSobre_MLD.setObjectName("actionSobre_MLD")
        self.actionSobre_MLD.triggered.connect(lambda: Dialog.show())

        self.actionAbrir_archivo = QtWidgets.QAction(MainWindow)
        self.actionAbrir_archivo.setObjectName("actionAbrir_archivo")
        self.actionAbrir_archivo.triggered.connect(lambda: openFileNamesDialog(self))

        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionSalir.triggered.connect(lambda: sys.exit())

        self.menuArchivo.addAction(self.actionAbrir_archivo)
        self.menuArchivo.addSeparator()

        self.menuArchivo.addAction(self.actionSalir)
        self.menuAyuda.addAction(self.actionSobre_MART)
        self.menuAyuda.addAction(self.actionSobre_MLD)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())


        # Central widget

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
                self.statusbar.showMessage(f"{files[0]}")
                self.checks = []

                for i in data_handler.get_column_names(files[0]):
                    c = QtWidgets.QCheckBox(f"{i}")
                    c.stateChanged.connect(lambda: plot_data(self, get_checkboxes(self)))
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
            "MainWindow", "MART log dumper"))
        MainWindow.setWindowIcon(QtGui.QIcon('assets/icon.png'))
        self.scroll_label.setText(_translate("MainWindow", "Valores"))
        self.cursor_label.setText(_translate("MainWindow", "Cursor"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.actionSobre_MART.setText(_translate("MainWindow", "Sobre MART"))
        self.actionSobre_MLD.setText(_translate("MainWindow", "Sobre MART log dumper"))
        self.actionAbrir_archivo.setText(_translate("MainWindow", "Abrir archivo"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionAbrir_archivo.setShortcut(_translate("MainWindow", "Ctrl+O"))

class AboutDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.setEnabled(True)
        Dialog.resize(453, 223)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(453, 223))
        Dialog.setMaximumSize(QtCore.QSize(453, 223))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./assets/mart_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 50, 151, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(120, 70, 311, 41))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 150, 191, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(120, 120, 291, 16))
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(120, 20, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 71, 71))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("./assets/mart_icon.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(340, 180, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sobre MART log dumper"))
        self.label.setText(_translate("Dialog", "Versión 1.0"))
        self.label_2.setText(_translate("Dialog", "MART log dumper es una herramienta gráfica para volcar y visualizar los datos de la ECU del monoplaza."))
        self.label_3.setText(_translate("Dialog", "Copyright (C) 2020 - MART FS"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>Programado por <a href=\"https://olegbrz.github.io/\"><span style=\" text-decoration: underline; color:#0000ff;\">Oleg Brezitskyy</span></a></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "MART log dumper"))
        self.pushButton.setText(_translate("Dialog", "Cerrar"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = Ui_MainWindow()
    window.setupUi(MainWindow)
    MainWindow.show()
    Dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
    about = AboutDialog()
    about.setupUi(Dialog)
    sys.exit(app.exec_())
