# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.

"""
  Audio Themes Add-on
  ~~~~~~~~~~~~~~~~~~~~~~
  This add-on creates a virtual audio display that plays sounds when focusing or navigating objects, the audio
  will be played in a location that corresponds to the object's location in the visual display. It also enables the user to
  activate, install, remove, edit, create, and distribute audio theme packages.

  Started as an indipendant project, this addon evolved to be an enhanced version of the 'Unspoken' addon
  by Austin Hicks (camlorn38@gmail.com).

  The development of this addon is happening on GitHub <http://github.com/mush42/Audio-Themes-NVDA-Add-on>
  Crafted by Musharraf Omer <ibnomer2011@hotmail.com> using code published by  others from the NVDA community.
"""

from contextlib import suppress
import wx
import globalPluginHandler
import appModuleHandler
import scriptHandler
import NVDAObjects
import gui
import speech
import controlTypes
import globalCommands

from .handler import AudioThemesHandler, SpecialProps
from .settings import AudioThemesSettingsPanel
from .studio import AudioThemesStudioStartupDialog


import addonHandler
addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    browser_apps = ["firefox", "iexplore", "chrome", "opera", "edge"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = AudioThemesHandler()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
            AudioThemesSettingsPanel
        )
        self._previous_mouse_object = None
        # Add the menu item for the audio themes studio
        self.studioMenuItem = gui.mainFrame.sysTrayIcon.menu.Insert(
            2,
            wx.ID_ANY,
            # Translators: label for the audio themes studio menu item
            _("&Audio Themes Studio"),
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.on_studio_item_clicked, self.studioMenuItem
        )

    def terminate(self):
        with suppress(Exception):
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
                AudioThemesSettingsPanel
            )
            gui.mainFrame.sysTrayIcon.menu.RemoveItem(self.studioMenuItem)
            self.handler.close()

    def on_studio_item_clicked(self, event):
        # Translators: title for the audio themes studio dialog
        with AudioThemesStudioStartupDialog(self, _("Audio Themes Studio")) as dlg:
            dlg.ShowModal()

    def script_speakObject(self, gesture):
        if scriptHandler.getLastScriptRepeatCount() == 0:
            self.playObject(NVDAObjects.api.getFocusObject())
        globalCommands.commands.script_reportCurrentFocus(gesture)

    script_speakObject.__doc__ = (
        globalCommands.GlobalCommands.script_reportCurrentFocus.__doc__
    )

    def event_gainFocus(self, obj, nextHandler):
        self.playObject(obj)
        nextHandler()

    def event_becomeNavigatorObject(self, obj, nextHandler, isFocus=False):
        self.playObject(obj)
        nextHandler()

    def event_mouseMove(self, obj, nextHandler, x, y):
        if obj is not self._previous_mouse_object:
            self._previous_mouse_object = obj
            self.playObject(obj)
        nextHandler()

    def event_show(self, obj, nextHandler):
        if obj.role == controlTypes.ROLE_HELPBALLOON:
            obj.snd = SpecialProps.notify
            self.playObject(obj)
        nextHandler()

    def event_documentLoadComplete(self, obj, nextHandler):
        if appModuleHandler.getAppNameFromProcessID(obj.processID) in self.browser_apps:
            self.playObject(obj)
        nextHandler()

    def playObject(self, obj):
        order = self.getOrder(obj)
        if getattr(obj, "snd", None) is None:
            if 16384 in obj.states:
                obj.snd = SpecialProps.protected
            elif order:
                obj.snd = order
            else:
                obj.snd = obj.role
        self.handler.play(obj, obj.snd)

    def getOrder(self, obj, parrole=14, chrole=15):
        if obj.parent and obj.parent.role != parrole:
            return None
        if (obj.previous is None) or (obj.previous.role != chrole):
            return SpecialProps.first
        elif (obj.next is None) or (obj.next.role != chrole):
            return SpecialProps.last

    __gestures = {"kb:nvda+tab": "speakObject"}
