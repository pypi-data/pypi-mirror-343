# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_chooser_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ProjectChooser(object):
    def setupUi(self, ProjectChooser):
        if not ProjectChooser.objectName():
            ProjectChooser.setObjectName(u"ProjectChooser")
        ProjectChooser.setWindowModality(Qt.WindowModality.ApplicationModal)
        ProjectChooser.resize(426, 355)
        ProjectChooser.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        ProjectChooser.setSizeGripEnabled(True)
        ProjectChooser.setModal(True)
        self.gridLayout = QGridLayout(ProjectChooser)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ProjectChooser)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.projectList = QListWidget(ProjectChooser)
        self.projectList.setObjectName(u"projectList")

        self.verticalLayout.addWidget(self.projectList)

        self.buttonBox = QDialogButtonBox(ProjectChooser)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(ProjectChooser)
        self.buttonBox.accepted.connect(ProjectChooser.accept)
        self.buttonBox.rejected.connect(ProjectChooser.reject)

        self.projectList.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(ProjectChooser)
    # setupUi

    def retranslateUi(self, ProjectChooser):
        ProjectChooser.setWindowTitle(QCoreApplication.translate("ProjectChooser", u"Project chooser", None))
        self.label.setText(QCoreApplication.translate("ProjectChooser", u"&Available Qt projects", None))
    # retranslateUi

