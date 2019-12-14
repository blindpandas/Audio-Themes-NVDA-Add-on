# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.


import os
import shutil
import wx
import gui
import globalVars
from contextlib import suppress

import addonHandler
addonHandler.initTranslation()


# A flag to indicate whether the user should be notified of updates to the default audio theme
__DEFAULT_THEME_UPDATED__ = False
THEMES_HOME = os.path.join(globalVars.appArgs.configPath, "audio-themes")
DEFAULT_THEME_FOLDER = os.path.join(os.path.dirname(__file__), "Default")


def onInstall():
    should_copy = False
    if not os.path.isdir(THEMES_HOME):
        os.mkdir(THEMES_HOME)
        should_copy = True
    elif not os.path.isdir(os.path.join(THEMES_HOME, "Default")):
        should_copy = True
    elif __DEFAULT_THEME_UPDATED__:
        rv = gui.messageBox(
            _("The default audio theme has been updated with new sounds.\n"
            "Do you want to apply these updates?"),
            _("Theme Updates Available"),
            wx.YES_NO|wx.ICON_QUESTION
        )
        if rv == wx.YES:
            shutil.rmtree(os.path.join(THEMES_HOME, "Default"))
            should_copy = True
    if should_copy:
        shutil.move(DEFAULT_THEME_FOLDER, THEMES_HOME)
    else:
        shutil.rmtree(DEFAULT_THEME_FOLDER)


