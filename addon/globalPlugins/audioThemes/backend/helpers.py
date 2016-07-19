# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import os
import wx
import zipfile

import winKernel
import config
import speech
import gui
import globalVars
import NVDAObjects

# Configuration spec
defaults = {
	"using": 'string(default="Default")',
	"threeD": "boolean(default=True)",
	"speakRole": "boolean(default=False)",
	"useSynthVolume": "boolean(default=False)",
	"volume": "integer(default=75)"
}

def getCfgVal(key):
	return config.conf["audioThemes"][key]

def setCfgVal(key, val):
	config.conf["audioThemes"][key] = val

def clamp(my_value, min_value, max_value):
	return max(min(my_value, max_value), min_value)

def playTarget(target, fromFile=False):
	if not fromFile:
		target.disconnect(0)
		target.position = 0.0
		target.connect_simulation(0)
		return
	from .audioThemeHandler import libaudioverse, SIMULATION
	filePath = os.path.abspath(target)
	fileNode = libaudioverse.BufferNode(SIMULATION)
	buffer = libaudioverse.Buffer(SIMULATION)
	buffer.load_from_file(filePath)
	fileNode.buffer = buffer
	fileNode.connect_simulation(0)

def setupConfig():
	config.conf.spec["audioThemes"] = defaults


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
	wildcard = ""
	if not isinstance(ext, basestring):
		# Asume a list.
		for e, h in zip(ext, extHint):
			wildcard+= "{hint}(*.{ext})|*.{ext}|".format(hint= h, ext=e)
	else:
		wildcard="{hint}(*.{ext})|*.{ext}".format(hint= extHint, ext=ext)
	fd=wx.FileDialog(parent,
		message=message,
		wildcard=(wildcard),
		style=wx.FD_OPEN)
	if fd.ShowModal()!=wx.ID_OK:
		fd.Destroy()
		return
	path = fd.GetPath()
	fd.Destroy()
	return path
