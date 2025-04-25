# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(395, 199)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.name = QLineEdit(Dialog)
        self.name.setObjectName(u"name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 24))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.path = QLineEdit(Dialog)
        self.path.setObjectName(u"path")

        self.horizontalLayout.addWidget(self.path)

        self.change = QPushButton(Dialog)
        self.change.setObjectName(u"change")

        self.horizontalLayout.addWidget(self.change)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.recurseIntoSubFolderLabel = QLabel(Dialog)
        self.recurseIntoSubFolderLabel.setObjectName(u"recurseIntoSubFolderLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.recurseIntoSubFolderLabel)

        self.pattern = QLineEdit(Dialog)
        self.pattern.setObjectName(u"pattern")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pattern)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.use_disk_cache = QCheckBox(Dialog)
        self.use_disk_cache.setObjectName(u"use_disk_cache")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.use_disk_cache)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 38, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.button_box = QDialogButtonBox(Dialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.button_box)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.name)
        self.label_2.setBuddy(self.path)
        self.recurseIntoSubFolderLabel.setBuddy(self.pattern)
        self.label_3.setBuddy(self.use_disk_cache)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.name, self.path)
        QWidget.setTabOrder(self.path, self.change)
        QWidget.setTabOrder(self.change, self.pattern)

        self.retranslateUi(Dialog)
        self.button_box.rejected.connect(Dialog.reject)
        self.button_box.accepted.connect(Dialog.accept)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Profile", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"&Name", None))
#if QT_CONFIG(whatsthis)
        self.name.setWhatsThis(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Name of the profile</p><p>Will be used in the <span style=\" font-style:italic;\">Profiles</span> menu</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"&Directory", None))
#if QT_CONFIG(whatsthis)
        self.path.setWhatsThis(QCoreApplication.translate("Dialog", u"Path of the image (jpeg) files", None))
#endif // QT_CONFIG(whatsthis)
        self.change.setText(QCoreApplication.translate("Dialog", u"&Select", None))
        self.recurseIntoSubFolderLabel.setText(QCoreApplication.translate("Dialog", u"New name &pattern", None))
        self.pattern.setText(QCoreApplication.translate("Dialog", u"%Y%m%d_%H%M%S.jpg", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Use disk &cache", None))
        self.use_disk_cache.setText("")
    # retranslateUi

