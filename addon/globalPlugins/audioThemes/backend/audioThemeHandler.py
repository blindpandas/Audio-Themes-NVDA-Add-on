# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import shutil
import gc
import copy
import json

import speech
import controlTypes

from enum import IntEnum
from .unspoken import mixer
from . import helpers
from . import file_directory, libaudioverse

_installedThemes = []
themesInstallDir = os.path.join(os.path.dirname(file_directory), "Themes")

NVDA_getSpeechTextForProperties = speech.getSpeechTextForProperties
SIMULATION = libaudioverse.Simulation(block_size = 1024)
MIXER = mixer.Mixer(SIMULATION, 1)
INFO_FILE_NAME = "info.json"

class SpecialProps(IntEnum):
	protective = 2500
	first = 2501
	last = 2502
	notify = 2503
	loaded = 2504

themeRoles = copy.deepcopy(controlTypes.roleLabels)
themeRoles.update({
  # Translators: The label of the sound which will be played when focusing a protected edit control.
  SpecialProps.protective: _("Password Edit Fields"),
  # Translators: The label of the sound which will be played when focusing the first item in a list.
  SpecialProps.first: _("First Item"),
  # Translators: The label of the sound which will be played when focusing the last item in a list.
  SpecialProps.last: _("Last Item"),
  # Translators: The label of the sound which will be played when a help balloon or a toast is shown.
  SpecialProps.notify: _("New Notification Sound"),
  # Translators: The label of the sound which will be played when a web page is loaded.
  SpecialProps.loaded: _("Web Page Loaded"),
})

class AudioTheme(object):
	"""An audio theme knows how to load its sounds and unload them, as well as holding other information about its author and directory.
	Do not use this class directly, use it via the convenience functions provided in this module.
	"""

	def __init__(self, name, infoDict):
		self.name = name
		self.author = infoDict["author"]
		self.summary = infoDict["summary"]
		self.isActive = False
		self.directory = os.path.join(themesInstallDir, self.name)
		self.soundobjects = dict()

	def __repr__(self):
		return "AudioTheme<name=%s><author=%s>" %(self.name, self.author)

	def load(self):
		if self.soundobjects:
			self.unload()
		if not self.directory:
			return
		for fileName in os.listdir(self.directory):
			path = os.path.join(self.directory ,fileName)
			if os.path.isfile(path) and path.endswith("wav"):
				key = int(os.path.splitext(fileName)[0])
				if key in themeRoles:
					self.loadFile(key, path)

	def loadFile(self, key, filePath):
		libaudioverse_object = libaudioverse.BufferNode(SIMULATION)
		buffer = libaudioverse.Buffer(SIMULATION)
		buffer.load_from_file(filePath)
		libaudioverse_object.buffer = buffer
		self.soundobjects[key] = libaudioverse_object

	def unload(self):
		self.soundobjects = {}
		gc.collect()

	def deactivate(self):
		"""Deactivate this theme"""
		self.unload()
		self.isActive = False

	def activate(self):
		"""Activate this theme"""
		activeTheme = findThemeWithProp("isActive", True)
		if activeTheme:
			activeTheme.deactivate()
		self.load()
		self.isActive = True


def makeAudioTheme(*args, **kwargs):
	return AudioTheme(*args, **kwargs)

def getInstalled(updated=False):
	global _installedThemes
	if updated:
		_installedThemes = []
	_installedThemes = _installedThemes or []
	if _installedThemes:
		return _installedThemes
	for folder in os.listdir(themesInstallDir):
		expected = os.path.join(themesInstallDir, folder)
		infoFile = os.path.join(expected, INFO_FILE_NAME)
		if os.path.isdir(expected):
			if os.path.exists(infoFile):
				info = loadInfoFile(infoFile)
			else:
				info = {
				  # Translators: The default message in the audio themes manager dialog which will be shown when no author was set for the audio theme.
				  "author": _("Not Set"),
				  # Translators: The default message in the audio themes manager dialog which will be shown when no description was set for the audio theme.
				  "summary": _("No description.")}
			_installedThemes.append(AudioTheme(name=folder.decode("mbcs"), infoDict=info))
	#create a dummy audio theme.
	dummyTheme = AudioTheme(
	  # Translators: The name of a dumy audio theme being used for disabling the add-on.
	  name=_("Deactivate Audio Themes"),
	  infoDict={
	    # Translators: A funny name for the author of the dummy audio theme.
	    # Translators: This is a prank. I used a name from The Hitchhiker's Guide to the Galaxy.
		"author": _("Zaphod"),
		# Translators: The description for the dumy audio theme, telling the user that this will disable the add-on.
		"summary": _("Silences the audable output")})
	dummyTheme.directory = None
	_installedThemes.append(dummyTheme)
	_installedThemes = _installedThemes
	initialize()
	return _installedThemes

def installAudioThemePackage(packagePath):
	helpers.extractArchive(archivePath=packagePath, directory=themesInstallDir)

def removeAudioTheme(audioTheme):
	audioTheme.deactivate()
	if audioTheme.directory:
		shutil.rmtree(audioTheme.directory)

def findThemeWithProp(prop, value):
	for theme in getInstalled():
		if getattr(theme, prop, None)==value:
			return theme

def initialize():
	# Activate configured theme.
	theme = findThemeWithProp("name", helpers.getCfgVal("using"))
	if not theme:
		theme = getInstalled()[-1]
	theme.activate()

def hook_getSpeechTextForProperties(reason=controlTypes.REASON_QUERY, *args, **kwargs):
	role = kwargs.get('role', None)
	sounds = getattr(findThemeWithProp("isActive", True), "soundobjects", None)
	if role and sounds:
		if 'role' in kwargs and role in sounds:
			del kwargs['role']
	return NVDA_getSpeechTextForProperties(reason, *args, **kwargs)

def loadInfoFile(infoFile):
	with open(infoFile, "rb") as f:
		return json.load(f)

def writeInfoFile(infoDict, infoFilePath):
	with open(infoFilePath, "wb") as f:
		json.dump(infoDict, f)
