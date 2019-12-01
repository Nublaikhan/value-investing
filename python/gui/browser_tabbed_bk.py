from __future__ import unicode_literals
import json
import os
import random
import re
import sys
import time

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt5 import QtGui, QtCore

# Additional imports
from numpy import arange, sin, pi, ndarray, asarray
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, Axes
from matplotlib.dates import epoch2num
from urllib.parse import urlencode

# Project imports
from python.tdameritrade import TDClient
import python.tdameritrade.auth as tdauth

#Converters for datetime converter
import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import pdb
class BasicDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(BasicDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Value Investing Calculator")
        font = title.font()
        font.setPointSize(14)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)
        self.text = QLabel()
        layout.addWidget(self.text)
        layout.addWidget(self.buttonBox)

        #for i in range(0, layout.count()):
        #    layout.itemAt(i).setAlignment(Qt.AlignHCenter)
        
        self.setLayout(layout)

    def setText(self, text):
        self.text.setText(text)


class AboutDialog(BasicDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)


        self.addOkayButton()
        self.setLayout(self.layout)

class InvalidInputDialog(BasicDialog):
    def __init__(self, *args, **kwargs):
        super(InvalidInputDialog, self).__init__(*args, **kwargs)

        invalidInputString = 'blah'
        if isinstance(invalidInputString, str): 
            layout.addWidget(QLabel(invalidInputString))

        self.addOkayButton()
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._token = None
        self._refresh_token = None
        self._tokenLifetime = None
        self._refreshTokenLifetime = None

        # Gather settings
        settingsPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','settings.json')
        with open(settingsPath) as fp:
            self.settings = json.load(fp)

        self.savedStatePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','..','saved_state.json')
        self.savedState = {}
        with open(self.savedStatePath) as fd:
            try:
                self.savedState = json.load(fd)
                if 'last_tickers' not in self.savedState.keys():
                    self.savedState['last_tickers'] = []
            except:
                self.savedState['last_tickers'] = []

        self.tdClient = TDClient(accountIds=self.settings['client_id'])

        # Setup overall layout
        # Setup tab frame
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Setup init tab with matplotlib
        initPlot = MyMplCanvas(self)
        self.tabs.addTab(initPlot, 'Initial Tab')

        # Setup the List frame layout
        listFrame = QFrame()
        listFrame.setFrameShape(QFrame.StyledPanel)
        listFrameLayout = QVBoxLayout()
        listFrame.setLayout(listFrameLayout)

        self.tickerList = TickerList()
        self.tickerList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listButtonLayout = QHBoxLayout()

        # Add text box to the list frame layout
        self.tickerTextBox = QLineEdit()

        # Add the buttons to the button layout
        self.addTickerButton = QPushButton('Add')
        self.addTickerButton.clicked.connect(self.add_ticker)
        self.runTickersButton = QPushButton('Run')
        self.runTickersButton.clicked.connect(self.run_tickers)
        self.addTickerListButton = QPushButton('Add List')
        self.addTickerListButton.clicked.connect(self.add_ticker_list)
        self.removeTickersButton = QPushButton('Remove Ticker')
        self.removeTickersButton.clicked.connect(self.remove_tickers)
        listButtonLayout.addWidget(self.addTickerButton)
        listButtonLayout.addWidget(self.runTickersButton)
        listButtonLayout.addWidget(self.addTickerListButton)
        listButtonLayout.addWidget(self.removeTickersButton)

        # Add the button layout and the list to the listFrame layout
        listFrameLayout.addWidget(self.tickerList)
        listFrameLayout.addWidget(self.tickerTextBox)
        listFrameLayout.addLayout(listButtonLayout)

        # Create the splitter for the list frame and the tab interface
        listTabSplitter = QSplitter(Qt.Horizontal)
        listTabSplitter.addWidget(listFrame)
        listTabSplitter.addWidget(self.tabs)
        listTabSplitter.setStretchFactor(0,0)
        listTabSplitter.setStretchFactor(1,5)
        listTabSplitter.setSizes([100,400])

        # Create the frame for the pice and volume
        self.priceVolFrame = PriceHistoryCanvas(self)

        # Create the splitter for the top and bottom frames
        mainSplit = QSplitter(Qt.Vertical)
        mainSplit.addWidget(listTabSplitter)
        mainSplit.addWidget(self.priceVolFrame)
        mainSplit.setStretchFactor(0,1)
        mainSplit.setStretchFactor(1,1)
        mainSplit.setSizes([400,400])

        # Add the main splitter to the main window layout
        self.setCentralWidget(mainSplit)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Setup File Menu
        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Value Investing Calculator", self)
        about_action.setStatusTip("Find out more about Value Investing Calculator")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # Set Initial Size
        self.resize(800,600)
        self.show()

        self.setWindowTitle("Value Investing Calculator")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        self.authenticate()

        # Setup a timer to determine when to refresh token.
        self.refreshTimer = QTimer()
        self.refreshTimer.timeout.connect(self.checkToken)
        self.refreshTimer.start(60000)

    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setText("Exit Application?")
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        if msgBox.exec_() == QMessageBox.Yes:
            self.saveTickers()
            event.accept()
    
    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.loadLastTickers()

    def saveTickers(self):
        items = []
        for index in range(self.tickerList.count()):
            items.append(self.tickerList.item(index).text())
        if len(items):
            self.savedState['last_tickers'] = items
        with open(self.savedStatePath, 'w') as fd:
            json.dump(self.savedState, fd, indent=3) 
    
    def loadLastTickers(self):
        if len(self.savedState['last_tickers']):
            for t in self.savedState['last_tickers']:
                self.add_ticker(t)

    def authenticate(self):
        resp = tdauth.authentication(self.settings['client_id'], self.settings['redirect_uri'])
        self._token = resp['access_token']
        self._refresh_token = resp['refresh_token']
        self._tokenLifetime = resp['expires_in']
        self._refreshTokenLifetime = resp['refresh_token_expires_in']
        self.tdClient.setToken(resp['access_token'])

    def checkToken(self):
        if self._tokenLifetime:
            if (time.time() - self._tokenLifetime) < 300:
                self.tdauth.refresh_token(self._refresh_token, self.settings['client_id'])

    def add_new_tab(self, ticker):
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def add_ticker(self, ticker=None):
        if ticker:
            tickerText = ticker
        else:
            tickerText = self.tickerTextBox.text()
        # Check input
        if not re.match('^[A-Za-z]*$', tickerText):
            dlg = BasicDialog()
            dlg.setText('Ticker '+tickerText+' is invalid.  Only alphabetical characters are allowed.')
            dlg.exec_()
        elif len(tickerText):
            self.tickerList.addItem(tickerText.upper())
            self.tickerTextBox.clear()

    def run_ticker(self, ticker):
        # Here we are going to gather the data for the main plot widget
        # Ten year
        # Calculate the big 5
        # Add to the plot
        # Five year
        # Calculate the big 5
        # Add to the plot
        # Three year
        # Calculate the big 5
        # Add to the plot
        # One year
        # Calculate the big 5
        # Add to the plot

        # Here we are going to gather the price and volume data for the bottom plot widget
        # Gather last year of pricing data
        data = self.tdClient.history(ticker)
        x = []
        y = []
        for day in data['candles']:
            x.append(day['datetime'])
            #x.append(time.strftime('%D', time.gmtime(day['datetime']/1000)))
            y.append(float(day['close']))
        self.priceVolFrame.addPlot(asarray(x),asarray(y))

        # Gather the last year of volume data

    def run_tickers(self):
        for index in range(self.tickerList.count()):
            self.run_ticker(self.tickerList.item(index).text())

    def add_ticker_list(self):
        pass

    def remove_tickers(self):
        items = self.tickerList.selectedItems()
        if len(items):
            for item in items:
                self.tickerList.takeItem(self.tickerList.row(item))

    def current_tab_changed(self, i):
        #qurl = self.tabs.currentWidget().url()
        #self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = 'Ticker Plot' #self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Value Investing Calculator" % title)

    def about(self):
        dlg = BasicDialog()
        dlg.setText('Version 0.0.0.1')
        dlg.exec_()

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().mainFrame().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()


class TickerList(QListWidget):
    def __init__(self):
        super(TickerList, self).__init__()

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=365, height=100, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.subplots()
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.canvas.draw()


class PriceHistoryCanvas(MyMplCanvas):
    def __init__(self, parent=None):
        super(PriceHistoryCanvas, self).__init__(parent)
        self.axes.set_title('Historical Closing Price')
        self.axes.set_xlabel('Date')
        self.axes.set_ylabel('Price (USD)')
        self.fig.canvas.draw()
    
    def addPlot(self, x, y):
        # The x axis here is a date
        dates = [epoch2num(i/1000) for i in x]
        self.axes.plot(dates,y)
        # Get the actual string for the date
        # set_xticklabels with rotation
        self.fig.canvas.draw()


app = QApplication(sys.argv)
app.setApplicationName("Value Investing Calculator")

window = MainWindow()

app.exec_()