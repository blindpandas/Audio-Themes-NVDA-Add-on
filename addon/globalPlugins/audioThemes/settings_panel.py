# coding: utf-8

import wx
import gui


import addonHandler
addonHandler.initTranslation()


class AudioThemesSettingsPanel(gui.SettingsPanel):
    # Translators: Title for the settings panel in NVDA's multi-category settings
    title = _("Audio Themes")

    def makeSettings(self, settingsSizer):
        settingsSizer.Add(self.lineLengthIndicatorCheckBox, border=10, flag=wx.BOTTOM)

    def onSave(self):
        config.conf["notepadPp"]["maxLineLength"] = int(self.maxLineLengthEdit.Value)
