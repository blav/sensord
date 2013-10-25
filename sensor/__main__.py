from . import *

rrd = SensorRRD ('/root/sensord/rrd')
sensor = RemoteSensor (rrd)
sensor.listen ('/dev/ttyAMA0', 9600)
