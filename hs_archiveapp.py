# -*- coding: utf-8 -*-
"""
/***************************************************************************
 hs_archiveapp
                                 A QGIS plugin
        HABITAT Syria Archive App
                              -------------------
        begin                : 2021-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Souhail Trabzounly
        email                : Souhhail@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from hs_archiveapp_dialog import hs_archiveappDialog
from qgis.core import *
from qgis.utils import *
from PyQt4.QtGui import *

import sys
import os
import os.path
import subprocess


class hs_archiveapp:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'hs_archiveapp_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&hs_archiveapp')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'hs_archiveapp')
        self.toolbar.setObjectName(u'hs_archiveapp')

        self.commandline = 'D:\\Dropbox\\UN\\UNHABITAT\\HABITAT-SYRIA-OFFICE-Contract.July.August.2023\\ArchiveApp\\Lazarus\\archiveapp.exe' 

        self.username='<not_set>'
        self.password='<not_set>'
        self.database='<not_set>'
        self.appfeature='<not_set>'
        self.appaction='<not_set>'

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('hs_archiveapp', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        # Create the dialog (after translation) and keep reference
        self.dlg = hs_archiveappDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/hs_archiveapp/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'hs_archiveapp'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&hs_archiveapp'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop

        result=True
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            layerList = QgsMapLayerRegistry.instance().mapLayersByName("tgeo_property")
            if layerList is None:
                return
            if len(layerList) == 0:
                return
            Layer = layerList[0]
            self.provider = Layer.dataProvider()
            cadanum = ""

            selected_features = Layer.selectedFeatures ()
            if selected_features is None:
                return
            features = None
            features = []
            field_names = [
                field.name()
                for field in Layer.pendingFields()]
            fltr=''
            pcode=''
            czone=''
            for feature in selected_features:
                if 'pcode' in field_names:
                    pcode = format( "pcode='{}'", feature['pcode'])
                if 'czone' in field_names:
                    czone = format( "czone={}", str(feature['czone']))    
            if czone == '':
                fltr = czone
            if pcode == '':
                if fltr == '':
                    fltr = pcode
                else:
                    fltr = format('({})AND({})', fltr, pcode)
                
            dirname, filename = os.path.split(os.path.abspath(__file__))
            #os.startfile(os.path.join(dirname,"hs_archiveapp.exe"), cadaid)
            subprocess.call([
                self.commandline,
                self.username,
                self.password,
                self.database,
                self.appfeature,
                self.appaction,
                fltr
            ])

def ErrMessage(message):
    #Error Message Box
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.exec_()
