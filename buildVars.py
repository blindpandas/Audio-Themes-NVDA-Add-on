# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "AudioThemes3D",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Audio Themes"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""This add-on creates a virtual audio display that plays sounds when focusing or navigating objects, the audio will be played in a location that corresponds to the object's location in the visual display. The add-on also enables you to activate, install, remove, edit, create, and distribute audio theme packages."""),
	# version
	"addon_version" : "5.1",
	# Author(s)
	"addon_author" : u"Musharraf Omer<ibnomer2011@hotmail.com>",
	# URL for the add-on documentation support
	"addon_url" : "https://mush42.github.io/audio-themes/",
	# Documentation file name
	"addon_docFileName" : "readme.html",
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join(os.path.abspath("addon/globalPlugins/AudioThemes"), fname) for fname in ("__init__.py", "*/*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
