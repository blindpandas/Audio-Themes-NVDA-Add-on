r"""
* This add-on creates a virtual audio display that plays sounds when focusing or navigating objects, the audio will be played in a location that corresponds to the object's location in the visual display.
* it also enables the user to activate, install, remove, edit, create, and distribute audio theme packages.
* Started as an indipendant project, this addon evolved to be an enhanced version of the 'Unspoken' addon by Bryan Smart (bryansmart@bryansmart.com) and Austin Hicks (camlorn38@gmail.com).
* The development of this addon is happening on GitHub <http://github.com/mush42/Audio-Themes-NVDA-Add-on>
* Crafted by Musharraf Omer <ibnomer2011@hotmail.com> using code published by  others from the NVDA community.
* Licensed under the GNU General Public License.
""" 

import time
import wx

import globalPluginHandler
import appModuleHandler
import NVDAObjects
import gui
import speech
import controlTypes
import globalVars

from .dialogs.manage_dg import ManagerDialog
from .dialogs.edit_dg import EditorDialog
from .dialogs.create_dg import CreaterDialog

from .backend import helpers
from .backend import audioThemeHandler
from .backend.audioThemeHandler import SIMULATION, MIXER, SpecialProps, libaudioverse

import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.allowedApps = [u'firefox', u'iexplore', u'chrome', u'opera']
		self.hrtf_panner = libaudioverse.HrtfNode(SIMULATION, "default")
		self.hrtf_panner.should_crossfade = False
		self.hrtf_panner.connect_simulation(0)
		self._previous_mouse_object = None
		self._last_played_object = None
		self._last_played_time = 0
		#these are in degrees.
		self._display_width = 180.0
		self._display_height_min = -40.0
		self._display_height_magnitude = 50.0
		#the mixer feeds us through NVDA.
		self.mixer = MIXER
		#Create GUI 
		self.themesMenu = wx.Menu()
		self.manage_themes_item = self.themesMenu.Append(wx.ID_ANY, 
		  # Translators: the label of the menu item
		  # Translators: that open the audio themes manager dialog.
		  _("&Manage audio themes..."), 
		  # Translators: the tooltip text of the menu item
		  # Translators: that opens audio themes manager dialog
		  _("Manage themes")
		)
		# Create IDs for these menu items to be remove if in secure screen.
		editId = wx.NewId()
		self.edit_theme_item = self.themesMenu.Append(editId, 
		  # Translators: The label of the menu item
		  # Translators: that opens the audio themes editor dialog
		  _("&Edit the active audio theme..."), 
		  # Translators: The tooltip of the menu item
		  # Translators: that opens the audio themes editor dialog
		  _("Edit the current theme"))
		createId = wx.NewId()
		self.create_theme_item = self.themesMenu.Append(createId, 
		  # Translators: the label of the menu item to open
		  # Translators: the audio themes Creater dialog.
		  _("&Create a new audio theme..."), 
		  # Translators: the tooltip text of the menu item
		  # Translators: that opens audio themes creater dialog
		  _("Create a new audio theme"))
		if globalVars.appArgs.secure:
			# Remove the vonrable items.
			self.themesMenu.Remove(editId)
			self.themesMenu.Remove(createId)
		self.submenu_item = gui.mainFrame.sysTrayIcon.menu.InsertMenu(2, wx.ID_ANY, 
		  # Translators: The label for this add-on's  menu
		  _("&Audio Themes"), 
		  self.themesMenu)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda evt: helpers.activate(ManagerDialog), self.manage_themes_item)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onEditorDialog, self.edit_theme_item)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, lambda e: helpers.activate(CreaterDialog), self.create_theme_item)
		self.postInit()

	def postInit(self):
		helpers.setupConfig()
		if helpers.getCfgVal("using"):
			audioThemeHandler.initialize()
		if not helpers.getCfgVal("speakRole"):
			speech.getSpeechTextForProperties = audioThemeHandler.hook_getSpeechTextForProperties

	def onEditorDialog(self, evt):
		if not helpers.getCfgVal("using"):
			gui.messageBox(
			  # Translators: The text in a message box telling the user to activate an audio theme before being able to start the themes editor. 
			  _("There is no active audio theme. Please activate an audio theme first."),
			  # Translators: The title of the message Box indicating an error.
			  _("Error"))
			return
		helpers.activate(EditorDialog)

	def terminate(self):
		if not self.submenu_item: return
		try:
			gui.mainFrame.sysTrayIcon.menu.RemoveItem(self.submenu_item)
		except wx.PyDeadObjectError:
			pass

	def event_gainFocus(self, obj, nextHandler):
		self.playObject(obj)
		nextHandler()

	def event_becomeNavigatorObject(self, obj, nextHandler):
		self.playObject(obj)
		nextHandler()

	def event_mouseMove(self, obj, nextHandler, x, y):
		if obj != self._previous_mouse_object:
			self._previous_mouse_object = obj
			self.playObject(obj)
		nextHandler()

	def event_show(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_HELPBALLOON or isinstance(obj, NVDAObjects.UIA.Toast):
			obj.snd = SpecialProps.notify
			self.playObject(obj)
		nextHandler()

	def event_documentLoadComplete(self, obj, nextHandler):
		if appModuleHandler.getAppNameFromProcessID(obj.processID) in self.allowedApps:
			location = obj.location
			obj.location = None
			self.playObject(obj)
			obj.location = location
		nextHandler()

	def playObject(self, obj):
		# aboart early!
		if not helpers.getCfgVal("using"): return
		activeTheme = audioThemeHandler.findThemeWithProp("isActive", True)
		if not activeTheme: return
		soundpack = activeTheme.soundobjects
		curtime = time.time()
		if curtime-self._last_played_time < 0.1 and obj is self._last_played_object:
			return
		order = self.getOrder(obj)
		# if the object has a snd property, then play directly!
		if getattr(obj, "snd", None):
			pass
		elif 16384 in obj.states:
			obj.snd = SpecialProps.protected
		elif order and soundpack.get(order, None):
			obj.snd = order
		else:
			obj.snd = obj.role
		if not obj.snd in soundpack:
			return
		self._last_played_object = obj
		self._last_played_time = curtime
		if helpers.getCfgVal("threeD"):
			self.play(obj, soundpack, _3d=True)
		else:
			self.play(obj, soundpack, _3d=False)

	def play(self, obj, soundPack, _3d):
		snd = obj.snd
		# Get coordinate bounds of desktop.
		desktop = NVDAObjects.api.getDesktopObject()
		desktop_max_x = desktop.location[2]
		desktop_max_y = desktop.location[3]
		# Get location of the object.
		if _3d and obj.location != None:
			# Object has a location. Get its center.
			obj_x = obj.location[0] + (obj.location[2] / 2.0)
			obj_y = obj.location[1] + (obj.location[3] / 2.0)
		else:
			# Objects without location are assumed in the center of the screen.
			obj_x = desktop_max_x / 2.0
			obj_y = desktop_max_y / 2.0
		# Scale object position to audio display.
		angle_x = ((obj_x-desktop_max_x/2.0)/desktop_max_x)*self._display_width
		#angle_y is a bit more involved.
		percent = (desktop_max_y-obj_y)/desktop_max_y
		angle_y = self._display_height_magnitude*percent+self._display_height_min
		#clamp these to Libaudioverse's internal ranges.
		angle_x = helpers.clamp(angle_x, -90.0, 90.0)
		angle_y = helpers.clamp(angle_y, -90.0, 90.0)
		#In theory, this can be made faster if we remember which is last, but that shouldn't matter here
		with SIMULATION:
			soundPack[self._last_played_object.role].disconnect(0)
			soundPack[snd].connect(0, self.hrtf_panner, 0)	
			soundPack[snd].position = 0.0
			self.hrtf_panner.azimuth = angle_x
			self.hrtf_panner.elevation = angle_y
			volume = helpers.compute_volume(helpers.getCfgVal("volume"))
			self.hrtf_panner.mul = volume

	def getOrder(self, obj, parrole = 14, chrole = 15):
		if obj.parent and obj.parent.role != parrole:
			return None
		if (obj.previous is None) or (obj.previous.role != chrole):
			return SpecialProps.first
		elif (obj.next is None) or (obj.next.role != chrole):
			return SpecialProps.last

