#from .imgproc import *
import gentimedist as gen
import cv2, time, sys, cPickle, zmq, os, copy, psutil
from math import log
from IPython.parallel import Client
from scipy import stats
import numpy as np

def findfaceswithtrigger(profile='picluster',threshold=15,n=100,serial='no',show=False):
	import sys, cPickle, os
	pidfile=open('mypythonpid','w')
	cPickle.dump(os.getpid(),pidfile)
	pidfile.close()
	runstate=open('runstate','w')
	cPickle.dump(0,runstate)
	runstate.close()
	print os.getpid()
	#context=zmq.Context()
	#pubsocket=context.socket(zmq.PUB)
	#port=5556
	#pubsocket.bind("tcp://*:%s"%port)
	#subsocket=context.socket(zmq.SUB)
	if sys.platform=='darwin':
		ips=open("/Users/isaac/Code/parastuff/ipaddresses").read()
	if sys.platform=='linux2':
		ips=open("/home/pi/ipaddresses").read()
	splitips=ips.split("\n")
	print splitips
	#for ip in splitips:
	#	if ip:
	#		subsocket.connect("tcp://%s:%s"%(ip,port))
	#subsocket.setsockopt(zmq.SUBSCRIBE,"need quiet?")

	c=Client(profile=profile)
	dview=c[:]
	numnodes=len(c.ids)
	dview.block=False
	with dview.sync_imports():
		import cv2,sys,time,math,os,cPickle,signal
	#dview.execute("mypid=os.getpid()")
	def getmypid():
		import cPickle
		try:
			file=open('mypythonpid','r')
			mypid=cPickle.load(file)
			file.close()
		except:
			mypid=False
		return mypid
	def getrunstate():
		import cPickle
		try:
			file=open('runstate','r')
			state=cPickle.load(file)
			file.close()
		except:
			state=0
		return state
	dview["getrunstate"]=getrunstate
	dview["getmypid"]=getmypid
	dview.execute("mypid=getmypid()")
	myippid=-1
	for proc in psutil.process_iter():
		if proc.name()=='ipengine':
			myippid=proc.pid
	ippids=[]
	dview.execute("enginepid=os.getpid()")
	for i in range(numnodes):
		if not myippid==c[c.ids[i]]['enginepid']:
			ippids.append(c.ids[i])
	dview=c.activate(ippids)
	
	print dview
	numnodes=len(dview)
	rejects=numnodes-len(c.ids)
	print "configured for this pi by rejecting a certain engine"
	print sys.platform
	if sys.platform=='darwin':
		facedetector=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	elif sys.platform=='linux2':
		facedetector=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")
	else: 
		print "something went wrong detecting the system"
	times=gen.loadtimes()
	scale=1.1
	dview["scale"]=scale
	for i in ippids:
		c[i].execute('if sys.platform=="darwin": haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")')
		c[i].execute('if sys.platform=="linux2": haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")')
	
	numsizes=len(times)
	trans=[None]*numsizes
	for i in range(numsizes):
		trans[i]=int(20*(scale**i))
	
	mintime=min(times)
	times=[thistime-mintime for thistime in times]

	print "predicting even distribution..."
	def predictdist(numnodes,times,numsizes,c):
		timepernode=sum(times)/numnodes
		thresholds=[None]*(numnodes+1)
		thresholds[0]=0
		for i in range(1,numnodes+1):
			j=thresholds[i-1]+1
			while sum(times[thresholds[i-1]:j])<timepernode and j<numsizes:
				j=j+1
				#print j
				#time.sleep(3)
			if sum(times[thresholds[i-1]:j])-timepernode>timepernode-sum(times[thresholds[i-1]:j-1]):
				j=j-1 #makes more even, but last few take longest...otherwise even but last is really short
			thresholds[i]=j
		thresholds[numnodes]=numsizes-1
		for i in range(numnodes):
			c[ippids[i]]['thismin']=tuple([trans[thresholds[i]]-1]*2)
			c[ippids[i]]['thismax']=tuple([trans[thresholds[i+1]]+1]*2)
	predictdist(numnodes,times,numsizes,c)
	
	def findfaces(img,scale,serial):
		starttime=time.time()
		numnodes=len(ippids)
		img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		dview['img']=img
		dview.execute('img=img.copy()')
		dview.execute("mypid=getmypid()")
		runstate=open('runstate','w')
		cPickle.dump(1,runstate)
		runstate.close()
		dview.execute("state=getrunstate()")
		#for i in range(numnodes):
		#	print c[c.ids[i]]["state"]
		dview.execute("if mypid and not state: os.kill(mypid,signal.SIGTSTP)")
		dview.execute("exectime=time.time();myfaces=haarface.detectMultiScale(img,scale,4,1,thismin,thismax);exectime=time.time()-exectime;endtime=time.time()",block=False)
		faces=set()
		thistimes=[None]*numnodes
		thistimesremote=[None]*numnodes
		for i in range(numnodes):
			thistimes[i]=time.time()
			print "checking engine "+str(ippids[i])
			thisfaces=c[ippids[i]]["myfaces"]
			thistimesremote[i]=c[ippids[i]]["exectime"]
			print len(thisfaces)
			if len(thisfaces)>0:
				for face in thisfaces:
					faces.add(tuple(face))
			thistimes[i]=time.time()-thistimes[i]
		print thistimes
		print thistimesremote

		duptime=time.time()
		facelist=list(faces)
		donttest=[]
		finallist=[]
		testlen=len(facelist)
		origlist=facelist
		testlennew=0
		print len(origlist)
		while not testlennew==testlen:
			testlen=len(facelist)
			for first in range(len(facelist)):
				if first not in donttest:
					for second in range(first+1,len(facelist)):
						sub=facelist[first]
						j=facelist[second]
						var=abs(j[3]-sub[3])/2
						if ((j[0]+j[3]/2-var<sub[0]+sub[3]/2) and (j[0]+j[3]/2+var>sub[0]+sub[3]/2)) and ((j[1]+j[2]/2-var<sub[1]+sub[2]/2) and (j[1]+j[2]/2+var>sub[1]+sub[2]/2)) and min([float(j[3])/sub[3],float(sub[3])/j[3]])>1.0/2.0:
							donttest.append(first)
							donttest.append(second)
							#facelist.append(tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2]))
							inter=tuple([(j[0]+sub[0])/2,(j[1]+sub[1])/2,(j[2]+sub[2])/2,(j[3]+sub[3])/2])
							finallist.append(inter)
							break
					if first not in donttest:
						finallist.append(facelist[first])
			testlennew=len(finallist)
			facelist=finallist
			finallist=[]
			donttest=[]
		finallist=facelist
		duptime=time.time()-duptime
		print len(finallist)
		starttime=time.time()-starttime
		print "min/avg/max/regtime/tottime: "+str(min(thistimesremote))+"/"+str(sum(thistimesremote)/numnodes)+"/"+str(max(thistimesremote))+"/"+str(starttime)+"/"+str(sum(thistimesremote))

		if serial=='yes':
			serialtime=time.time()
			facedetector.detectMultiScale(img,scale,4,1)
			serialtime=time.time()-serialtime
			print serialtime
		
		dview.execute("if mypid: os.kill(mypid,signal.SIGCONT)")
		#for i in range(numnodes):
		#	print c[c.ids[i]]['mypid']
		runstate=open('runstate','w')
		cPickle.dump(0,runstate)
		runstate.close()
		return finallist
	
	def calibcam(n,cam):
		sumlist=[None]*n
		for i in range(n):
			retval,img=cam.read()
			xstart=img.shape[0]/4
			ystart=img.shape[1]/4
			sumlist[i]=img[xstart:(xstart*3),ystart:(ystart*3),:].sum()
		return sumlist
	
	cam=cv2.VideoCapture(0)
	
	retval,img=cam.read()
	gen.dumptimes(img,scale=1.1)
	
	sumlist=calibcam(n,cam)
	std=stats.tstd(sumlist)
	avg=sum(sumlist)/n
	framenum=0
	oldids=ippids
	
	print "starting detection"
	
	while True:
		retval,img=cam.read()
		xstart=img.shape[0]/4
		ystart=img.shape[1]/4
		thisz=(img[xstart:(xstart*3),ystart:(ystart*3),:].sum()-avg)/std
		#while True:
		#	print "testing for sleep needed"
		#	try:
		#		if subsocket.recv(flags=zmq.NOBLOCK)=="need quite? yes":
		#			print "need sleep"
		#			while True:
		#				try:
		#					if subsocket.recv(flags=zmq.NOBLOCK)=="need quite? not anymore":
		#						break
		#				except:
		#					pass
		#				time.sleep(.5)
		#	except:
		#		break
		if abs(thisz)>threshold:
			print "something weird, zscore="+str(thisz)
			time.sleep(.5)
		#	pubsocket.send("need quiet? yes")
			retval,newimg=cam.read() #works well on mac, maybe not pis...
			#if not len(c.ids)==len(oldids): #done periodically, not ideal to update here...
			#	print "cluster changed"
			#	numnodes=len(c.ids)
			#	dview=c[:]
			#	print "repredicting even distribution..."
			#	predictdist(numnodes,times,numsizes,c)
			#	for id in c.ids:
			#		if id not in oldids:
			#			c[id].execute('import cv2,sys,time,math,os,cPickle,signal;myfaces=[]')
			#			c[id]['getrunstate']=getrunstate
			#			c[id]['getmypid']=getmypid
			#			c[id]['scale']=scale
			#			c[id].execute('haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")')
					#else:
					#	c[id].execute('myfaces=[]')
			#	oldids=c.ids
			print "searching for faces..."
			faces=findfaces(newimg,scale,serial)
		#	pubsocket.send("need quiet? not anymore")
			if len(faces)>0:
				print "FOUND A FACEZ!!!!!11!"
				if show==True:
					for (x,y,h,w) in faces:
						cv2.rectangle(newimg,(x,y),(x+w,y+h),(0,255,255),1)
					#cv2.imshow("obj num "+str(i),newimg)
					cv2.imshow("obj found",newimg)
			else:
				print "no facez :("
				if show==True:
					cv2.imshow("obj not found",newimg)
			if show==True:
				cv2.waitKey(1)
			sumlist[0]=img[xstart:(xstart*3),ystart:(ystart*3),:].sum()
			std=stats.tstd(sumlist)
			avg=sum(sumlist)/n
		#else:
		#	pubsocket.send("need quiet? no")
		framenum=framenum+1
		if framenum%10==0:
			sumlist[0]=img[xstart:(xstart*3),ystart:(ystart*3),:].sum()
			std=stats.tstd(sumlist)
			avg=sum(sumlist)/n
		#if framenum%100==0:
		#	print framenum
		if framenum%(10*numnodes)==0:
			if not len(c.ids)-len(oldids)==rejects:
				print "cluster changed"
				numnodes=len(c.ids)
				dview=c[:]
				print "repredicting even distribution..."
				predictdist(numnodes,times,numsizes,c)
				for id in c.ids:
					if id not in oldids:
						c[id].execute('import cv2,sys,time,math,os,cPickle,signal;myfaces=[]')
						c[id]['getrunstate']=getrunstate
						c[id]['getmypid']=getmypid
						c[id]['scale']=scale
						c[id].execute('haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")')
					#else:
					#	c[id].execute('myfaces=[]')
				oldids=c.ids
				#c.spin()
				#trying reseting the client
				c=Client(profile=profile)
				dview=c[i]
				myippid=-1
				for proc in psutil.process_iter():
					if proc.name()=='ipengine':
						myippid=proc.pid
				ippids=[]
				dview.execute("enginepid=os.getpid()")
				for i in range(numnodes):
					if not myippid==c[c.ids[i]]['enginepid']:
						ippids.append(c.ids[i])
				dview=c.activate(ippids)


