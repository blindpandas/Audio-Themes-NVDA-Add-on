# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.

from enum import IntEnum
from collections import OrderedDict
from dataclasses import dataclass, field, asdict
from zipfile import ZipFile, ZIP_DEFLATED
from uuid import uuid4
import os
import ctypes
import shutil
import copy
import json
import config
import controlTypes
import extensionPoints
from config import post_configSave, post_configReset, post_configProfileSwitch
from .unspoken import UnspokenPlayer, libaudioverse, dll_hack

import addonHandler
addonHandler.initTranslation()

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


theme_roles = copy.copy(controlTypes.roleLabels)
theme_roles.update(
    {
        # Translators: The label of the sound which will be played when focusing a protected edit control.
        SpecialProps.protected: _("Protected Edit Field"),
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
    directory: str
    author: str
    summary: str
    is_active: bool = False
    sounds: dict = field(default_factory=dict)

    @property
    def info_file_path(self):
        return os.path.join(self.directory, INFO_FILE_NAME)

    @property
    def folder(self):
        return os.path.split(self.directory)[-1]

    def exists(self):
        return os.path.isdir(self.directory)

    def todict(self):
        data = asdict(self)
        for unwanted_key in ("is_active", "directory", "sounds"):
            data.pop(unwanted_key)
        return data

    def load(self, player):
        if self.sounds:
            self.unload()
        if not os.path.isdir(self.directory):
            return
        for filename in os.listdir(self.directory):
            path = os.path.join(self.directory, filename)
            rep_role = self.is_valid_audio_file(path)
            if rep_role is not None:
                self.sounds[rep_role] = player.make_sound_object(path)

    def unload(self):
        self.sounds.clear()

    def deactivate(self):
        """Deactivate this theme"""
        self.unload()
        self.is_active = False

    @staticmethod
    def is_valid_audio_file(filepath):
        """Return the role that this file represent (if any) else None."""
        filename = os.path.split(filepath)[-1]
        fnrole, ext = os.path.splitext(filename)
        if os.path.isfile(filepath) and ext[1:] in SUPPORTED_FILE_TYPES.keys():
            try:
                key = int(fnrole)
            except ValueError:
                return
            if key in theme_roles:
                return key


class AudioThemesHandler:
    """Query and manage audio themes."""

    def __init__(self):
        config.conf.spec["audiothemes"] = audiothemes_config_defaults
        self.enabled = True
        self.player = UnspokenPlayer()
        self.active_theme = None
        self.configure()
        for action in (
            post_configSave,
            post_configReset,
            post_configProfileSwitch,
            audiotheme_changed,
        ):
            action.register(self.configure)

    def close(self):
        if self.active_theme is not None:
            self.active_theme.deactivate()
        for _dll in dll_hack:
            ctypes.windll.kernel32.FreeLibrary(_dll._handle)

    def get_active_theme(self):
        if not config.conf["audiothemes"]["enable_audio_themes"]:
            return
        theme = self.get_theme_from_folder(config.conf["audiothemes"]["active_theme"])
        if not theme:
            config.conf["audiothemes"]["active_theme"] = "Default"
            theme = self.get_theme_from_folder("Default")
        if theme.exists():
            theme.load(self.player)
            theme.is_active = True
            return theme

    def configure(self, *args, **kwargs):
        user_config = config.conf["audiothemes"]
        if self.active_theme is not None:
            self.active_theme.deactivate()
        self.enabled = user_config["enable_audio_themes"]
        self.active_theme = self.get_active_theme()
        if self.active_theme is None:
            return
        self.player.audio3d = user_config["audio3d"]
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
            return AudioTheme(directory=expected, **info)

    @classmethod
    def get_installed_themes(cls):
        for folder in os.listdir(THEMES_DIR):
            theme = cls.get_theme_from_folder(folder)
            if theme is None:
                continue
            yield theme

    @classmethod
    def install_audio_themePackage(cls, theme_pack):
        identified_path = os.path.join(THEMES_DIR, uuid4().hex).lower()
        with ZipFile(theme_pack, "r") as pack:
            if pack.infolist()[0].is_dir():
                # Legacy theme package
                return cls._install_legacy(pack, identified_path)
            pack.extractall(path=identified_path)

    @classmethod
    def _install_legacy(cls, pack, final_dst):
        pack_infolist = pack.infolist()
        theme_name = pack_infolist[0].orig_filename.strip("/")
        os.mkdir(final_dst)
        for zinfo in pack_infolist[1:]:
            filename = os.path.split(zinfo.filename)[1]
            with open(os.path.join(final_dst, filename), "wb") as soundfile:
                soundfile.write(pack.read(zinfo))
        info_file = os.path.join(final_dst, INFO_FILE_NAME)
        theme_info = cls.load_info_file(info_file)
        if "name" not in theme_info:
            theme_info["name"] = theme_name
            cls.write_info_file(info_file, theme_info)

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
    def write_info_file(file_path, data):
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(data, f)

    @staticmethod
    def make_zip_file(output_filename, source_dir):
        with ZipFile(output_filename, "w", ZIP_DEFLATED) as zip:
            for filename in os.listdir(source_dir):
                file = os.path.join(source_dir, filename)
                if os.path.isfile(file):
                    zip.write(file, filename)
