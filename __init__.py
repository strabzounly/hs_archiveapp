# -*- coding: utf-8 -*-
"""
/***************************************************************************
 hs_archiveapp
                                 A QGIS plugin
 أعمال القانون رقم 33 لعام 2008
                             -------------------
        begin                : 2021-07-16
        copyright            : (C) 2021 by Souhail Trabzounly
        email                : Souhhail@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load hs_archiveapp class from file hs_archiveapp.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .hs_archiveapp import hs_archiveapp
    return hs_archiveapp(iface)