def getalignface(facefinder,eyefinder,nosefinder,cam):
	cv2.destroyAllWindows()
	print "finding faces..."
	retval,img=cam.read()
	if not retval:
		print "could not read image"
	cv2.imshow("img",img)
	#cv2.imshow("img",img)
	dims=facefinder.detectMultiScale(img,1.1,5,1,(20,20),img.shape[:2])
	print dims
	if len(dims)>0:
		sizelist=[w for (x,y,h,w) in dims]
		maxsize=max(sizelist)
		biggestface=[[x,y,h,w] for (x,y,h,w) in dims if w==maxsize and w>60]
		print biggestface
		if len(biggestface)>0:
			print "finding facial features..."
			for (x,y,h,w) in biggestface:
				thisface=img[x:(x+w),y:(y+h),:]
				cleanface=copy.deepcopy(thisface)
			cv2.imshow("thisface",thisface)
			eyes=eyefinder.detectMultiScale(thisface,1.1,30,1)
			noses=nosefinder.detectMultiScale(thisface,1.1,20,1)
			print "eyes: "+str(eyes)
			print "noses: "+str(noses)
			if len(noses)>0 and len(eyes)>1:
				maxnosesize=max([w for (x,y,h,w) in noses])
				biggestnose=[[x,y,h,w] for (x,y,h,w) in noses if w==maxnosesize][0]
				finaleyes=[]
				print "filtering out nostrils from the eyes..."
				for eye in eyes:
					if not (eye[0]>(biggestnose[0]-5) and eye[0]<(biggestnose[0]+biggestnose[3]+5) and eye[1]>(biggestnose[1]-5) and eye[1]<(biggestnose[1]+biggestnose[2]+5)):
						finaleyes.append(eye)
				print "eyes: "+str(finaleyes)
				print "noses: "+str(noses)
				for (x,y,h,w) in finaleyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				for (x,y,h,w) in [biggestnose]:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(255,255,0),1)
				#print biggestnose
			elif len(eyes)>1 and len(eyes)<3:
				print "could not find a nose, found 2 eyes. working with them"
				for (x,y,h,w) in eyes:
					cv2.rectangle(thisface,(x,y),(x+w,y+h),(0,255,255),1)
				cv2.imshow("thisface",thisface)
				finaleyes=eyes
			else: #add parsing for more than 2 detected eyes without a nose
				print "feature detection went wrong"
				return []
			cv2.imshow("thisface features",thisface)
			eye1mid=(finaleyes[0][0]+finaleyes[0][3]/2,finaleyes[0][1]+finaleyes[0][2]/2)
			try:
				eye2mid=(finaleyes[1][0]+finaleyes[1][3]/2,finaleyes[1][1]+finaleyes[1][2]/2)
			except:
				print "something went wrong with the format of eyes, skipping to next iteration"
				return []
			if eye1mid[0]<eye2mid[0]:
				lefteye=eye1mid
				righteye=eye2mid
			else:
				lefteye=eye2mid
				righteye=eye1mid
			borderoffset=9.0/12.0
			midborderoffset=3
			eyetriangle=[righteye[0]-lefteye[0],righteye[1]-lefteye[1]]
			topbordermid=[lefteye[0]+eyetriangle[0]/2+eyetriangle[1]/midborderoffset,lefteye[1]+eyetriangle[1]/2-eyetriangle[0]/midborderoffset]
			topborder=[(topbordermid[0]-int(eyetriangle[0]*borderoffset),topbordermid[1]-int(eyetriangle[1]*borderoffset)),(topbordermid[0]+int(eyetriangle[0]*borderoffset),topbordermid[1]+int(eyetriangle[1]*borderoffset))]
			bordertriangle=[topborder[1][0]-topborder[0][0],topborder[1][1]-topborder[0][1]]
			borderlength=int(np.sqrt(bordertriangle[0]**2+bordertriangle[1]**2))
			print bordertriangle
			border=[topborder[0],topborder[1],(topborder[1][0]-bordertriangle[1],topborder[1][1]+bordertriangle[0]),(topborder[0][0]-bordertriangle[1],topborder[0][1]+bordertriangle[0])]
			violation=0
			for i in range(4):
				for j in range(2):
					if border[i][j]>thisface.shape[0] or border[i][j]<0:
						violation=1			
			if violation:
				print "could not align face, features too close to edge"
			else:
				print "aligning face"
				cv2.line(thisface,eye1mid,eye2mid,(255,0,0),1)
				cv2.line(thisface,border[0],border[1],(0,255,0),1)
				cv2.line(thisface,border[2],border[3],(0,255,0),1)
				cv2.line(thisface,border[0],border[3],(0,255,0),1)
				cv2.line(thisface,border[1],border[2],(0,255,0),1)
				#cv2.line(thisface,(nosemid[0]+eyedist,nosemid[1]+noseedgeoffset),(nosemid[0]-eyedist,nosemid[1]+noseedgeoffset),(0,255,0),1)
				facecenter=tuple(np.array([border[0][0]+border[2][0],border[0][1]+border[2][1]])/2)
				cv2.circle(thisface,facecenter,5,(255,0,0),-1)
				cv2.imshow("thisface border",thisface)
				rotationangle=np.arctan(float(eyetriangle[1])/float(eyetriangle[0]))
				rotationmat=cv2.getRotationMatrix2D(facecenter,rotationangle*180/np.pi,1.0)
				print border[0]
				bordercenteroffset=[border[0][0]-facecenter[0],border[0][1]-facecenter[1]]
				print bordercenteroffset
				borderoffsetafterrotation=[bordercenteroffset[0]*np.cos(rotationangle)+bordercenteroffset[1]*np.sin(rotationangle),bordercenteroffset[0]*np.sin(rotationangle)-bordercenteroffset[1]*np.cos(rotationangle)-borderlength]
				print borderoffsetafterrotation
				borderafterrotation=(int(borderoffsetafterrotation[0]+facecenter[0]),int(borderoffsetafterrotation[1]+facecenter[1]))
				print borderafterrotation
				finalface=cv2.warpAffine(thisface,rotationmat,thisface.shape[:2],flags=cv2.INTER_LINEAR)
				finalcroppedface=finalface[borderafterrotation[1]:borderlength+borderafterrotation[1],borderafterrotation[0]:borderafterrotation[0]+borderlength]
				cv2.circle(finalface,borderafterrotation,3,(0,255,0),-1)
				#cv2.circle(finalface,(borderafterrotation[0],borderafterrotation[1]-borderlength),3,(0,255,0),-1)
				cv2.circle(finalface,facecenter,4,(0,255,255),-1)
				cv2.imshow("rotated",finalface)
				cv2.imshow("final cropped face",finalcroppedface)
				cleanface=cv2.warpAffine(cleanface,rotationmat,thisface.shape[:2],flags=cv2.INTER_LINEAR)[borderafterrotation[1]:borderlength+borderafterrotation[1],borderafterrotation[0]:borderafterrotation[0]+borderlength]
				cv2.imshow("clean face",cleanface)
				cleanface=cv2.cvtColor(cleanface,cv2.COLOR_BGR2GRAY)
				cleanface=cv2.resize(cleanface,(60,60))
				cv2.imshow("small clean face",cleanface)
				return cleanface
			while 1:
				k=cv2.waitKey(10)
				if k==27:
					break
				else:
					continue
	return []


def makepredictor():
	imgset=[]
	labels=[]
	facefinder=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")
	eyefinder=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_eye.xml")
	nosefinder=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_mcs_nose.xml")
	cam=cv2.VideoCapture(-1)
	while not raw_input("capture image? y/n ")=='n':
		face=getalignface(facefinder,eyefinder,nosefinder,cam)
		if len(face)>0:
			if not raw_input("is this the correct face? y/n ")=='n':
				imgset.append(face)
				labels.append(int(raw_input("who is this? (int) ")))

	labels=np.array(labels)
	facerec=cv2.createLBPHFaceRecognizer()
	facerec.train(imgset,labels)
	return facerec