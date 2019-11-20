# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.

from typing import Sequence
from dataclasses import dataclass, field, asdict
from contextlib import suppress
import os
import shutil
import wx
import gui
from ..unspoken import UnspokenPlayer
from ..handler import AudioTheme, AudioThemesHandler, theme_roles, SUPPORTED_FILE_TYPES

import addonHandler
addonHandler.initTranslation()


def _show_audio_file_dialog(parent):
    # Translators: label for all supported file types found in an open dialog
    wildcards = [_("All Supported Audio Formats") + "(*.wav, *.ogg)|*.wav;*.ogg"]
    for ext, desc in SUPPORTED_FILE_TYPES.items():
        wildcards.append(_(desc) + f" (*.{ext})|*.{ext}")
    openFileDlg = wx.FileDialog(
        parent,
        # Translators: the title of a file dialog to browse to an audio file
        message=_("Choose an audio file"),
        # Translators: theme file type description
        wildcard="|".join(wildcards),
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
    )
    if openFileDlg.ShowModal() == wx.ID_OK:
        filename = openFileDlg.GetPath().strip()
        openFileDlg.Destroy()
        if filename.strip():
            return filename


@dataclass(order=True, eq=True)
class SoundFileInfo:
    role: int
    src: os.PathLike
    dst: os.PathLike

    @property
    def role_label(self):
        return theme_roles[self.role]

    def reconcile(self):
        src_ext = os.path.splitext(self.src)[-1]
        dst_file = os.path.join(os.path.dirname(self.dst), f"{self.role}{src_ext}")
        with suppress(shutil.Error):
            shutil.copy(self.src, dst_file)
            return True
        return False


@dataclass
class ThemeState:
    theme: AudioTheme
    initial_state: Sequence[SoundFileInfo] = None
    state: Sequence[SoundFileInfo] = None

    def __post_init__(self):
        _init_state = []
        basedir = self.theme.directory
        for file in os.listdir(basedir):
            filepath = os.path.join(basedir, file)
            if AudioTheme.is_valid_audio_file(filepath):
                _init_state.append(
                    SoundFileInfo(
                        role=int(os.path.splitext(file)[0]), src=filepath, dst=filepath
                    )
                )
        self.initial_state = tuple(_init_state)
        self.state = list(self.initial_state)

    def apply_diff(self):
        for fileinfo in self.state:
            if fileinfo.src != fileinfo.dst:
                result = fileinfo.reconcile()
                if not result:
                    wx.MessageBox(
                        # Translators: message indicating failure in copying files
                        _(
                            "Could not copy file {src} to directory {dst}."
                        ).format(src=fileinfo.src, dst=fileinfo.dst),
                        # Translators: title for a message indicating an error
                        _("Error"),
                        style=wx.ICON_ERROR,
                    )


