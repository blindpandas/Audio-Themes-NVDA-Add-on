# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.

import wx
import config
import gui
from .handler import AudioThemesHandler, audiotheme_changed


import addonHandler
addonHandler.initTranslation()


class AudioThemesSettingsPanel(gui.SettingsPanel):
    # Translators: Title for the settings panel in NVDA's multi-category settings
    title = _("Audio Themes")

    def makeSettings(self, settingsSizer):
        # Translators: label for the checkbox to enable or disable audio themes
        self.enableThemesCheckbox = wx.CheckBox(self, -1, _("Enable audio themes"))
        self.innerPanel = innerPanel = wx.Panel(self)
        # Translators: label for a combobox containing a list of installed audio themes
        installedThemesLabel = wx.StaticText(innerPanel, -1, _("Select theme:"))
        self.installedThemesChoice = wx.Choice(innerPanel, -1)
        # Translators: label for a button to show info about an audio theme
        self.aboutThemeButton = wx.Button(innerPanel, -1, _("&About"))
        # Translators: label for a button to remove an audio theme
        self.removeThemeButton = wx.Button(innerPanel, -1, _("&Remove"))
        # Translators: label for a button to add a new audio theme
        self.addThemeButton = wx.Button(innerPanel, -1, _("Add &New..."))
        # Translators: label for a checkbox to toggle the 3D mode
        self.play3dCheckbox = wx.CheckBox(innerPanel, -1, _("Play sounds in 3D mode"))
        # Translators: label for a checkbox to toggle the speaking of object role
        self.speakRoleCheckbox = wx.CheckBox(
            innerPanel, -1, _("Speak roles such as button, edit box , link etc. ")
        )
        # Translators: label for a checkbox to toggle the use of audio themes during say all
        self.useInSayAllCheckbox = wx.CheckBox(
            innerPanel, -1, _("Speak roles during say all")
        )
        # Translators: label for a checkbox to toggle whether the volume of this add-on should follow the synthesizer volume
        self.useSynthVolumeCheckbox = wx.CheckBox(
            innerPanel, -1, _("Use speech synthesizer volume")
        )
        # Translators: label for a slider to set the volume of this add-on
        volumeLabel = wx.StaticText(innerPanel, -1, _("Audio themes volume:"))
        self.volumeSlider = wx.Slider(
            innerPanel, -1, minValue=0, maxValue=100, name=_("Audio themes volume")
        )
        innerSizer = wx.BoxSizer(wx.VERTICAL)
        themesListSizer = wx.BoxSizer(wx.HORIZONTAL)
        themesListSizer.AddMany(
            [
                (installedThemesLabel, 1, wx.LEFT | wx.TOP | wx.BOTTOM, 10),
                (self.installedThemesChoice, 2, wx.EXPAND | wx.ALL, 10),
            ]
        )
        actionSizer = wx.BoxSizer(wx.HORIZONTAL)
        actionSizer.AddMany(
            [
                (self.aboutThemeButton, 1, wx.ALL, 5),
                (self.removeThemeButton, 1, wx.ALL, 5),
                (self.addThemeButton, 1, wx.ALL, 5),
            ]
        )
        innerSizer.Add(self.enableThemesCheckbox, 1, wx.ALL, 15)
        innerSizer.AddMany(
            [(themesListSizer, 1, wx.EXPAND, 10), (actionSizer, 1, wx.ALIGN_CENTER, 10)]
        )
        innerSizer.AddSpacer(10)
        innerSizer.AddMany(
            [
                (self.play3dCheckbox, 1, wx.ALL, 5),
                (self.speakRoleCheckbox, 1, wx.ALL, 5),
                (self.useInSayAllCheckbox, 1, wx.ALL, 5),
                (self.useSynthVolumeCheckbox, 1, wx.ALL, 5),
                (volumeLabel, 1, wx.TOP | wx.LEFT | wx.RIGHT, 10),
                (self.volumeSlider, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 5),
            ]
        )
        innerPanel.SetSizer(innerSizer)
        innerSizer.Fit(innerPanel)
        settingsSizer.Add(innerPanel, 1, wx.EXPAND)
        # Bind events
        self.Bind(wx.EVT_BUTTON, self.onAbout, self.aboutThemeButton)
        self.Bind(wx.EVT_BUTTON, self.onRemove, self.removeThemeButton)
        self.Bind(wx.EVT_BUTTON, self.onAdd, self.addThemeButton)
        self.Bind(
            wx.EVT_CHECKBOX,
            lambda e: self.innerPanel.Enable(e.IsChecked()),
            self.enableThemesCheckbox,
        )
        self.Bind(
            wx.EVT_CHECKBOX,
            lambda e: self.volumeSlider.Enable(not e.IsChecked()),
            self.useSynthVolumeCheckbox,
        )
        self.Bind(
            wx.EVT_CHOICE, self.onThemeSelectionChanged, self.installedThemesChoice
        )
        self._initialize_at_state()
        self._maintain_state()

    @property
    def selected_theme(self):
        selection = self.installedThemesChoice.GetSelection()
        if selection != wx.NOT_FOUND:
            return self.installedThemesChoice.GetClientData(selection)

    def _initialize_at_state(self):
        conf = config.conf["audiothemes"]
        self.enableThemesCheckbox.SetValue(conf["enable_audio_themes"])
        self.play3dCheckbox.SetValue(conf["audio3d"])
        self.speakRoleCheckbox.SetValue(conf["speak_roles"])
        self.useInSayAllCheckbox.SetValue(conf["use_in_say_all"])
        self.useSynthVolumeCheckbox.SetValue(conf["use_synth_volume"])
        self.volumeSlider.SetValue(conf["volume"])

    def _maintain_state(self):
        self.audio_themes = sorted(AudioThemesHandler.get_installed_themes())
        self.installedThemesChoice.Clear()
        for theme in self.audio_themes:
            self.installedThemesChoice.Append(theme.name, theme)
        for theme in self.audio_themes:
            if theme.folder == config.conf["audiothemes"]["active_theme"]:
                self.installedThemesChoice.SetStringSelection(theme.name)
        self.innerPanel.Enable(self.enableThemesCheckbox.IsChecked())
        self.volumeSlider.Enable(not self.useSynthVolumeCheckbox.IsChecked())
        self.onThemeSelectionChanged(None)

    def onSave(self):
        conf = config.conf["audiothemes"]
        conf["enable_audio_themes"] = self.enableThemesCheckbox.IsChecked()
        conf["active_theme"] = self.selected_theme.folder
        conf["audio3d"] = self.play3dCheckbox.IsChecked()
        conf["speak_roles"] = self.speakRoleCheckbox.IsChecked()
        conf["use_in_say_all"] = self.useInSayAllCheckbox.IsChecked()
        conf["use_synth_volume"] = self.useSynthVolumeCheckbox.IsChecked()
        conf["volume"] = self.volumeSlider.GetValue()

    def postSave(self):
        audiotheme_changed.notify()

    def onAbout(self, event):
        wx.MessageBox(
            # Translators: content of a message box containing theme information
            _("Name: {name}\nAuthor: {author}\n\n{summary}").format(
                **self.selected_theme.todict()
            ),
            # Translators: title for a message containing theme information
            _("About Audio Theme"),
            style=wx.ICON_INFORMATION,
        )

    def onRemove(self, event):
        theme = self.selected_theme
        confirm = wx.MessageBox(
            # Translators: message asking the user to confirm the removal of an audio theme
            _(
                "This can not be undone.\nAre you sure you  want to remove audio theme {name}?"
            ).format(name=theme.name),
            # Translators: title of a message asking the user to confirm the removal of an audio theme
            _("Remove Audio Theme"),
            style=wx.YES_NO | wx.ICON_WARNING,
        )
        if confirm == wx.YES:
            AudioThemesHandler.remove_audio_theme(theme)
            self._maintain_state()

    def onAdd(self, event):
        openFileDlg = wx.FileDialog(
            self,
            # Translators: the title of a file dialog to browse to an audio theme package
            message=_("Choose an audio theme package"),
            # Translators: theme file type description
            wildcard=_("Audio Theme Packages") + " (*.atp)|*.atp",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if openFileDlg.ShowModal() == wx.ID_OK:
            filename = openFileDlg.GetPath().strip()
            openFileDlg.Destroy()
            if filename:
                AudioThemesHandler.install_audio_themePackage(filename)
                self._maintain_state()

    def onThemeSelectionChanged(self, event):
        flag = self.selected_theme is not None
        for btn in (self.aboutThemeButton, self.removeThemeButton):
            btn.Enable(flag)
