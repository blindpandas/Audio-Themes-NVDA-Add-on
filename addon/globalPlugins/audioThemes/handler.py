# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer and Others
# This file is covered by the GNU General Public License.

from enum import IntEnum
from collections import OrderedDict
from dataclasses import dataclass, field, asdict
from zipfile import ZipFile
from uuid import uuid4
import os
import shutil
import copy
import json
import winKernel
import config
import controlTypes
import extensionPoints
from config import post_configSave, post_configReset, post_configProfileSwitch
from .unspoken import UnspokenPlayer


THEMES_DIR = os.path.join(os.path.dirname(__file__), "Themes")
INFO_FILE_NAME = "info.json"
SUPPORTED_FILE_TYPES = OrderedDict()
# Translators: The file type to be shown in a dialog used to browse for audio files.
SUPPORTED_FILE_TYPES["ogg"] = _("Ogg audio files")
# Translators: The file type to be shown in a dialog used to browse for audio files.
SUPPORTED_FILE_TYPES["wav"] = _("Wave audio files")
# When the active audio theme is being changed
audiotheme_changed = extensionPoints.Action()

# Configuration spec
audiothemes_config_defaults = {
    "enable_audio_themes": "boolean(default=    True)",
    "active_theme": 'string(default="Default")',
    "audio3d": "boolean(default=True)",
    "use_in_say_all": "boolean(default=True)",
    "speak_roles": "boolean(default=False)",
    "use_synth_volume": "boolean(default=True)",
    "volume": "integer(default=100)",
}


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
    folder: str
    author: str
    summary: str
    is_active: bool = False
    sounds: dict = field(default_factory=dict)

    @property
    def directory(self):
        return os.path.join(THEMES_DIR, self.folder)

    def todict(self):
        return asdict(self)

    def load(self, player):
        if self.sounds:
            self.unload()
        if not os.path.isdir(self.directory):
            return
        for filename in os.listdir(self.directory):
            path = os.path.join(self.directory, filename)
            fnrole, ext = os.path.splitext(filename)
            if os.path.isfile(path) and ext[1:] in SUPPORTED_FILE_TYPES.keys():
                key = int(fnrole)
                if key in themeRoles:
                    self.sounds[key] = player.make_sound_object(path)

    def unload(self):
        self.sounds.clear()

    def deactivate(self):
        """Deactivate this theme"""
        self.unload()
        self.is_active = False


class AudioThemesHandler:
    """Query and manage audio themes.""" 

    def __init__(self):
        config.conf.spec["audiothemes"] = audiothemes_config_defaults
        self.enabled = True
        self.player = UnspokenPlayer()
        self.active_theme = None
        self.configure()
        for action in (post_configSave, post_configReset, post_configProfileSwitch, audiotheme_changed):
            action.register(self.configure)


    def get_active_theme(self):
        if not config.conf["audiothemes"]["enable_audio_themes"]:
            return
        theme = self.get_theme_from_folder(config.conf["audiothemes"]["active_theme"])
        if theme:
            theme.load(self.player)
            theme.is_active = True
            return theme

    def configure(self, *args, **kwargs):
        user_config = config.conf["audiothemes"]
        if self.active_theme is not None:
            self.active_theme.deactivate()
        self.enabled = user_config["enable_audio_themes"]
        self.active_theme = self.get_active_theme()
        self.player.audio3d =user_config["audio3d"]
        self.player.use_in_say_all = user_config["use_in_say_all"]
        self.player.speak_roles = user_config["speak_roles"]
        self.player.use_synth_volume = user_config["use_synth_volume"]
        self.player.volume = user_config["volume"]

    def play(self, obj, sound):
        if not self.enabled or (self.active_theme is None):
            return
        sound_obj = self.active_theme.sounds.get(sound)
        if sound_obj is None:
            return
        self.player.play(obj, sound_obj)

    @classmethod
    def get_theme_from_folder(cls, folderpath):
        expected = os.path.join(THEMES_DIR, folderpath)
        info_file = os.path.join(expected, INFO_FILE_NAME)
        if os.path.isfile(info_file):
            info = cls.load_info_file(info_file)
            return AudioTheme(folder=folderpath, **info)

    @classmethod
    def get_installed_themes(cls):
        for folder in os.listdir(THEMES_DIR):
            theme = cls.get_theme_from_folder(folder)
            if theme is None:
                continue
            yield theme

    @staticmethod
    def install_audio_themePackage(theme_pack):
        identified_path = os.path.join(THEMES_DIR, uuid4().hex).lower()
        with ZipFile(theme_pack, "r") as pack:
            pack.extractall(path=identified_path)

    @staticmethod
    def remove_audio_theme(theme):
        theme.deactivate()
        if theme.directory:
            shutil.rmtree(theme.directory)

    @staticmethod
    def load_info_file(info_file):
        with open(info_file, "r", encoding="utf8") as f:
            return json.load(f)

    @staticmethod
    def write_info_file(data, file_path):
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(data, f)

    @staticmethod
    def make_zip_file(output_filename, source_dir):
        # Taken from stackoverflow
        relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
        with ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk(source_dir):
                # add directory (needed for empty dirs)
                zip.write(root, os.path.relpath(root, relroot))
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename):  # regular files only
                        arcname = os.path.join(os.path.relpath(root, relroot), file)
                        zip.write(filename, arcname)
