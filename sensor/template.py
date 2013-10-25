from pyrrd.rrd import RRA

TEMPERATURE = {
	'name': 'temperature',
	'rra': [ 
		RRA(cf='AVERAGE', xff=0.5, steps=1, rows=12*24*366),
		RRA(cf='AVERAGE', xff=0.5, steps=12, rows=24*366*10),
		RRA(cf='AVERAGE', xff=0.5, steps=12*24, rows=366*10),
		RRA(cf='AVERAGE', xff=0.5, steps=12*24*30, rows=12*10)
	]
}

VOLTAGE = {
	'name': 'voltage',
	'rra': [ 
		RRA(cf='AVERAGE', xff=0.5, steps=1, rows=12*24*366),
		RRA(cf='AVERAGE', xff=0.5, steps=12, rows=24*366*10),
		RRA(cf='AVERAGE', xff=0.5, steps=12*24, rows=366*10),
		RRA(cf='AVERAGE', xff=0.5, steps=12*24*30, rows=12*10)
	]
}


