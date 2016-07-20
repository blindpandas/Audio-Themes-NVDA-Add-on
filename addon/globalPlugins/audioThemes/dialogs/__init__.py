# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import copy
import wx
import shutil

import gui
import controlTypes
import ui

from ..backend import helpers
from ..backend import audioThemeHandler
from ..backend.audioThemeHandler import themeRoles

import addonHandler
addonHandler.initTranslation()


class NewSoundDialog(gui.SettingsDialog):
	# Translators: The default title of a dialog used to add a new sound to the active audio theme.
	title = _("Add A New Sound")

	def __init__(self, parent, roleList, copyingPath):
		self.roleList = roleList
		self.copyingPath = copyingPath
		self.newSoundPath = ""
		super(NewSoundDialog, self).__init__(parent=parent)

	def makeSettings(self, settingsSizer):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The text of a label for a combobox contains object roles.
		roleListLabel = wx.StaticText(self,-1,label=_("&Select Object Type:"))
		roleListId = wx.NewId()
		self.roleListCombo =wx.Choice(self, roleListId,
		  choices=[label for id, label in self.roleList])
		self.roleListCombo.SetSelection(0)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		browseId = wx.NewId()
		# Translators: The label of the buttons to browse to an audio file.
		browseBtn = wx.Button(self, browseId, _("&Browse to an audio file"))
		previewId = wx.NewId()
		# Translators: The label of the button to preview/play the selected audio file.
		self.previewBtn = wx.Button(self, previewId, _("&Preview"))
		btnSizer.Add(browseBtn)
		btnSizer.Add(self.previewBtn)
		mainSizer.Add(roleListLabel)
		mainSizer.Add(self.roleListCombo)
		mainSizer.Add(btnSizer)
		settingsSizer.Add(mainSizer,border=10,flag=wx.BOTTOM)
		self.Bind(wx.EVT_BUTTON, self.onBrowseClick, id=browseId)
		self.Bind(wx.EVT_BUTTON, self.onPreviewClick, id=previewId)

	def postInit(self):
		self.roleListCombo.SetFocus()
		self.previewBtn.Disable()

	def onBrowseClick(self, evt):
		self.newSoundPath = helpers.showFileDialog(self,
		  # Translators: The title of a dialog asking the user to select an audio file.
		  _("Select Audio File"), audioThemeHandler.SUPPORTED_FILE_TYPES.keys(), audioThemeHandler.SUPPORTED_FILE_TYPES.values())
		if self.newSoundPath:
			self.previewBtn.Enable()

	def onPreviewClick(self, evt):
		if self.newSoundPath:
			helpers.playTarget(self.newSoundPath, fromFile=True)

	def onOk(self, evt):
		if self.newSoundPath :
			role = self.roleList[self.roleListCombo.GetSelection()][0]
			ext = os.path.splitext(self.newSoundPath)[-1]
			copyingFile = os.path.join(self.copyingPath, "%d%s" %(role, ext))
			try:
				shutil.copy(self.newSoundPath, copyingFile)
			except IOError :
				gui.messageBox(_("Can not copy file."), _("Error"))
		super(NewSoundDialog, self).onOk(evt)

