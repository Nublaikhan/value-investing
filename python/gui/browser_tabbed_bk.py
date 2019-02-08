from __future__ import unicode_literals
import sys
import os
import random
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt5 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Value Investing Calculator")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 0.0.0.1"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class WebBrowserTab(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Mozarella Ashbadger", self)
        about_action.setStatusTip("Find out more about Mozarella Ashbadger")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Mozarella Ashbadger Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to Mozarella Ashbadger Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.show()

        self.setWindowTitle("Mozarella Ashbadger")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Setup overall layout
        # Setup tab frame
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # Setup init tab with matplotlib
        initPlot = MyStaticMplCanvas()
        self.tabs.addTab(initPlot, 'Initial Tab')

        # Setup the List frame layout
        listFrame = QFrame()
        listFrame.setFrameShape(QFrame.StyledPanel)
        listFrameLayout = QVBoxLayout()
        listFrame.setLayout(listFrameLayout)

        tickerList = TickerList()
        listButtonLayout = QHBoxLayout()

        # Add text box to the list frame layout
        tickerTextBox = QLineEdit()

        # Add the buttons to the button layout
        addTickerButton = QPushButton('Add')
        runTickersButton = QPushButton('Run')
        addTickerListButton = QPushButton('Add List')
        listButtonLayout.addWidget(addTickerButton)
        listButtonLayout.addWidget(runTickersButton)
        listButtonLayout.addWidget(addTickerListButton)

        # Add the button layout and the list to the listFrame layout
        listFrameLayout.addWidget(tickerList)
        listFrameLayout.addWidget(tickerTextBox)
        listFrameLayout.addLayout(listButtonLayout)

        # Create the splitter for the list frame and the tab interface
        listTabSplitter = QSplitter(Qt.Horizontal)
        listTabSplitter.addWidget(listFrame)
        listTabSplitter.addWidget(self.tabs)
        listTabSplitter.setStretchFactor(0,0)
        listTabSplitter.setStretchFactor(1,5)
        listTabSplitter.setSizes([100,400])

        # Create the frame for the pice and volume
        #priceVolFrame = QFrame()
        priceVolFrame = MyStaticMplCanvas()

        # Create the splitter for the top and bottom frames
        mainSplit = QSplitter(Qt.Vertical)
        mainSplit.addWidget(listTabSplitter)
        mainSplit.addWidget(priceVolFrame)
        mainSplit.setStretchFactor(0,1)
        mainSplit.setStretchFactor(1,1)
        mainSplit.setSizes([400,200])

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

    def add_new_tab(self, ticker):

        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        # More difficult! We only want to update the url when it's from the
        # correct tab
        #browser.urlChanged.connect(lambda qurl, browser=browser:
        #                           self.update_urlbar(qurl, browser))

        #browser.loadFinished.connect(lambda _, i=i, browser=browser:
        #                             self.tabs.setTabText(i, browser.page().title()))

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
        dlg = AboutDialog()
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
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

app = QApplication(sys.argv)
app.setApplicationName("Value Investing Calculator")

window = MainWindow()

app.exec_()