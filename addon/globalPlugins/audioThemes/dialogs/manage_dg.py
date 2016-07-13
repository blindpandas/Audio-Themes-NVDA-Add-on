# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import wx
import winKernel
import shutil
import zipfile

import gui
import speech
import ui

from gui.settingsDialogs import VoiceSettingsSlider

from ..backend import helpers
from ..backend import audioThemeHandler

import addonHandler
addonHandler.initTranslation()

class ManagerDialog(wx.Dialog):

	def __init__(self, parent,
	# Translators: The title of the audio themes manager dialog 
	title=_("Audio Themes Manager")):
		super(ManagerDialog, self).__init__(parent, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		tasksSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: the text of the label of a listbox that shows all available themes
		tasksLabel = wx.StaticText(self, -1, label=_("Installed Themes:"))
		tasksSizer.Add(tasksLabel)
		self.themesList=wx.ListCtrl(self,-1,style=wx.LC_REPORT|wx.LC_SINGLE_SEL, size=(550,350))
		# Translators: The label for a column in themes list used to identify theme package name.
		self.themesList.InsertColumn(0,_("Theme"),width=150)
		# Translators: The label for a column in themes list used to identify theme's author.
		self.themesList.InsertColumn(1,_("Author"),width=50)
		# Translators: The label for a column in themes list used to identify theme's description.
		self.themesList.InsertColumn(2,_("Description"),width=50)
		tasksSizer.Add(self.themesList, proportion=8)
		mainSizer.Add(tasksSizer)
		extraOptionsSizer = wx.BoxSizer(wx.HORIZONTAL)
		cbSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label of a checkbox to toggle the 3D or mono Mode.
		self.play3DCb = wx.CheckBox(self, -1, _("Play sounds in 3D mode"))
		# Translators: The label of a checkbox to toggle the speaking of object's role.
		self.speakRoleCb = wx.CheckBox(self, -1, _("Speak role such as button, edit box , link etc. "))
		# Translators: The label of a checkbox to toggle whether the audio theme's volume should follow the voice volume.
		self.useSynthVolumeCb = wx.CheckBox(self, -1, _("Use Synthesizer Volume"))
		cbSizer.Add(self.play3DCb, proportion=2)
		cbSizer.Add(self.speakRoleCb, proportion=2)
		cbSizer.Add(self.useSynthVolumeCb, proportion=2)
		extraOptionsSizer.Add(cbSizer)
		volumeSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label of a slider to set the audio theme volume.
		volumeLabel = wx.StaticText(self, -1, label=_("Audio Theme Volume:"))
		self.volumeSlider = VoiceSettingsSlider(self,wx.ID_ANY,minValue=0,maxValue=100,name=_("Add-on Volume"))
		volumeSizer.Add(volumeLabel)
		volumeSizer.Add(self.volumeSlider)
		extraOptionsSizer.Add(volumeSizer)
		mainSizer.Add(extraOptionsSizer)
		buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		useThemeID= wx.NewId()
		# Translators: The label of the button to set the selected theme as a user's active theme.
		self.useTheme = wx.Button(self, useThemeID, _("&Use Selected"))
		buttonsSizer.Add(self.useTheme)
		removeThemeID = wx.NewId()
		# Translators: The label of the buttons to remove the selected theme from installed themes list.
		self.removeTheme = wx.Button(self, removeThemeID, _("&Remove Selected"))
		buttonsSizer.Add(self.removeTheme)
		addThemeID = wx.NewId()
		# Translators: The label of the button to add a new theme to user's themes.
		addTheme = wx.Button(self, addThemeID, _("&Add New"))
		buttonsSizer.Add(addTheme)
		# Translators: The text of a button to close a dialog.
		cancelButton = wx.Button(self, wx.ID_CANCEL, _("&Close"))
		buttonsSizer.Add(cancelButton)
		mainSizer.Add(buttonsSizer)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.themesList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)
		self.Bind( wx.EVT_BUTTON, self.onUseClick, id=useThemeID)
		self.Bind( wx.EVT_BUTTON, self.onRemoveClick, id=removeThemeID)
		self.Bind( wx.EVT_BUTTON, self.onAddClick, id=addThemeID)
		self.Bind( wx.EVT_CHECKBOX, self.onPlay3DCbCheck, self.play3DCb)
		self.Bind( wx.EVT_CHECKBOX, self.onSpeakRoleCbCheck, self.speakRoleCb)
		self.Bind( wx.EVT_CHECKBOX, self.onUseSynthVolumeCb, self.useSynthVolumeCb)
		self.volumeSlider.Bind(wx.EVT_SLIDER, self.onVolumeChange)
		self.currentThemes = []
		self.refresh()
		self.finishSetup()

	def finishSetup(self):
		self.useTheme.SetDefault()
		self.play3DCb.SetValue(helpers.getCfgVal("threeD"))
		self.speakRoleCb.SetValue(helpers.getCfgVal("speakRole"))
		self.useSynthVolumeCb.SetValue(helpers.getCfgVal("useSynthVolume"))
		self.volumeSlider.SetValue(helpers.getCfgVal("volume"))
		if helpers.getCfgVal("useSynthVolume"):
			self.volumeSlider.Disable()

	def onPlay3DCbCheck(self, evt):
		cbVal = self.play3DCb.GetValue()
		helpers.setCfgVal("threeD", cbVal)

	def onSpeakRoleCbCheck(self, evt):
		cbVal = evt.GetEventObject().GetValue()
		helpers.setCfgVal("speakRole", cbVal)
		if not cbVal:
			speech.getSpeechTextForProperties = audioThemeHandler.hook_getSpeechTextForProperties
		else:
			speech.getSpeechTextForProperties = audioThemeHandler.NVDA_getSpeechTextForProperties

	def onUseSynthVolumeCb(self, evt):
		cbVal = evt.GetEventObject().GetValue()
		helpers.setCfgVal("useSynthVolume", cbVal)
		if cbVal:
			self.volumeSlider.Disable()
		else:
			self.volumeSlider.Enable()

	def onVolumeChange(self, evt):
		sliderVal = self.volumeSlider.GetValue()
		helpers.setCfgVal("volume", sliderVal)

	def onListItemSelected(self, evt):
		selected = self.themesList.GetFirstSelected()
		controls = [self.removeTheme, self.play3DCb, self.speakRoleCb, self.useSynthVolumeCb, self.volumeSlider]
		isInDisable = selected == len(self.currentThemes)-1
		for c in controls:
				if isInDisable:
					c.Disable()
				else:
					c.Enable()

	def onUseClick(self, event):
		selected = self.themesList.GetFirstSelected()
		if selected<0: return
		selectedTheme = self.currentThemes[selected]
		if selectedTheme == self.currentThemes[-1]:
			selectedTheme.name = ""
		helpers.setCfgVal("using", self.currentThemes[selected].name)
		selectedTheme.activate()

	def onRemoveClick(self, event):
		selected = self.themesList.GetFirstSelected()
		if selected<0: return
		selectedTheme = self.currentThemes[selected]
		if selectedTheme.isActive:
			if gui.messageBox(
			# Translators: message confirming the removal of the active theme.
			_("The {themeName} is the currently active theme. Do you realy want to remove it?").format(themeName=selectedTheme.name),
			# Translators: the title of the message box that ask the user if he/she realy want to remove the active theme. 
			_("Removing The Active Theme"), wx.YES_NO|wx.ICON_WARNING) == wx.YES:
				helpers.setCfgVal("using", "")
			else:
				return
		else:
			if gui.messageBox(
			# Translators: message asking the user if he/she realy want to remove the selected theme.
			_("Do you want to remove the {themeName} theme permanently?").format(themeName=selectedTheme.name),
			# Translators: the title of the message box that ask the user if he/she realy want to remove the theme. 
			_("Are You Sure"),
			wx.YES_NO|wx.ICON_WARNING) == wx.NO:
				return
		try:
			audioThemeHandler.removeAudioTheme(selectedTheme)
		except:
			gui.messageBox(
			# Translators: message telling the user that the deletion process was faild.
			_("Error Removing Theme"),
			# Translators: the title of the message telling that the deletion was faild
			_("Error"))
		self.refresh()

	def onAddClick(self, event):
		filename = helpers.showFileDialog(self,
		  # Translators: The title of a dialog to browse to an audio theme package.
		  message=_("Select An Audio Theme Package"),
		  # Translators: The extention hint for audio theme packages shown in a dialog to browse to an audio theme package.
		  ext="atp", extHint=_("Audio Theme Packages"))
		if not filename:
			return
		audioThemeHandler.installAudioThemePackage(packagePath=filename)
		self.refresh()

	def refresh(self):
		self.themesList.DeleteAllItems()
		self.currentThemes = []
		installedThemes = audioThemeHandler.getInstalled(updated=True)
		buttons = [self.useTheme, self.removeTheme]
		for btn in buttons:
			if installedThemes:
				btn.Enable()
			else:
				btn.Disable()
		for theme in installedThemes:
			self.themesList.Append((theme.name, theme.author, theme.summary))
			self.currentThemes.append(theme)
		self.themesList.Select(0)
		self.themesList.SetItemState(0, wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)