import os
from gi.repository import GObject, Gdk, Gtk, Gedit, PeasGtk

class oldTab(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
	__gtype_name__ = "oldTab"
	window = GObject.property(type=Gedit.Window)
	tabs = None
	tabnumbers = None

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.kpe_handler = self.window.connect('key-press-event', self.on_tab_switch)

	def do_deactivate(self):
		pass

	def do_update_state(self):
		pass

	def get_tabs(self):
		tabs = []
		for document in self.window.get_documents():
			tabs.append(document.get_uri_for_display())

		return tabs

	def on_tab_switch(self, widget, event):
		defmod = Gtk.accelerator_get_default_mod_mask() & event.state
		if (event.keyval == 65289 and defmod == Gdk.ModifierType.CONTROL_MASK) or (event.keyval == 65056 and defmod == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK)):
			curtab = self.window.get_active_tab()
			tabs = curtab.get_parent().get_children()
			tablist = Gtk.ListStore(GObject.TYPE_STRING)
			self.tabs = self.get_tabs()

			i = 0
			x = 0
			self.tabnumbers = []
			for tab in self.tabs:
				tablist.append((tab,))
				if (tab == curtab.get_document().get_uri_for_display()):
					if (event.keyval == 65289):
						x = i + 1
						if (x == len(self.tabs)):
							x = 0
					if (event.keyval == 65056):
						x = i - 1
						if (x == -1): 
							x = len(self.tabs) - 1
				self.tabnumbers.append(i)
				i = i + 1
			self.window.set_active_tab(tabs[self.tabnumbers[x]])
			
			return True

		return
