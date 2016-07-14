# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import wx
import zipfile
import winsound
import configobj

import winKernel
import speech
import gui
import globalVars
import NVDAObjects

from cStringIO import StringIO
from validate import Validator
from logHandler import log

conf = None

defaults = StringIO("""#Audio Themes add-on Configuration File.
	using = string(default="Default")
	threeD = boolean(default=True)
	speakRole = boolean(default=False)
	useSynthVolume = boolean(default=False)
	volume = integer(default=75)
#End of configuration File.
""")

def getCfgVal(key):
	return conf[key]

def setCfgVal(key, val):
	conf[key] = val
	conf.write()

def clamp(my_value, min_value, max_value):
	return max(min(my_value, max_value), min_value)

def playFile(filePath, async=True):
	if not async:
		return winsound.PlaySound(filePath, winsound.SND_NODEFAULT)
	winsound.PlaySound(filePath, winsound.SND_ASYNC|winsound.SND_NODEFAULT)

def setupConfig():
	global defaults, conf
	confspec=configobj.ConfigObj(defaults, list_values=False, encoding="UTF-8")
	confspec.newlines="\r\n"
	conf = configobj.ConfigObj(infile = os.path.join(globalVars.appArgs.configPath, 'Themes.ini'), create_empty = True, configspec=confspec, stringify=True)
	validated=conf.validate(Validator(), copy=True)
	if validated:
		conf.write()

def activate(dg):
	frame = gui.mainFrame
	if gui.isInMessageBox:
		return
	frame.prePopup()
	d = dg(frame)
	d.Show()
	frame.postPopup()

def makeZipFile(output_filename, source_dir):
	# Taken from stackoverflow
	relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
	with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
		for root, dirs, files in os.walk(source_dir):
			# add directory (needed for empty dirs)
			zip.write(root, os.path.relpath(root, relroot))
			for file in files:
				filename = os.path.join(root, file)
				if os.path.isfile(filename): # regular files only
					arcname = os.path.join(os.path.relpath(root, relroot), file)
					zip.write(filename, arcname)

def extractArchive(archivePath, directory):
	"""Extracts the given zip file to the specified directory."""
	with zipfile.ZipFile(archivePath, 'r') as z:
		for info in z.infolist():
			if isinstance(info.filename, str):
				info.filename = info.filename.decode("cp%d" % winKernel.kernel32.GetOEMCP())
			z.extract(info, directory)

def compute_volume(volume=0):
	if getCfgVal("useSynthVolume") or not volume:
		driver=speech.getSynth()
		volume = getattr(driver, 'volume', 100)
	volume = volume/100.0 #nvda reports as percent.
	volume=clamp(volume, 0.0, 1.0)
	return volume

def showFileDialog(parent, message, ext, extHint):
	fd=wx.FileDialog(parent,
		message=message,
		wildcard=("{hint}(*.{ext})"+"|*.{ext}").format(hint= extHint, ext=ext),
		style=wx.FD_OPEN)
	if fd.ShowModal()!=wx.ID_OK:
		fd.Destroy()
		return
	path = fd.GetPath()
	fd.Destroy()
	return path
