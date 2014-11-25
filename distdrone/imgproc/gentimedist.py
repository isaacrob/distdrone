import cv2, time, sys, cPickle
from math import log
def gentimedist(imgname,slices=False,scale=1.1,invert=0):
	if sys.platform=='darwin':
		if type(imgname)=='str':
			img=cv2.imread("/Users/isaac/Code/"+imgname)#raw_input("image? "))
		else:
			img=imgname
		haarface=cv2.CascadeClassifier("/usr/local/Cellar/opencv/2.4.9/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
	elif sys.platform=='linux2':
		if type(imgname)=='str':
			img=cv2.imread("/home/pi/"+imgname)
		else:
			img=imgname
		haarface=cv2.CascadeClassifier("/home/pi/opencv-2.4.9/data/haarcascades/haarcascade_frontalface_alt2.xml")
	#numstages=10
	print "got here (yet again)"
	try:
		sp=img.shape
		sp=min(sp[:1])
	except:
		print "could not read image"
		sys.exit("could not read image")
	if not slices:
		slices=int(log(sp/20)/log(scale))
		uselog=True
	else:
		uselog=False
	if slices>sp:
		print "too many slices, using sp"
		slices=sp
	inc=(sp-20)/slices
	trans=[None]*slices
	times=[None]*(slices-1)
	if uselog:
		for i in range(slices):
			trans[i]=int(20*(scale**i))
		#print trans
	else:
		for i in range(slices):
			trans[i]=int(inc*(i))+20
	for i in range(slices-1):
		times[i]=time.time()
		haarface.detectMultiScale(img,scale,1,1,tuple([trans[i]-1]*2),tuple([trans[i]+1]*2))
		times[i]=(time.time()-times[i])
		if invert:
			times[i]=1/times[i]**2
	print max(times)
	print min(times)
	print sum(times)/len(times)
	return times
def dumptimes(imgname,filename="timedistinfo",slices=False,scale=1.01,invert=0):
	times=gentimedist(imgname,slices,scale,invert)
	file=open(filename,"w")
	cPickle.dump(times,file)
	file.close()
	print "dumped time info to "+filename
def loadtimes(filename="timedistinfo"):
	file=open(filename,"r")
	times=cPickle.load(file)
	file.close()
	return times
def findratios(imgname,ratios=1,mag=10,slices=100,scale=1.1,invert=0):
	metatimes=[[None]]*(ratios+1)
	for i in range(ratios+1):
		metatimes[i]=gentimedist(imgname,slices,((scale-1)*(mag**(-i))+1),invert)
	for i in range(ratios):
		thisratio=[None]*(slices-1)
		for j in range(slices-1):
			thisratio[j]=(metatimes[i+1][j]-min(metatimes[i+1])+.05)/(metatimes[i][j]-min(metatimes[i])+.05)
		print thisratio
		print max(thisratio)
		print min(thisratio)
		print sum(thisratio)/(slices-1)