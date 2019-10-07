# coding: utf-8

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
  Licensed under the GNU General Public License.
"""

import wx
import config
import globalPluginHandler
import appModuleHandler
import scriptHandler
import NVDAObjects
import gui
import speech
import controlTypes
import globalCommands

from .backend.unspoken import UnspokenPlayer
from .backend import audioThemeHandler
from .backend.audioThemeHandler import SpecialProps
from .settings import AudioThemesSettingsPanel


import addonHandler
addonHandler.initTranslation()


# Configuration spec
audiothemes_config_defaults = {
    "active_theme": 'string(default="Default")',
    "audio3d": "boolean(default=True)",
    "speak_roles": "boolean(default=False)",
    "use_synth_volume": "boolean(default=True)",
    "volume": "integer(default=100)",
}


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    browser_apps  = ["firefox", "iexplore", "chrome", "opera", "edge"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config.conf.spec["audiothemes"] = audiothemes_config_defaults
        self.player = UnspokenPlayer()
        self.handler = AudioThemesHandler(self, player)
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(AudioThemesSettingsPanel)
        self._previous_mouse_object = None

	def terminate(self):
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(AudioThemesSettingsPanel)
		except IndexError:
			pass

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
        if appModuleHandler.getAppNameFromProcessID(obj.processID) in self.allowedApps:
            location = obj.location
            obj.location = None
            self.playObject(obj)
            obj.location = location
        nextHandler()

    def playObject(self, obj):
        soundpack = self.activeTheme.soundobjects
        order = self.getOrder(obj)
        # if the object has a snd property, then play directly!
        if getattr(obj, "snd", None):
            pass
        elif 16384 in obj.states:
            obj.snd = SpecialProps.protected
        elif order and soundpack.get(order, None):
            obj.snd = order
        else:
            obj.snd = obj.role
        if not obj.snd in soundpack:
            return
        if True: #helpers.getCfgVal("threeD"):
            self.play(obj, soundpack, _3d=True)
        else:
            self.play(obj, soundpack, _3d=False)

    def play(self, obj, soundPack, _3d):
        self.player.play(obj, soundPack[obj.snd])

    def getOrder(self, obj, parrole=14, chrole=15):
        if obj.parent and obj.parent.role != parrole:
            return None
        if (obj.previous is None) or (obj.previous.role != chrole):
            return SpecialProps.first
        elif (obj.next is None) or (obj.next.role != chrole):
            return SpecialProps.last

    __gestures = {"kb:nvda+tab": "speakObject"}