class BaseDialog(wx.Dialog):
    """Base dialog for all other dialogs."""

    def __init__(self, title, parent=gui.mainFrame):
        super().__init__(parent=parent, title=title)
        self.__retval = wx.ID_CANCEL

        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.addControls(sizer, panel)
        buttons = self.getButtons(panel)
        if buttons is not None:
            line = wx.StaticLine(panel, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
            sizer.Add(
                line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 10
            )
            sizer.Add(buttons, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        panel.Layout()
        sizer.Fit(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 2, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(sizer)
        self.Fit()
        self.CenterOnScreen()

    def ShowModal(self):
        super().ShowModal()
        return self.__retval

    def addControls(self, sizer, parent):
        """Add dialog controls here."""

    def getButtons(self, parent):
        btnsizer = wx.StdDialogButtonSizer()
        # Translators: the label of the close button in a dialog
        okBtn = wx.Button(parent, wx.ID_OK, _("OK"))
        okBtn.SetDefault()
        # Translators: the label of the close button in a dialog
        cancelBtn = wx.Button(parent, wx.ID_CANCEL, _("Cancel"))
        btnsizer.AddButton(okBtn)
        btnsizer.AddButton(cancelBtn)
        btnsizer.Realize()
        self.Bind(wx.EVT_BUTTON, self.onOkClicked, okBtn)
        return btnsizer

    def onOkClicked(self, event):
        if self.should_return_id_ok():
            self.__retval = wx.ID_OK
        self.Close()

    def should_return_id_ok(self):
        """Override to indicate if this dialog was not cancelled."""
        return True


class ThemeBlenderDialog(BaseDialog):
    """Dialog for editing and creating audio themes."""

    def __init__(self, title, theme, editing=True):
        self.theme_state = ThemeState(theme)
        self.editing = editing
        self.player = UnspokenPlayer()
        super().__init__(title)

    def addControls(self, sizer, parent):
        # Translators: label for a list containing theme's audio files
        themeEntriesLabel = wx.StaticText(parent, -1, _("Theme Sounds"))
        self.themeEntriesList = wx.ListBox(parent, -1)
        # Translators: label for a button to change the audio file
        self.editButton = wx.Button(parent, wx.ID_EDIT, _("&Change..."))
        # Translators: label for a button to remove the audio file
        self.removeButton = wx.Button(parent, wx.ID_REMOVE, _("&Remove"))
        # Translators: label for a button to add a new audio file
        self.addButton = wx.Button(parent, wx.ID_ADD, _("&Add..."))
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.VERTICAL)
        actionButtonSizer = wx.BoxSizer(wx.VERTICAL)
        listSizer.AddMany(
            [
                (themeEntriesLabel, 1, wx.ALL, 5),
                (self.themeEntriesList, 2, wx.ALL | wx.EXPAND, 5),
            ]
        )
        actionButtonSizer.AddMany(
            [
                (self.editButton, 1, wx.ALL, 5),
                (self.removeButton, 1, wx.ALL, 5),
                (self.addButton, 1, wx.ALL, 5),
            ]
        )
        mainSizer.AddMany(
            [(listSizer, 1, wx.ALL | wx.EXPAND, 10), (actionButtonSizer, 1, wx.ALL, 10)]
        )
        sizer.Add(mainSizer, 1, wx.EXPAND)
        parent.SetMinSize((500, 700))
        parent.Layout()
        self._bind_events()
        self._maintain_state()

    def getButtons(self, parent):
        btnsizer = wx.StdDialogButtonSizer()
        # Translators: the label of the OK button in a dialog
        saveBtn = wx.Button(parent, wx.ID_SAVE, _("&Save"))
        saveBtn.SetDefault()
        # Translators: the label of the cancel button in a dialog
        cancelBtn = wx.Button(parent, wx.ID_CANCEL, _("Cancel"))
        for btn in (saveBtn, cancelBtn):
            btnsizer.AddButton(btn)
        btnsizer.Realize()
        return btnsizer

    def _bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.onSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.onEdit, self.editButton)
        self.Bind(wx.EVT_BUTTON, self.onAdd, self.addButton)
        self.Bind(wx.EVT_BUTTON, self.onRemove, self.removeButton)
        self.Bind(
            wx.EVT_LISTBOX, self.onEntriesListSelectionChanged, self.themeEntriesList
        )

    def _maintain_state(self):
        self.themeEntriesList.Clear()
        for entry in self.theme_state.state:
            self.themeEntriesList.Append(entry.role_label, entry)
        has_items = self.themeEntriesList.Count
        if has_items:
            self.themeEntriesList.SetSelection(0)
        self.editButton.Enable(has_items)
        self.removeButton.Enable(has_items)

    @property
    def selected_sound(self):
        selection = self.themeEntriesList.GetSelection()
        if selection != wx.NOT_FOUND:
            return self.themeEntriesList.GetClientData(selection)

    def is_dirty(self):
        return tuple(self.theme_state.state) == self.theme_state.initial_state

    def onSave(self, event):
        self.theme_state.apply_diff()
        if not self.editing:
            saveFileDlg = wx.FileDialog(
                self,
                # Translators: title for a dialog to save an audio theme package
                _("Save Audio Theme Package"),
                # Translators: filetype description for audio theme packages
                wildcard=_("Audio Theme Package (*.atp)|*.atp"),
                defaultFile=f"{self.theme_state.theme.name}.atp",
                style=wx.FD_SAVE,
            )
            if saveFileDlg.ShowModal() == wx.ID_OK:
                filename = saveFileDlg.GetPath().strip()
                saveFileDlg.Destroy()
                if filename:
                    self.save_theme_package(filename)
        self.theme_state.state = self.theme_state.initial_state = ()
        self.Close()

    def onClose(self, event):
        confirmed = self.is_dirty()
        if not confirmed:
            result = wx.MessageBox(
                # Translators: message asking the user if he/she really want to discard changes
                _(
                    "You will lose all of the changes you have made.\nAre you sure you want to quit this dialog?"
                ),
                # Translators: title for a message asking the user if he/she really want to discard changes
                _("Confirm Quit"),
                style=wx.YES_NO | wx.ICON_WARNING,
            )
            if result == wx.YES:
                confirmed = True
        if not confirmed:
            return
        self.Hide()

    def onEdit(self, event):
        selected_sound = self.selected_sound
        if selected_sound:
            filepath = _show_audio_file_dialog(self)
            if filepath is not None:
                selected_sound.src = filepath

    def onAdd(self, event):
        # Translators: title for a dialog to add a new sound to the audio theme
        dlg = AudioSelectorDialog(parent=self, title=_("Add Sound"))
        with dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.theme_state.state.append(dlg.get_sound())
                self._maintain_state()

    def onRemove(self, event):
        if self.selected_sound is not None:
            self.theme_state.state.pop(self.themeEntriesList.GetSelection())
            self._maintain_state()

    def onEntriesListSelectionChanged(self, event):
        selected_sound = self.selected_sound
        if selected_sound is not None:
            self.player.play_file(selected_sound.src)
        self.editButton.Enable(selected_sound is not None)
        self.removeButton.Enable(selected_sound is not None)

    def save_theme_package(self, dst_dir):
        theme = self.theme_state.theme
        AudioThemesHandler.write_info_file(theme.info_file_path, theme.todict())
        AudioThemesHandler.make_zip_file(dst_dir, theme.directory)


class AudioSelectorDialog(BaseDialog):
    def __init__(self, *args, **kwargs):
        self.selected_audio = None
        super().__init__(*args, **kwargs)

    def addControls(self, sizer, parent):
        # Translators: label for a choice containing theme roles
        roleChoiceLabel = wx.StaticText(parent, -1, _("Sound For:"))
        self.roleChoice = wx.Choice(parent, -1)
        # Translators: label for a button to browse to a an audio file
        self.browseButton = wx.Button(parent, -1, _("&Browse"))
        # Translators: label for a button to preview the selected sound
        self.previewButton = wx.Button(parent, -1, _("&Preview"))
        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        choiceSizer.AddMany(
            [
                (roleChoiceLabel, 1, wx.LEFT | wx.BOTTOM | wx.TOP, 5),
                (self.roleChoice, 2, wx.ALL | wx.EXPAND, 5),
            ]
        )
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddMany(
            [(self.browseButton, 1, wx.ALL, 5), (self.previewButton, 1, wx.ALL, 5)]
        )
        sizer.AddMany([(choiceSizer, 1, wx.ALL, 10), (btnSizer, 1, wx.ALL, 10)])
        self.Bind(wx.EVT_BUTTON, self.onBrowseClicked, self.browseButton)
        self.Bind(wx.EVT_BUTTON, self.onPreviewClicked, self.previewButton)
        self.Bind(wx.EVT_BUTTON, self.onOkClicked, id=wx.ID_OK)
        existing_roles = [finf.role for finf in self.Parent.theme_state.state]
        nonexisting_roles = [
            (r, l) for r, l in theme_roles.items() if r not in existing_roles
        ]
        for role, label in nonexisting_roles:
            self.roleChoice.Append(label, role)
        self.roleChoice.SetSelection(0)
        self.previewButton.Enable(False)

    @property
    def selected_role(self):
        selection = self.roleChoice.GetSelection()
        if selection != wx.NOT_FOUND:
            return self.roleChoice.GetClientData(selection)

    def onBrowseClicked(self, event):
        self.selected_audio = _show_audio_file_dialog(self)
        self.previewButton.Enable(self.selected_audio is not None)

    def onPreviewClicked(self, event):
        if self.selected_audio is not None:
            self.Parent.player.play_file(self.selected_audio)

    def should_return_id_ok(self):
        return self.selected_audio is not None

    def get_sound(self):
        ext = os.path.splitext(self.selected_audio)[-1]
        return SoundFileInfo(
            role=self.selected_role,
            src=self.selected_audio,
            dst=os.path.join(
                self.Parent.theme_state.theme.directory, f"{self.selected_role}{ext}"
            ),
        )
