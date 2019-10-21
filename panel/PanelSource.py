from scapy.all import *
from flexx import flx
import configparser
import os

class PanelSource(flx.PyWidget):
	def init(self):
		with flx.HBox() as pnl_source:
			flx.Label(text="Name: ")
			self.txt_name = flx.LineEdit(text="test", flex=1)
			self.btn_save = flx.Button(text='Apply')
			self.btn_new = flx.Button(text='New')
			self.btn_del = flx.Button(text='Delete')

	@flx.reaction('btn_save.pointer_click')
	def on_save(self, *events):
		self.root.save_config(self.txt_name.text)

	@flx.reaction('btn_del.pointer_click')
	def on_del(self, *events):
		self.root.del_config(self.txt_name.text)

	@flx.reaction('btn_new.pointer_click')
	def on_new(self, *events):
		self.txt_name.set_text("")
		self.root.new_config()
