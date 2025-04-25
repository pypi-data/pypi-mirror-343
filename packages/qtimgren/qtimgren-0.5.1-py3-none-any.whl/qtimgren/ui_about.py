# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.setWindowModality(Qt.WindowModality.ApplicationModal)
        About.resize(297, 169)
        About.setSizeGripEnabled(False)
        About.setModal(True)
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(About)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 49, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.version = QLabel(About)
        self.version.setObjectName(u"version")

        self.verticalLayout.addWidget(self.version)

        self.libversion = QLabel(About)
        self.libversion.setObjectName(u"libversion")

        self.verticalLayout.addWidget(self.libversion)

        self.python_version = QLabel(About)
        self.python_version.setObjectName(u"python_version")

        self.verticalLayout.addWidget(self.python_version)

        self.verticalSpacer_2 = QSpacerItem(20, 49, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(About)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(About)
        self.buttonBox.accepted.connect(About.accept)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label.setText(QCoreApplication.translate("About", u"QtImgren", None))
        self.version.setText(QCoreApplication.translate("About", u"Version: ", None))
        self.libversion.setText(QCoreApplication.translate("About", u"(pyimgren version: 0.0.0)", None))
        self.python_version.setText(QCoreApplication.translate("About", u"Python version:", None))
    # retranslateUi