class BaseEditorDialog(wx.Dialog):

	def __init__(self, parent):
		super(BaseEditorDialog, self).__init__(parent)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		tasksSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: the text of the label of a listbox that shows all available themes
		tasksLabel = wx.StaticText(self, -1, label=_("Existing  Sounds:"))
		tasksSizer.Add(tasksLabel)
		listId = wx.NewId()
		self.listBox = wx.ListBox(self, listId, style=wx.LB_SINGLE, size=(500, 250))
		tasksSizer.Add(self.listBox, proportion=8)
		mainSizer.Add(tasksSizer)
		buttonsSizer = wx.BoxSizer(wx.VERTICAL)
		changeId= wx.NewId()
		# Translators: The label of the button to edit the current sound.
		self.changeBtn = wx.Button(self, changeId, _("&Change Selected"))
		buttonsSizer.Add(self.changeBtn)
		removeId = wx.NewId()
		# Translators: The label of the buttons to remove the selected sound.
		self.removeBtn = wx.Button(self, removeId, _("&Remove Selected"))
		buttonsSizer.Add(self.removeBtn)
		addId = wx.NewId()
		# Translators: The label of the button to add a new sound.
		self.addBtn = wx.Button(self, addId, _("&Add New Sound"))
		buttonsSizer.Add(self.addBtn)
		mainSizer.Add(buttonsSizer)
		taskButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		if getattr(self, "isCreatingANewTheme", None):
			packageId = wx.NewId()
			# Translators: The text of a button used to package the audio theme and save it.
			packageBtn = wx.Button(self, packageId, _("&Package Audio Theme"))
			taskButtonsSizer.Add(packageBtn)
			self.Bind(wx.EVT_BUTTON, self.onPackClick, id=packageId)
		# Translators: The text of a button to close the dialog.
		cancelBtn = wx.Button(self, wx.ID_CLOSE, _("&Close"))
		taskButtonsSizer.Add(cancelBtn)
		mainSizer.Add(taskButtonsSizer)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.changeBtn.SetDefault()
		self.Bind(wx.EVT_LISTBOX, self.OnSelectionChange, id=listId)
		self.Bind( wx.EVT_BUTTON, self.onChangeClick, id=changeId)
		self.Bind( wx.EVT_BUTTON, self.onRemoveClick, id=removeId)
		self.Bind( wx.EVT_BUTTON, self.onAddClick, id=addId)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_BUTTON, self.onClose, 	cancelBtn)
		self.EscapeId = wx.ID_CLOSE
		self.audioTheme = self.getAudioTheme()
		self.Title = self.makeTitle()
		audioThemeHandler.findThemeWithProp("isActive", True).deactivate()
		self.refresh()

	def onChangeClick(self, event):
		selectionIndex = self.listBox.GetSelection()
		if  selectionIndex == wx.NOT_FOUND: return
		newSnd = helpers.showFileDialog(self, _("Select Audio File"), audioThemeHandler.SUPPORTED_FILE_TYPES.keys(), audioThemeHandler.SUPPORTED_FILE_TYPES.values())
		if not newSnd:
			return
		oldFile = self.getFileFromIndex(selectionIndex)
		ext = os.path.splitext(newSnd)[-1]
		targetFile = os.path.join(self.audioTheme.directory, "%d%s" %(self.keys[selectionIndex], ext))
		try:
			os.remove(oldFile)
			shutil.copy(newSnd, targetFile)
		except IOError :
			gui.messageBox(
			  # Translators: Message box shown to the user when the copying fails.
			  _("Can not copy the file"),
			  # Translators: The title of a message box indicating an error.
			  _("Error"))
		self.audioTheme.load()

	def onRemoveClick(self, event):
		if (self.listBox.GetSelection() == wx.NOT_FOUND):
			return
		if gui.messageBox(
		# Translators: message asking the user if he/she realy want to remove the selected sound.
		_("Do you want to remove the %s sound?")%self.listBox.GetStringSelection(),
		# Translators: the title of the message box that ask the user if he/she realy want to remove the theme. 
		_("Confirm"),
		wx.YES_NO|wx.ICON_WARNING) == wx.NO:
			return
		try:
			os.remove(self.getFileFromIndex(self.listBox.GetSelection()))
		except WindowsError:
			gui.messageBox(
			# Translators: message telling the user that the deletion process was faild.
			_("Error Removing File"),
			# Translators: the title of the message telling that the deletion was faild
			_("Error"))
		self.refresh()

	def onAddClick(self, event):
		roleList = []
		for  id, label in themeRoles.iteritems():
			if not id in self.keys:
				roleList.append((id, label))
		NewSoundDialog(self, roleList=roleList,
		  copyingPath=self.audioTheme.directory).ShowModal()
		self.refresh()

	def onClose(self, evt):
		self.Destroy()
		tempDir = getattr(self, "baseTemp", None)
		if tempDir:
			try:
				self.audioTheme.unload()
				os.remove(tempDir)
			except:
				pass
		audioThemeHandler.initialize()

	def OnSelectionChange(self, evt):
		selection = self.listBox.GetSelection()
		attrToInvoke  = "Disable"if selection==wx.NOT_FOUND else "Enable"
		for b in [self.changeBtn, self.removeBtn]:
			getattr(b, attrToInvoke)()
		role = self.keys[selection]
		soundObj = self.audioTheme.soundobjects[role]
		helpers.playTarget(soundObj)

	def refresh(self):
		self.listBox.Clear()
		self.audioTheme.load()
		self.keys = self.audioTheme.soundobjects.keys()
		labels = [themeRoles[k] for k in self.keys if k in themeRoles]
		self.listBox.Set(labels)
		if not len(labels):
			[b.Disable() for b in [self.changeBtn, self.removeBtn]]

	def makeTitle(self):
		# Translators: The default title of a dialog used to edit audio themes.
		return _("Audio Theme Editor")

	def getFileFromIndex(self, index):
		expected = [os.path.join(self.audioTheme.directory, "%d.%s" %(self.keys[index], ext)) for ext in audioThemeHandler.SUPPORTED_FILE_TYPES.keys()]
		if os.path.exists(expected[0]):
			return expected[0]
		else:
			return expected[1]
