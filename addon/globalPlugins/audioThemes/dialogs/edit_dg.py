# -*- coding: utf-8 -*-

# Copyright (c) 2014-2016 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

import gui
from . import BaseEditorDialog

from ..backend import helpers
from ..backend import audioThemeHandler

class EditorDialog(BaseEditorDialog):

	def getAudioTheme(self):
		return audioThemeHandler.findThemeWithProp("isActive", True)

	def makeTitle(self):
		return _("Editing {themeName}, The Active Audio Theme").format(themeName=self.audioTheme.name)
