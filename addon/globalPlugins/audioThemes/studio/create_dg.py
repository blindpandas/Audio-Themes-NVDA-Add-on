# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import tempfile
import wx
import json

import gui

from . import BaseEditorDialog
from ..backend import helpers
from ..backend import audioThemeHandler


class CreateNewDialog(BaseEditorDialog):
    isCreatingANewTheme = True

    def __init__(self, parent, infoDict):
        self.infoDict = infoDict
        self.name = self.infoDict.pop("name")
        super(CreateNewDialog, self).__init__(parent=parent)

    def getAudioTheme(self):
        self.baseTemp, tempDir = self.makeTempDir()
        infoFilePath = os.path.join(tempDir, audioThemeHandler.INFO_FILE_NAME)
        audioThemeHandler.writeInfoFile(self.infoDict, infoFilePath)
        audioTheme = audioThemeHandler.makeAudioTheme(
            name=self.name, infoDict=self.infoDict
        )
        audioTheme.directory = tempDir
        return audioTheme

    def makeTitle(self):
        # Translators: The title of the main dialog being used to create a new audio theme.
        return _("Creating {themeName}, a new audio theme").format(
            themeName=self.audioTheme.name
        )

    def onPackClick(self, evt):
        filename = wx.FileSelector(
            # Translators: The title of a dialog used to browse to a location to save the audio theme package.
            _("Save Audio Theme Package"),
            default_filename="%s.atp" % self.name,
            # Translators: The extention hint for audio theme packages shown in a dialog asking the user to save the audio theme package.
            wildcard=("{hint}(*.{ext})" + "|*.{ext}").format(
                hint=_("Audio Theme Package"), ext="atp"
            ),
            flags=wx.SAVE | wx.OVERWRITE_PROMPT,
            parent=self,
        )
        if not filename:
            return
        helpers.makeZipFile(filename, self.audioTheme.directory)
        gui.messageBox(
            # Translators: Message box telling the user that the oparation succeeded.
            _(
                "The audio theme package was created successfully. You can find the package at: {filename}"
            ).format(filename=filename),
            # Translators: The title of a messagebox telling the user that the process was completed successfully.
            _("Done"),
        )

    def makeTempDir(self):
        baseTemp = tempfile.mkdtemp()
        tempDir = os.path.join(baseTemp, self.name)
        os.mkdir(tempDir)
        return baseTemp, tempDir


class CreaterDialog(gui.SettingsDialog):
    # Translators: The title of a dialog to create a new audio theme.
    title = _("Create A New Audio Theme")

    def makeSettings(self, settingsSizer):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: instruction to the user for entering theme details shown in a dialog.
        instructionLabel = wx.StaticText(
            self,
            -1,
            label=_(
                "&Please enter the details you want to be shown in the themes manager for your new theme and then click the OK button to start adding sounds to your audio theme."
            ),
        )
        # Translators: The label of an edit box for entering theme name.
        nameLabel = wx.StaticText(self, -1, label=_("&Theme Name"))
        self.nameEdit = wx.TextCtrl(self, wx.NewId())
        # Translators: A label of an edit box for entering theme's author.
        authorLabel = wx.StaticText(self, -1, label=_("Your &Name"))
        self.authorEdit = wx.TextCtrl(self, wx.NewId())
        # Translators: A label of an edit box for entering theme's description.
        descLabel = wx.StaticText(self, -1, label=_("Theme &description"))
        self.descEdit = wx.TextCtrl(self, wx.NewId(), style=wx.TE_MULTILINE)
        mainSizer.AddMany(
            [
                (instructionLabel),
                (nameLabel),
                (self.nameEdit),
                (authorLabel),
                (self.authorEdit),
                (descLabel),
                (self.descEdit),
            ]
        )
        settingsSizer.Add(mainSizer, border=10, flag=wx.BOTTOM)

    def postInit(self):
        self.nameEdit.SetFocus()

    def onOk(self, evt):
        name = self.nameEdit.GetValue()
        if not name:
            gui.messageBox(
                # Translators: A message box telling the user that he must enter a theme name in order to continue
                _("Please enter a name for your theme package."),
                # Translators: The title of a message box indicating an error.
                _("Error"),
            )
            return
        try:
            name.encode("mbcs")
        except UnicodeEncodeError:
            gui.message(
                # Translators: A message telling the user to change the name of the new theme because the entered name is not valid.
                _(
                    "The theme name you have entered is not valid. Please try another name."
                ),
                # Translators: The title of a message box indicating an error.
                _("Error"),
            )
            self.nameEdit.Clear()
            return self.nameEdit.SetFocus()
        infoDict = {
            "name": name,
            # Translators: The default message in the audio themes manager dialog which will be shown when no author was set for the audio theme.
            "author": self.authorEdit.GetValue() or _("Not Set"),
            # Translators: The default message in the audio themes manager dialog which will be shown when no description was set for the audio theme
            "summary": self.descEdit.GetValue() or _("No Description"),
        }
        super(CreaterDialog, self).onOk(evt)
        dg = CreateNewDialog(parent=gui.mainFrame, infoDict=infoDict)
        dg.CenterOnScreen()
        dg.Show()
