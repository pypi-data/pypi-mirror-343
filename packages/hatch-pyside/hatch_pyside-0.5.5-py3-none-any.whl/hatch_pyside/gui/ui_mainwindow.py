# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.action_Change_project_folder = QAction(MainWindow)
        self.action_Change_project_folder.setObjectName(u"action_Change_project_folder")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.action_Quit.setMenuRole(QAction.MenuRole.QuitRole)
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.action_About.setMenuRole(QAction.MenuRole.AboutRole)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionAbout_Qt.setMenuRole(QAction.MenuRole.AboutQtRole)
        self.action_Reload = QAction(MainWindow)
        self.action_Reload.setObjectName(u"action_Reload")
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.project_files_widget = QListWidget(self.centralwidget)
        self.project_files_widget.setObjectName(u"project_files_widget")
        self.project_files_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_2.addWidget(self.project_files_widget)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(70, 0))
        icon1 = QIcon(QIcon.fromTheme(u"media-seek-forward"))
        self.pushButton.setIcon(icon1)

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(70, 0))
        icon2 = QIcon(QIcon.fromTheme(u"media-seek-backward"))
        self.pushButton_2.setIcon(icon2)

        self.verticalLayout.addWidget(self.pushButton_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.files_widget = QListWidget(self.centralwidget)
        self.files_widget.setObjectName(u"files_widget")
        self.files_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.files_widget)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.project_files_widget)
        self.label_2.setBuddy(self.files_widget)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.project_files_widget, self.files_widget)
        QWidget.setTabOrder(self.files_widget, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton_4)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.action_Change_project_folder)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Reload)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)

        self.retranslateUi(MainWindow)
        self.action_Quit.triggered.connect(MainWindow.close)
        self.actionAbout_Qt.triggered.connect(MainWindow.about_qt)
        self.action_About.triggered.connect(MainWindow.about)
        self.action_Change_project_folder.triggered.connect(MainWindow.change_project)
        self.pushButton.clicked.connect(MainWindow.remove)
        self.pushButton_2.clicked.connect(MainWindow.add)
        self.pushButton_3.clicked.connect(MainWindow.build)
        self.pushButton_4.clicked.connect(MainWindow.clean)
        self.action_Reload.triggered.connect(MainWindow.reload)
        self.action_Save.triggered.connect(MainWindow.save)
        self.pushButton_5.clicked.connect(MainWindow.lupdate)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"hatch-pyside", None))
        self.action_Change_project_folder.setText(QCoreApplication.translate("MainWindow", u"&Change project folder", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(statustip)
        self.action_Quit.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"&About...", None))
#if QT_CONFIG(statustip)
        self.action_About.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About &Qt...", None))
#if QT_CONFIG(statustip)
        self.actionAbout_Qt.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.actionAbout_Qt.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.action_Reload.setText(QCoreApplication.translate("MainWindow", u"&Reload", None))
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"&Project files", None))
        self.pushButton.setText("")
        self.pushButton_2.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Other &files", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"&Build", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"&Lupdate", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"&Clean", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
    # retranslateUi

