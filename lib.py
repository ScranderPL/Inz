import sys
import time
import datetime
import math
import numpy as np
import os
import pptk
import array
import struct
from datetime import datetime, timedelta
from astropy.time import Time

def milisOfDay(time):
	return (time-time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()*1000
	
	
def generation(lidarFileName, missionFileName, genOption):

	if genOption != "xyz" and genOption != "geo":
		print("Zła opcja")
		return

	lidarFile = open(lidarFileName, "r")
	
	gpsTimes = []
	longitudes = []
	latitudes = []
	altitudes = []
	yawList = []
	pitchList = []
	rollList = []
	lidarData = []
	
	for lineNumber, line in enumerate(lidarFile):
		if lineNumber > 1:
			tmpSplit = line.replace("[", "").replace("]", "").replace("L", "").replace(" ","").split(",")
			try:
				gpsTimes.append(datetime.strptime(tmpSplit[1], "%H:%M:%S.%f"))
			except ValueError:
				gpsTimes.append(datetime.strptime(tmpSplit[1], "%H:%M:%S"))
			longitudes.append(float(tmpSplit[2]))
			latitudes.append(float(tmpSplit[3]))
			altitudes.append(float(tmpSplit[4]))
			yawList.append(float(tmpSplit[7]))
			pitchList.append(float(tmpSplit[8]))
			rollList.append(float(tmpSplit[9]))
			
			tmpSplit = tmpSplit[11:]
			
			lidarRead = []
			for value in tmpSplit:
				if value == "":
					break;
				lidarRead.append(int(value))
				
			lidarData.append(lidarRead)

	# lidar's last reading will usually be incomplete, so we should just erase it
	lidarData = lidarData[:-1]
###############################################################
	# another log file with AHRS data, yaw provided in last log is not precise enough
	
	ahrsWeek = []
	ahrsTime = []
	ahrsTimeTS = []
	ahrsRoll = []
	ahrsPitch = []
	ahrsYaw = []
	ahrsRpyTS = []
	ahrsAlt = []
	ahrsLat = []
	ahrsLon = []
	
	ahrsTimeFinal = []
	ahrsRollFinal = []
	ahrsPitchFinal = []
	ahrsYawFinal = []
	ahrsAltFinal = []
	ahrsLatFinal = []
	ahrsLonFinal = []
	
	ahrsFile = open(missionFileName, "r")
	
	for lineNumber, line in enumerate(ahrsFile):
		tmpLine = line.replace(" ","").split(",")
		if tmpLine[0] == "GPS":
			gpsMils = int(tmpLine[4])*(60*60*24*7*1000)+int(tmpLine[3])
			#LEAP SECONDS
			gpsMilsC = float(float(gpsMils)/1000.0)
			time = Time(gpsMilsC, format='gps')
			gpsTime = Time(time, format='datetime', scale='utc')
			print(gpsTime)
			#gpsTime = datetime(1980, 1, 6) + timedelta(microseconds=gpsMils*1000) - timedelta(seconds=18)
			#####
			ahrsTime.append(gpsTime.datetime);
			ahrsTimeTS.append(int(tmpLine[1]))
		if tmpLine[0] == "AHR2":
			ahrsRoll.append(float(tmpLine[2]))
			ahrsPitch.append(float(tmpLine[3]))
			ahrsYaw.append(float(tmpLine[4]))
			ahrsAlt.append(float(tmpLine[5]))
			ahrsLat.append(float(tmpLine[6]))
			ahrsLon.append(float(tmpLine[7]))
			ahrsRpyTS.append(int(tmpLine[1]))
	
	j = 0
	for i in range(0, len(ahrsTime)):
		if ahrsTimeTS[i] < ahrsRpyTS[j]:
			continue
		while ahrsTimeTS[i] > ahrsRpyTS[j]:
			j = j+1
			if j >= len(ahrsYaw):
				j = j-1
				break
			if ahrsTimeTS[i] <= ahrsRpyTS[j]:
				j = j-1
				break
		if j+1 >= len(ahrsYaw):
			break

		ahrsTimeFinal.append(ahrsTime[i])
		ahrsRollFinal.append(ahrsRoll[j])
		ahrsPitchFinal.append(ahrsPitch[j])
		ahrsYawFinal.append(ahrsYaw[j])
		ahrsAltFinal.append(ahrsAlt[j])
		ahrsLatFinal.append(ahrsLat[j])
		ahrsLonFinal.append(ahrsLon[j])
			
	j = 0
	for i in range(0, len(gpsTimes)):
		while milisOfDay(gpsTimes[i]) > milisOfDay(ahrsTimeFinal[j]):
			j = j+1
			if j >= len(ahrsTimeFinal):
				j = j-1
				break
			if milisOfDay(gpsTimes[i]) < milisOfDay(ahrsTimeFinal[j]):
				j = j-1
				break
		if j+1 >= len(ahrsTimeFinal):
			break
			
		rollList[i] = ahrsRollFinal[j]
		pitchList[i] = ahrsPitchFinal[j]
		yawList[i] = ahrsYawFinal[j]
		altitudes[i] = ahrsAltFinal[j]
		latitudes[i] = ahrsLatFinal[j]
		longitudes[i] = ahrsLonFinal[j]
		
	# lidar gps's last readings are very inaccurate so it will be removed
	siz = len(gpsTimes)
	lidarData = lidarData[:-(siz-i+1)]
	gpsTimes =      gpsTimes[:-(siz-i+1)]
	longitudes =    longitudes[:-(siz-i+1)]
	latitudes =     latitudes[:-(siz-i+1)]
	altitudes =     altitudes[:-(siz-i+1)]
	yawList =       yawList[:-(siz-i+1)]
	pitchList =     pitchList[:-(siz-i+1)]
	rollList =      rollList[:-(siz-i+1)]
	lidarData =     lidarData[:-(siz-i+1)]
			
	################################################
	rrr = 6378137
	
	normLat = np.ndarray(shape=(len(longitudes)), dtype=float)
	normLon = np.ndarray(shape=(len(longitudes)), dtype=float)


	#for j in range(0, len(latitudes) - 1):
	#	normLon[j] = rrr * math.cos(math.radians(latitudes[j])) * math.sin(math.radians(longitudes[j]))
	#	normLat[j] = rrr * math.cos(math.radians(latitudes[j])) * math.cos(math.radians(longitudes[j]))

	x = math.radians((max(longitudes))-(min(longitudes)))*math.cos(((max(latitudes))+(min(latitudes)))/2)
	y = math.radians((max(latitudes))-(min(latitudes)))
	distX = abs(x*rrr)
	distY = abs(y*rrr)
	print("x diff = {}".format(distX))
	print("y diff = {}".format(distY))
	
	normLon = [ float(float(x-min(longitudes))/float(max(longitudes)-min(longitudes)))*distX for x in longitudes ]
	normLat = [ float(float(x-min(latitudes))/float(max(latitudes)-min(latitudes)))*distY for x in latitudes ]
	
	probeSize = 100 #len(lidarData)
	probeStart = 2500
	
	xs = np.ndarray(shape=(probeSize*len(lidarData[0])), dtype=float)
	ys = np.ndarray(shape=(probeSize*len(lidarData[0])), dtype=float)
	zs = np.ndarray(shape=(probeSize*len(lidarData[0])), dtype=float)
	
	lidarSteps = len(lidarData[0])
	
	# Depends on amount of points from lidar impulse
	lidarRange = 0.25*(lidarSteps-1)
	
	ran = np.linspace(-45+0,-45+lidarRange,lidarSteps)  #+170.5
	
	yawOffset = 0
	if genOption == "geo":
		yawOffset = 280
	elif genOption == "xyz":
		yawOffset = 310
	
	for j in range(probeStart, probeStart+probeSize): #len(lidarData)-1):
		i = 0
		sys.stdout.write( '{0}/{1}\r'.format(j, probeSize+probeStart-1))
		for l in ran:
			xyz = np.matrix([
			[(lidarData[j][i]/1000.0)*math.cos(math.radians(l))],
			[0.0],
			[-(lidarData[j][i]/1000.0)*math.sin(math.radians(l))]])
			
			
			yaw =  math.radians(yawList[j] + yawOffset)
			
			pitch = math.radians(pitchList[j])
			
			roll = math.radians(rollList[j])
			
			yawMatrix = np.matrix([
			[math.cos(yaw), -math.sin(yaw), 0],
			[math.sin(yaw), math.cos(yaw), 0],
			[0, 0, 1]])
			
			pitchMatrix = np.matrix([
			[math.cos(roll), 0, math.sin(roll)],
			[0, 1, 0],
			[-math.sin(roll), 0, math.cos(roll)]])
			
			rollMatrix = np.matrix([
			[1, 0, 0],
			[0, math.cos(pitch), -math.sin(pitch)],
			[0, math.sin(pitch), math.cos(pitch)]])
			
			
			newxyz = yawMatrix * (pitchMatrix*(rollMatrix*xyz))
			
			newy = newxyz[1]/(111111)
			newx = newxyz[0]/(111111*math.cos(math.radians(latitudes[j]+newy)))

			newz = newxyz[2]
			# ---------------------------
			
			if genOption == "geo":
				xs[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newx +longitudes[j]
				ys[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newy +latitudes[j]
				zs[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newz + (altitudes[j])
			elif genOption == "xyz":
				xs[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newxyz[0, 0] +	normLon[j]
				ys[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newxyz[1, 0] +	normLat[j]
				zs[(j-probeStart)*(lidarSteps)+(i % lidarSteps)] = newxyz[2, 0] +	altitudes[j]

			i = i + 1
	
	return xs, ys, zs
	
def visualize(xs, ys, zs, genOption):

	scale = 1.0
	if genOption == "geo":
		scale = 111111.0
	elif genOption == "xyz":
		scale = 1.0
	else:
		print("Zła opcja")
		return
	xyz_v = np.array((xs, ys, zs), dtype=float)
	xaad = np.random.rand(len(xyz_v[0]),3)
	for j in range(0, len(xyz_v[0]) - 1):
		xaad[j][0] = xs[j]*scale
		xaad[j][1] = ys[j]*scale
		xaad[j][2] = zs[j]
	xaa = np.random.rand(len(xyz_v[0]),3)

	
	v = pptk.viewer(xaad)
	v.attributes(xaa)
	v.set(point_size=0.01)
	v.set(lookat=[xaad[j][0],xaad[j][1],xaad[j][2]])

def writeToLas(lasFileName, xs, ys, zs):
	fil = open(lasFileName, "w+b")
	ch = bytearray(b'LASF')
	ch.extend([0, 0]) # file source id
	ch.extend([0, 0]) # global encoding
	ch.extend([0]*16) # GUID
	ch.extend([1]) # version major
	ch.extend([2]) # version minor
	ch.extend([0]*32) # system identifier
	
	gen_soft = bytearray(b'InzMGWB')
	ch.extend(gen_soft)
	ch.extend([0]*(32-len(gen_soft))) # generating software

	curr_time = datetime.now()
	ch.extend(struct.pack('<H', int(curr_time.timetuple().tm_yday))) 	# file creation day of year
	ch.extend(struct.pack('<H', int(curr_time.year))) 					# file creation year
	
	ch.extend(struct.pack('<H', 227))			# header size
	ch.extend(struct.pack('<I', 227))			# offset to point data
	ch.extend(struct.pack('<I', 0))				# number of variable length records
	ch.extend([0])								# point data format id
	ch.extend(struct.pack('<H', 20))			# point data record length
	ch.extend(struct.pack('<I', len(xs)))		# number of point records
	
	ch.extend(struct.pack('<I', len(xs)))
	ch.extend(struct.pack('<I', 0)*4)				# number of points by return
	ch.extend(struct.pack('<d', 0.0000001)*3)		# x, y, z scale factors
	ch.extend(struct.pack('<d', 0)*3)				# x, y, z offset
	
	ch.extend(struct.pack('<d', max(xs)))			# max x
	ch.extend(struct.pack('<d', min(xs)))			# min x
	
	ch.extend(struct.pack('<d', max(ys)))			# max y
	ch.extend(struct.pack('<d', min(ys)))			# min y
	
	ch.extend(struct.pack('<d', max(zs)))			# max z
	ch.extend(struct.pack('<d', min(zs)))			# min z

	# tmp
	
	for j in range(0, len(xs) - 1):
		sys.stdout.write( '{0}/{1}\r'.format(j, len(xs)-1))
		ch.extend(struct.pack('<i', int(xs[j]*10000000.0)))
		ch.extend(struct.pack('<i', int(ys[j]*10000000.0)))
		ch.extend(struct.pack('<i', int(zs[j]*10000000.0)))
		ch.extend(struct.pack('<H', 0))
		ch.extend([1])
		ch.extend([0])
		ch.extend([45])
		ch.extend([0])
		ch.extend(struct.pack('<H', 0))
	
	fil.write(ch)
	fil.close()

def writeToXyz(lasFileName, xs, ys, zs):
	fil = open(lasFileName, "w+")

	for j in range(0, len(xs) - 1):
		sys.stdout.write( '{0}/{1}\r'.format(j, len(xs)-1))
		fil.write("{} {} {}\n".format(xs[j], ys[j], zs[j]))

	fil.close()
