# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDoubleSpinBox,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

from .main_view import View

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(793, 540)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_qt = QAction(MainWindow)
        self.action_about_qt.setObjectName(u"action_about_qt")
        self.action_new_profile = QAction(MainWindow)
        self.action_new_profile.setObjectName(u"action_new_profile")
        self.action_manage_profiles = QAction(MainWindow)
        self.action_manage_profiles.setObjectName(u"action_manage_profiles")
        self.actionChange_Folder = QAction(MainWindow)
        self.actionChange_Folder.setObjectName(u"actionChange_Folder")
        self.action_merge = QAction(MainWindow)
        self.action_merge.setObjectName(u"action_merge")
        self.action_merge.setEnabled(True)
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_Clean = QAction(MainWindow)
        self.action_Clean.setObjectName(u"action_Clean")
        self.action_Reset = QAction(MainWindow)
        self.action_Reset.setObjectName(u"action_Reset")
        self.action_Informations = QAction(MainWindow)
        self.action_Informations.setObjectName(u"action_Informations")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.images_display = QCheckBox(self.centralWidget)
        self.images_display.setObjectName(u"images_display")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.images_display.sizePolicy().hasHeightForWidth())
        self.images_display.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.images_display)

        self.tableView = View(self.centralWidget)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.tableView)

        self.groupBox = QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.reset = QPushButton(self.groupBox)
        self.reset.setObjectName(u"reset")

        self.horizontalLayout_2.addWidget(self.reset)

        self.renamed = QPushButton(self.groupBox)
        self.renamed.setObjectName(u"renamed")

        self.horizontalLayout_2.addWidget(self.renamed)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.delta = QDoubleSpinBox(self.centralWidget)
        self.delta.setObjectName(u"delta")
        self.delta.setDecimals(3)
        self.delta.setMinimum(-14400.000000000000000)
        self.delta.setMaximum(14400.000000000000000)

        self.horizontalLayout.addWidget(self.delta)

        self.rename = QPushButton(self.centralWidget)
        self.rename.setObjectName(u"rename")

        self.horizontalLayout.addWidget(self.rename)

        self.back = QPushButton(self.centralWidget)
        self.back.setObjectName(u"back")

        self.horizontalLayout.addWidget(self.back)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 793, 33))
        self.menu_File = QMenu(self.menuBar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Help = QMenu(self.menuBar)
        self.menu_Help.setObjectName(u"menu_Help")
        self.menu_Profiles = QMenu(self.menuBar)
        self.menu_Profiles.setObjectName(u"menu_Profiles")
        self.menuDisk_cache = QMenu(self.menuBar)
        self.menuDisk_cache.setObjectName(u"menuDisk_cache")
        self.menuDisk_cache.setEnabled(False)
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.delta)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.tableView, self.delta)
        QWidget.setTabOrder(self.delta, self.rename)
        QWidget.setTabOrder(self.rename, self.back)

        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Profiles.menuAction())
        self.menuBar.addAction(self.menuDisk_cache.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.action_merge)
        self.menu_File.addAction(self.action_settings)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_quit)
        self.menu_Help.addAction(self.action_about)
        self.menu_Help.addAction(self.action_about_qt)
        self.menu_Profiles.addAction(self.action_new_profile)
        self.menu_Profiles.addSeparator()
        self.menu_Profiles.addSeparator()
        self.menu_Profiles.addAction(self.action_manage_profiles)
        self.menuDisk_cache.addAction(self.action_Informations)
        self.menuDisk_cache.addSeparator()
        self.menuDisk_cache.addAction(self.action_Clean)
        self.menuDisk_cache.addAction(self.action_Reset)

        self.retranslateUi(MainWindow)
        self.action_quit.triggered.connect(MainWindow.close)
        self.delta.valueChanged.connect(self.tableView.delta_changed)
        self.rename.clicked.connect(self.tableView.rename)
        self.back.clicked.connect(self.tableView.back)
        self.reset.clicked.connect(self.tableView.reset_selection)
        self.renamed.clicked.connect(self.tableView.select_renamed)
        self.images_display.clicked["bool"].connect(self.tableView.display_images)
        self.action_Clean.triggered.connect(self.tableView.cache_clean)
        self.action_Reset.triggered.connect(self.tableView.cache_reset)
        self.action_Informations.triggered.connect(self.tableView.cache_info)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QtImgren", None))
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(statustip)
        self.action_quit.setStatusTip(QCoreApplication.translate("MainWindow", u"Exit from the application", None))
