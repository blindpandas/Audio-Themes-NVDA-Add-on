# Audio Themes Add-on For NVDA
This add-on creates a virtual audio display that plays sounds when focusing or navigating objects (such as buttons, links etc...) the audio will be played in a location that corresponds to the object's location in the visual display.

The add-on also enables you to activate, install, remove, edit, create, and distribute audio theme packages.


## Usage
This add-on enables you to perform three distinct tasks, including managing your installed audio themes, editing the currently active audio theme, and creating a new audio theme.

You can access these functions from the add-on's menu which is found in the main NVDA menu.


### Managing Your Audio Themes
- The 'Manage Audio Themes' dialogue enables you to activate or deactivate audio themes, in addition to installing and removing audio themes.
- In this dialogue there are some additional options including:
 - Play sounds in 3D mode: When you uncheck this box the add-on will play the sounds in mono mode (always in the centre of the audio display) regardless of the object location.
 - Speak role such as button, edit box , link etc.: When you uncheck this box NVDA will start announcing the role when focusing objects rather than ignoring it (which is the default behaviour when installing this add-on).
 - Use Synthesizer Volume: Checking this box will set the sound player of this add-on to use the active voice sound, thus making all audible output the same as the voice volume when ever you change that volume.
 - Audio Theme Volume Slider: Alternatively you can set the volume for the add-on using this slider. Setting it to 0 will mute all sounds, and 100 is the maximum volume.


### Editing The Active Audio Theme:
- When you click on the 'Edit the active audio theme' option, a dialogue will open with a list containing all the sounds contained in the currently active theme. From this dialogue you can:
- Change Selected: Selecting a sound from the list and clicking this button, will  open a standard open file dialogue, select a wave file from your file system to replace the selected sound, and click OK to complete the process.
- Remove Selected: This will remove the selected sound from the theme, click 'Yes' to confirm the removal process, and the selected sound will be removed.
- Add New Sound: When clicking this button a new dialogue will be shown. From the first combo box in the newly opened dialogue select the object type you want to assign the sound to it, for example (button, link, tab, menu and so on), then click the 'Browse to a wave file' button to select the sound you want to assign for the previously selected object type. Optionally you can click the preview   button to preview the sound, and finally clicking the OK button will apply the changes and assign the selected sound to the selected object. 
- Close: Will  exit the dialogue without performing any action.


### Creating A New Audio Theme
- If you have a good sound production skills you can apply them here and create an audio theme of your own, rather than editing an existing one. To do this you can follow these steps.
- Collect your audio files in one place, and rename them to whatever make sense to you. For example when I was creating the default audio theme for this add-on, I grouped sounds according to interaction patterns, for example, the combo box, the drop down button, and the split button can all have the same sound, while the Check box, The toggle button, and the menu check item can have the same sound.
- From the add-on menu click 'Create a new audio theme'
- A dialogue will be opened asking you for some information about your new audio theme, including:
*	Theme Name : The name of your theme which will be shown in the audio themes manager. This must be a valid windows folder name.
*	Your Name: Enter your real name or a nick name.
*	Theme description : A Brief description about your audio theme.
- Click OK to move to the next step.
- In the next step a dialogue similar to the 'Audio Themes Editor' will be shown, and from their the process is the same as the Theme editing process, so refer to 'Editing The Active Audio Theme' section.


## Copyright:
Copyright (c) 2014-2016 Musharraf Omer<ibnomer2011@hotmail.com> and Others

Although this add-on was started as an independent project, it evolved to be an enhanced version of the 'Unspoken' add-on by Austin Hicks (camlorn38@gmail.com) and Bryan Smart (bryansmart@bryansmart.com). The majority of this add-on's development went into creating the tools to manage, edit and create audio theme packages. So a big thank you to them for creating such a wonderful add-on, and making it available for us to build on top of their work.


## A Note on Third-party audio files:
The **Default** audio theme package in this add-on uses sounds from several sources, here is a breakdown for them:
- Unspoken 3D Audio: An add-on for NVDA
- TWBlue: A free and open source twitter client
- Mushy TalkBack: An alternative talkback with better sounds.


## Licence
Licensed under the GNU General Public License. See the file **copying** for more details.
