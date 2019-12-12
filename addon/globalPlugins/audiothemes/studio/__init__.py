# coding: utf-8

# Copyright (c) 2014-2019 Musharraf Omer
# This file is covered by the GNU General Public License.


import wx
import config
import gui
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from wx.adv import CommandLinkButton
from ..handler import AudioTheme, AudioThemesHandler, audiotheme_changed
from .themes_blender import BaseDialog, ThemeBlenderDialog

import addonHandler
addonHandler.initTranslation()


# Translators: the welcome message of the audio theme studio dialog
WELCOME_MSG = _(
    "Welcome To The Audio Themes Studio:\n"
    "Here you can create new audio themes and package them for sharing with others.\n"
    "You can also customize anyone of your installed audio themes with your own sounds."
)


class NewThemeInfoDialog(BaseDialog):
    """Gets information from the user about  the theme."""

    def addControls(self, sizer, parent):
        # Translators: label for a text field
        themeNameLabel = wx.StaticText(parent, -1, _("Theme Name"))
        self.themeNameEdit = wx.TextCtrl(parent, -1, name="name")
        # Translators: label for a text field
        themeAuthorLabel = wx.StaticText(parent, -1, _("Theme Author"))
        self.themeAuthorEdit = wx.TextCtrl(parent, -1, name="author")
        # Translators: label for a text field
        themeSummaryLabel = wx.StaticText(parent, -1, _("Theme Description"))
        self.themeSummaryEdit = wx.TextCtrl(
            parent, -1, style=wx.TE_MULTILINE, name="summary"
        )
        sizer.AddMany(
            [
                (themeNameLabel, 0, wx.ALL, 5),
                (self.themeNameEdit, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 10),
                (themeAuthorLabel, 0, wx.ALL, 5),
                (self.themeAuthorEdit, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 10),
                (themeSummaryLabel, 0, wx.ALL, 5),
                (self.themeSummaryEdit, 1, wx.BOTTOM | wx.LEFT | wx.RIGHT, 10),
            ]
        )
        self.edit_fields = (
            self.themeNameEdit,
            self.themeAuthorEdit,
            self.themeSummaryEdit,
        )

    def get_user_input(self):
        return {field.Name: field.GetValue().strip() for field in self.edit_fields}

    def should_return_id_ok(self):
        has_content = all(self.get_user_input().values())
        if not has_content:
            wx.MessageBox(
                # Translators: error message telling the user that all of the fields are required
                _("All of the fields are required. Exiting..."),
                # Translators: title for an error message
                _("Error"),
                style=wx.ICON_ERROR,
            )
        return has_content


class AudioThemeSelectorDialog(BaseDialog):
    """Allows the user to select one of the installed audio themes for editing."""

    def addControls(self, sizer, parent):
        # Translators: label for the audio theme selector choice
        themesChoiceLabel = wx.StaticText(parent, -1, _("Audio themes"))
        self.themeChoice = wx.Choice(parent, -1)
        sizer.AddMany(
            [
                (themesChoiceLabel, 0, wx.ALL, 5),
                (self.themeChoice, 1, wx.ALL | wx.EXPAND, 10),
            ]
        )
        for theme in AudioThemesHandler.get_installed_themes():
            self.themeChoice.Append(theme.name, theme)
        self.themeChoice.SetSelection(0)

    @property
    def selected_theme(self):
        selection = self.themeChoice.GetSelection()
        if selection != wx.NOT_FOUND:
            return self.themeChoice.GetClientData(selection)


class AudioThemesStudioStartupDialog(BaseDialog):

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super().__init__(*args, **kwargs)

    def addControls(self, sizer, parent):
        # Translators: instruction message in the audio themes studio startup dialog
        dialogMessage = wx.StaticText(self, -1, _(WELCOME_MSG))
        self.createNewThemeButton = CommandLinkButton(
            parent,
            -1,
            # Translators: the main label of a button
            _("Create &New Audio Theme"),
            # Translators: the note of a button
            _("Create a new audio theme package from scratch"),
        )
        self.editExistingThemeButton = CommandLinkButton(
            parent,
            -1,
            # Translators: the main label of a button
            _("Customize &Existing Audio Theme"),
            # Translators: the note of a button
            _("Customize an installed audio theme with your prefered  sounds."),
        )
        sizer.AddMany(
            [
                (dialogMessage, 1, wx.EXPAND | wx.ALL, 10),
                (self.createNewThemeButton, 1, wx.EXPAND | wx.ALL, 10),
                (self.editExistingThemeButton, 1, wx.EXPAND | wx.ALL, 10),
            ]
        )
        # Bind events
        self.Bind(wx.EVT_BUTTON, self.onCreateNewTheme, self.createNewThemeButton)
        self.Bind(wx.EVT_BUTTON, self.onEditExistingTheme, self.editExistingThemeButton)

    def getButtons(self, parent):
        btnsizer = wx.StdDialogButtonSizer()
        # Translators: the lable of the close button in a dialog
        closeBtn = wx.Button(parent, wx.ID_CANCEL, _("&Close"))
        btnsizer.AddButton(closeBtn)
        btnsizer.Realize()
        return btnsizer

    @contextmanager
    def audio_theme_muted(self):
        theme_state = self.plugin.handler.enabled
        self.plugin.handler.enabled = False
        try:
            yield
        finally:
            self.plugin.handler.enabled = theme_state

    def onCreateNewTheme(self, event):
        self.Close()
        theme_info = None
        # Translators: title of a dialog to supply information about a new audio theme
        infoDlg = NewThemeInfoDialog(title=_("Enter Theme Information"))
        with infoDlg:
            if infoDlg.ShowModal() == wx.ID_OK:
                theme_info = infoDlg.get_user_input()
        if not theme_info:
            return
        with TemporaryDirectory() as tempdir:
            new_theme = AudioTheme(directory=tempdir, **theme_info)
            dlg = ThemeBlenderDialog(
                # Translators: title for create new theme dialog
                _("Creating New Theme - {name}").format(name=theme_info["name"]),
                theme=new_theme,
                editing=False,
            )
            with self.audio_theme_muted():
                with dlg:
                    dlg.ShowModal()

    def onEditExistingTheme(self, event):
        self.Close()
        if not list(AudioThemesHandler.get_installed_themes()):
            return wx.MessageBox(
                # Translators: message telling the user that there are no audio themes installed
                _(
                    "You do not have any audio themes installed.\nPlease install or create an audio theme first."
                ),
                # Translators: title for a message telling the user that no audio theme was found
                _("No Audio Themes"),
                style=wx.ICON_ERROR,
            )
        selected_theme = None
        # Translators: title for the theme selector dialog
        with AudioThemeSelectorDialog(_("Select An Audio Theme")) as selectDlg:
            if selectDlg.ShowModal() != wx.ID_OK:
                return
            selected_theme = selectDlg.selected_theme
        dlg = ThemeBlenderDialog(
            # Translators: title for create new theme dialog
            _("Editing Audio Theme: {name}").format(name=selected_theme.name),
            theme=selected_theme,
        )
        with self.audio_theme_muted():
            with dlg:
                dlg.ShowModal()
        audiotheme_changed.notify()
