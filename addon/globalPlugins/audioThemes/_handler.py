# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

from enum import IntEnum
from collections import OrderedDict
from dataclasses import dataclass, field
import os
import shutil
import copy
import json
import controlTypes


_file_directory = os.path.split(os.path.abspath(__file__))[0]
THEMES_DIR = os.path.join(os.path.dirname(_file_directory), "Themes")
INFO_FILE_NAME = "info.json"
SUPPORTED_FILE_TYPES = OrderedDict()
# Translators: The file type to be shown in a dialog used to browse for audio files.
SUPPORTED_FILE_TYPES["ogg"] = _("Ogg audio files")
# Translators: The file type to be shown in a dialog used to browse for audio files.
SUPPORTED_FILE_TYPES["wav"] = _("Wave audio files")


class SpecialProps(IntEnum):
    """Represents sounds defined by this addon."""
    protected = 2500
    first = 2501
    last = 2502
    notify = 2503
    loaded = 2504

themeRoles = copy.copy(controlTypes.roleLabels)
themeRoles.update(
    {
        # Translators: The label of the sound which will be played when focusing a protected edit control.
        SpecialProps.protected: _("Protected Editable Controls"),
        # Translators: The label of the sound which will be played when focusing the first item in a list.
        SpecialProps.first: _("First Item"),
        # Translators: The label of the sound which will be played when focusing the last item in a list.
        SpecialProps.last: _("Last Item"),
        # Translators: The label of the sound which will be played when a help balloon or a toast is shown.
        SpecialProps.notify: _("New Notification Sound"),
        # Translators: The label of the sound which will be played when a web page is loaded.
        SpecialProps.loaded: _("Web Page Loaded"),
    }
)


@dataclass(order=True)
class AudioTheme:
    name: str
    author: str
    summary: str
    is_active: bool = False
    sounds: dict = field(default_factory=dict)

    @property
    def directory(self):
        return os.path.join(THEMES_DIR, name)

    def load(self, theme):
        if self.sounds:
            self.unload()
        if not os.path.isdir(self.directory):
            return
        for filename in os.listdir(self.directory):
            path = os.path.join(self.directory, filename)
            fnrole, ext = os.path.splitext(filename)
            if (
                os.path.isfile(path)
                and ext[1:] in SUPPORTED_FILE_TYPES.keys()
            ):
                key = int(fnrole)
                if key in themeRoles:
                    self.sounds[key] = player.make_sound_object(filePath)

    def unload(self):
        self.sounds.clear()

    def activate(self):
        """Activate this theme"""
        self.load()
        self.is_active = True

    def deactivate(self):
        """Deactivate this theme"""
        self.unload()
        self.is_active = False


class AudioThemesHandler:

    def __init__(self, plugin, player):
        self.plugin = plugin
        self.player = player
        self._installed_themes = []

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
            if os.path.isdir(expected) and os.path.exists(infoFile):
                info = loadInfoFile(infoFile)
                _installedThemes.append(
                    AudioTheme(name=folder, infoDict=info)
                )
        # create a dummy audio theme.
        dummyTheme = AudioTheme(
            # Translators: The name of a dumy audio theme being used for disabling the add-on.
            name=_("Deactivate Audio Themes"),
            infoDict={
                # Translators: A funny name for the author of the dummy audio theme.
                # Translators: This is a prank. I used a name from The Hitchhiker's Guide to the Galaxy.
                "author": _("Zaphod"),
                # Translators: The description for the dumy audio theme, telling the user that this will disable the add-on.
                "summary": _("Silences the audable output"),
            },
        )
        dummyTheme.directory = None
        _installedThemes.append(dummyTheme)
        return _installedThemes


    def installAudioThemePackage(packagePath):
        helpers.extractArchive(archivePath=packagePath, directory=themesInstallDir)


    def removeAudioTheme(audioTheme):
        audioTheme.deactivate()
        if audioTheme.directory:
            shutil.rmtree(audioTheme.directory)


    def findThemeWithProp(prop, value):
        for theme in getInstalled():
            if getattr(theme, prop, None) == value:
                return theme


    def initialize():
        # Activate configured theme.
        theme = findThemeWithProp("name", helpers.getCfgVal("using"))
        if not theme:
            theme = getInstalled()[-1]
        theme.activate()


    def loadInfoFile(infoFile):
        with open(infoFile, "rb") as f:
            return json.load(f)


    def writeInfoFile(infoDict, infoFilePath):
        with open(infoFilePath, "wb") as f:
            json.dump(infoDict, f)

    def makeZipFile(output_filename, source_dir):
        # Taken from stackoverflow
        relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
        with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk(source_dir):
                # add directory (needed for empty dirs)
                zip.write(root, os.path.relpath(root, relroot))
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename):  # regular files only
                        arcname = os.path.join(os.path.relpath(root, relroot), file)
                        zip.write(filename, arcname)


    def extractArchive(archivePath, directory):
        """Extracts the given zip file to the specified directory."""
        with zipfile.ZipFile(archivePath, "r") as z:
            for info in z.infolist():
                if isinstance(info.filename, str):
                    info.filename = info.filename.decode(
                        "cp%d" % winKernel.kernel32.GetOEMCP()
                    )
                z.extract(info, directory)