#endif // QT_CONFIG(statustip)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"&About", None))
#if QT_CONFIG(statustip)
        self.action_about.setStatusTip(QCoreApplication.translate("MainWindow", u"Version information for QtImgren", None))
#endif // QT_CONFIG(statustip)
        self.action_about_qt.setText(QCoreApplication.translate("MainWindow", u"About &Qt", None))
#if QT_CONFIG(statustip)
        self.action_about_qt.setStatusTip(QCoreApplication.translate("MainWindow", u"Information about the underlying Qt framework", None))
#endif // QT_CONFIG(statustip)
        self.action_new_profile.setText(QCoreApplication.translate("MainWindow", u"&New profile", None))
#if QT_CONFIG(statustip)
        self.action_new_profile.setStatusTip(QCoreApplication.translate("MainWindow", u"Create a new profile", None))
#endif // QT_CONFIG(statustip)
        self.action_manage_profiles.setText(QCoreApplication.translate("MainWindow", u"&Manage profiles", None))
#if QT_CONFIG(statustip)
        self.action_manage_profiles.setStatusTip(QCoreApplication.translate("MainWindow", u"Edit or remove existing profiles", None))
#endif // QT_CONFIG(statustip)
        self.actionChange_Folder.setText(QCoreApplication.translate("MainWindow", u"Change &Folder", None))
        self.action_merge.setText(QCoreApplication.translate("MainWindow", u"&Merge", None))
#if QT_CONFIG(statustip)
        self.action_merge.setStatusTip(QCoreApplication.translate("MainWindow", u"Merge pictures from another folder", None))
#endif // QT_CONFIG(statustip)
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"&Settings", None))
#if QT_CONFIG(statustip)
        self.action_settings.setStatusTip(QCoreApplication.translate("MainWindow", u"Configure the language and cache", None))
#endif // QT_CONFIG(statustip)
        self.action_Clean.setText(QCoreApplication.translate("MainWindow", u"&Clean", None))
#if QT_CONFIG(statustip)
        self.action_Clean.setStatusTip(QCoreApplication.translate("MainWindow", u"Remove unused entries from the cache", None))
#endif // QT_CONFIG(statustip)
        self.action_Reset.setText(QCoreApplication.translate("MainWindow", u"&Reset", None))
#if QT_CONFIG(statustip)
        self.action_Reset.setStatusTip(QCoreApplication.translate("MainWindow", u"Purge all entries from the cache", None))
#endif // QT_CONFIG(statustip)
        self.action_Informations.setText(QCoreApplication.translate("MainWindow", u"&Informations", None))
#if QT_CONFIG(statustip)
        self.action_Informations.setStatusTip(QCoreApplication.translate("MainWindow", u"Cache informations", None))
#endif // QT_CONFIG(statustip)
        self.images_display.setText(QCoreApplication.translate("MainWindow", u"Display &images", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Automatic selections", None))
        self.reset.setText(QCoreApplication.translate("MainWindow", u"Default &selection", None))
        self.renamed.setText(QCoreApplication.translate("MainWindow", u"Select renamed &images", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"&Delta (minutes)", None))
        self.rename.setText(QCoreApplication.translate("MainWindow", u"&Rename", None))
        self.back.setText(QCoreApplication.translate("MainWindow", u"&Back", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_Profiles.setTitle(QCoreApplication.translate("MainWindow", u"&Profiles", None))
        self.menuDisk_cache.setTitle(QCoreApplication.translate("MainWindow", u"Disk &cache", None))
    # retranslateUi

