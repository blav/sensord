#!/usr/bin/python

import serial
from time import sleep
from pyrrd.rrd import DataSource, RRA, RRD
from pyrrd.exceptions import ExternalCommandError
import os
import datetime as dt
from .template import *

class SensorRRD:
	def __init__(self, rrdpath):
		self.rrdpath = rrdpath
		self.rrdfiles = {}
		if os.path.isdir (self.rrdpath) == False:
			raise ValueError(rrdpath + " is not a directory")

	def _key(self, name, template):
		return name + '-' + template['name']

	def _rrd(self, name, template):
		key = self._key(name, template)
		if self.rrdfiles.has_key(key):
			return self.rrdfiles[key]

		filename = os.path.join (self.rrdpath, key + '.rrd')	
		if os.path.isfile(filename):
			self.rrdfiles[key] = RRD(filename, mode='w')
			return self.rrdfiles[key]

		self.rrdfiles[key] = RRD(filename, mode='w',
			ds = [ DataSource(dsName=name, dsType='GAUGE', heartbeat=600) ],
			rra = template['rra']
		)

		self.rrdfiles[key].create()
		return self.rrdfiles[key]

	def record (self, name, template, value):
		try:
			rrd = self._rrd(name, template)
			now = dt.datetime.now().strftime("%s")
			rrd.bufferValue (now, value)
			rrd.update(debug=True)
		except ExternalCommandError as e:
			print (e)

class RemoteSensor:
	def __init__ (self, rrd):
		self.rrd = rrd

	def onTemperature (self, devid, temperature):
		self.rrd.record (devid, TEMPERATURE, temperature)
		print(temperature)

	def onAwake (self, devid):
		pass

	def onStarted (self, devid):
		print(devid + " started")

	def onSleeping (self, devid):
		pass

	def onBattery (self, devid, voltage):
		self.rrd.record (devid, VOLTAGE, voltage)
		print (voltage)

	def listen (self, tty, baudrate):
		ser = serial.Serial(tty, baudrate)
		msg = ''
		while True:
			msg += ser.read(12)
			if len(msg) < 12:
				continue
		
			i = msg.find("a")
			if i < 0:
				continue
			
			msg = msg [i:] 
			while len(msg) >= 12:
				cmd = msg[:12]
				self._dispatch(cmd)
				msg = msg [12:]
			

	def _dispatch (self, cmd):
		devid = cmd [1:3]
		cmd = cmd [3:]
		i = cmd.find('-')
		if i >= 0:
			cmd = cmd [:i]

		if cmd.startswith ("TMPA"):
			self.onTemperature(devid, cmd [4:])
		elif cmd.startswith ("TEMP"):
			self.onTemperature(devid, cmd [4:])
		elif cmd.startswith ("STARTED"):
			self.onStarted(devid)
		elif cmd.startswith ("AWAKE"):
			self.onAwake(devid)
		elif cmd.startswith ("SLEEPING"):
			self.onSleeping(devid)
		elif cmd.startswith ("BATT"):
			self.onBattery(devid, cmd [4:])

