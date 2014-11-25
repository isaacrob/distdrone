from IPython.parallel import Client
import os, sys
from .gears import *

def centersearch(size,progo='picluster',clearprompt='n',algorithm='edge'):
	#like ipparasearch, but start from a clustered position
	#use center-seeking and/or edge-seeking algorithm

	#start the controller and view
	#progo=raw_input('Profile? ')
	c=Client(profile=progo)
	dview=c[:]
	dview.block=False

	#import on engines
	with dview.sync_imports():
		import numpy
		from math import sqrt, ceil
		import time, sys

	numworkers=len(c.ids)
	#size=int(raw_input('How large of an area? '))
	#clearprompt=raw_input('Clear the screen? y/n ')
	#algorithm=raw_input('Which algorithm? edge/center ')+"seek"
	gen='bishop'
	bishopdic=[0,2,5,7,1,3,4,6]
	rookdic=[0,1,2,3,4,5,6,7]
	dicname=gen+"dic"

	#define organizational means and variables
	if gen=='bishop':
		def genmyspotlist(myspot): #bishop bias (for central use only)
			myspot=list(myspot)
			myspotlist=[None]*8
			myspotlist[0]=(myspot[0]-1,myspot[1]-1)
			myspotlist[4]=(myspot[0],myspot[1]-1)
			myspotlist[1]=(myspot[0]+1,myspot[1]-1)
			myspotlist[5]=(myspot[0]-1,myspot[1])
			myspotlist[6]=(myspot[0]+1,myspot[1])
			myspotlist[2]=(myspot[0]-1,myspot[1]+1)
			myspotlist[7]=(myspot[0],myspot[1]+1)
			myspotlist[3]=(myspot[0]+1,myspot[1]+1)
			return myspotlist
	elif gen=='rook':
		def genmyspotlist(myspot): #rook bias (for central use only)
			myspot=list(myspot)
			myspotlist=[None]*8
			myspotlist[4]=(myspot[0]-1,myspot[1]-1)
			myspotlist[0]=(myspot[0],myspot[1]-1)
			myspotlist[5]=(myspot[0]+1,myspot[1]-1)
			myspotlist[1]=(myspot[0]-1,myspot[1])
			myspotlist[2]=(myspot[0]+1,myspot[1])
			myspotlist[6]=(myspot[0]-1,myspot[1]+1)
			myspotlist[3]=(myspot[0],myspot[1]+1)
			myspotlist[7]=(myspot[0]+1,myspot[1]+1)
			return myspotlist
	else:
		def genmyspotlist(myspot): #basic bias (for central use only)
			myspot=list(myspot)
			myspotlist=[None]*8
			myspotlist[0]=(myspot[0]-1,myspot[1]-1)
			myspotlist[1]=(myspot[0],myspot[1]-1)
			myspotlist[2]=(myspot[0]+1,myspot[1]-1)
			myspotlist[3]=(myspot[0]-1,myspot[1])
			myspotlist[4]=(myspot[0]+1,myspot[1])
			myspotlist[5]=(myspot[0]-1,myspot[1]+1)
			myspotlist[6]=(myspot[0],myspot[1]+1)
			myspotlist[7]=(myspot[0]+1,myspot[1]+1)
			return myspotlist
	def genmyspotlist0(myspot): #-1-1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[0]=(myspot[0]-1,myspot[1]-1)
		myspotlist[1]=(myspot[0],myspot[1]-1)
		myspotlist[3]=(myspot[0]+1,myspot[1]-1)
		myspotlist[2]=(myspot[0]-1,myspot[1])
		myspotlist[5]=(myspot[0]+1,myspot[1])
		myspotlist[4]=(myspot[0]-1,myspot[1]+1)
		myspotlist[6]=(myspot[0],myspot[1]+1)
		myspotlist[7]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist7(myspot): #+1+1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[7]=(myspot[0]-1,myspot[1]-1)
		myspotlist[6]=(myspot[0],myspot[1]-1)
		myspotlist[4]=(myspot[0]+1,myspot[1]-1)
		myspotlist[5]=(myspot[0]-1,myspot[1])
		myspotlist[2]=(myspot[0]+1,myspot[1])
		myspotlist[3]=(myspot[0]-1,myspot[1]+1)
		myspotlist[1]=(myspot[0],myspot[1]+1)
		myspotlist[0]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist5(myspot): #-1+1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[3]=(myspot[0]-1,myspot[1]-1)
		myspotlist[5]=(myspot[0],myspot[1]-1)
		myspotlist[7]=(myspot[0]+1,myspot[1]-1)
		myspotlist[2]=(myspot[0]-1,myspot[1])
		myspotlist[6]=(myspot[0]+1,myspot[1])
		myspotlist[0]=(myspot[0]-1,myspot[1]+1)
		myspotlist[1]=(myspot[0],myspot[1]+1)
		myspotlist[4]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist2(myspot): #+1-1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[4]=(myspot[0]-1,myspot[1]-1)
		myspotlist[1]=(myspot[0],myspot[1]-1)
		myspotlist[0]=(myspot[0]+1,myspot[1]-1)
		myspotlist[6]=(myspot[0]-1,myspot[1])
		myspotlist[2]=(myspot[0]+1,myspot[1])
		myspotlist[7]=(myspot[0]-1,myspot[1]+1)
		myspotlist[5]=(myspot[0],myspot[1]+1)
		myspotlist[3]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist1(myspot): #0-1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[2]=(myspot[0]-1,myspot[1]-1)
		myspotlist[0]=(myspot[0],myspot[1]-1)
		myspotlist[1]=(myspot[0]+1,myspot[1]-1)
		myspotlist[3]=(myspot[0]-1,myspot[1])
		myspotlist[4]=(myspot[0]+1,myspot[1])
		myspotlist[6]=(myspot[0]-1,myspot[1]+1)
		myspotlist[7]=(myspot[0],myspot[1]+1)
		myspotlist[5]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist6(myspot): #0+1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[5]=(myspot[0]-1,myspot[1]-1)
		myspotlist[7]=(myspot[0],myspot[1]-1)
		myspotlist[6]=(myspot[0]+1,myspot[1]-1)
		myspotlist[4]=(myspot[0]-1,myspot[1])
		myspotlist[3]=(myspot[0]+1,myspot[1])
		myspotlist[1]=(myspot[0]-1,myspot[1]+1)
		myspotlist[0]=(myspot[0],myspot[1]+1)
		myspotlist[2]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist4(myspot): #+10 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[6]=(myspot[0]-1,myspot[1]-1)
		myspotlist[3]=(myspot[0],myspot[1]-1)
		myspotlist[2]=(myspot[0]+1,myspot[1]-1)
		myspotlist[7]=(myspot[0]-1,myspot[1])
		myspotlist[0]=(myspot[0]+1,myspot[1])
		myspotlist[5]=(myspot[0]-1,myspot[1]+1)
		myspotlist[4]=(myspot[0],myspot[1]+1)
		myspotlist[1]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist3(myspot): #-10 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[1]=(myspot[0]-1,myspot[1]-1)
		myspotlist[4]=(myspot[0],myspot[1]-1)
		myspotlist[5]=(myspot[0]+1,myspot[1]-1)
		myspotlist[0]=(myspot[0]-1,myspot[1])
		myspotlist[7]=(myspot[0]+1,myspot[1])
		myspotlist[2]=(myspot[0]-1,myspot[1]+1)
		myspotlist[3]=(myspot[0],myspot[1]+1)
		myspotlist[6]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	#dview['genmyspotlist']=genmyspotlist
	def createcenter(layer,midspot):
		midspot=list(midspot)
		layerspots=[None]*(8*(layer-1))
		def varyx(mult=1):
			thissection=[]
			for x in range(-1*(layer-1),layer+1):
				thissection.append(tuple([midspot[0]+mult*x,midspot[1]+mult*layer]))
			return thissection
		def varyy(mult=1):
			thissection=[]
			for y in range(-1*(layer-1),layer+1):
				thissection.append(tuple([midspot[0]+mult*layer,midspot[1]+-1*mult*y]))
			return thissection
		layerspots[0:2*(layer-1)-1]=varyx()
		layerspots[2*(layer-1):4*(layer-1)-1]=varyy()
		layerspots[4*(layer-1):6*(layer-1)-1]=varyx(mult=-1)
		layerspots[6*(layer-1):8*(layer-1)-1]=varyy(mult=-1)
		return layerspots
	def nearestzero(myspot,map):
		myspotlist=genmyspotlist(myspot)
		listofbadspots=[]
		for i in range(0,8):
			if len(map) in myspotlist[i] or -1 in myspotlist[i]:
				listofbadspots.append(myspotlist[i])
		for i in listofbadspots:
			myspotlist.remove(i)
		x,y=numpy.where(map==0)
		zerospots=zip(x,y)
		if len(zerospots)==0:
			print 'could not find any zeros, will stay put'
			return myspot
		zerodists=[None]*len(zerospots)
		for i in range(0,len(zerospots)):
			zerodists[i]=sqrt((myspot[0]-zerospots[i][0])**2+(myspot[1]-\
				   zerospots[i][1])**2)
		closestzero=zerospots[zerodists.index(min(zerodists))]
		distlist=[None]*len(myspotlist)
		for i in range(0,len(myspotlist)):
			distlist[i]=sqrt((closestzero[0]-myspotlist[i][0])**2+\
					 (closestzero[1]-myspotlist[i][1])**2)
		return tuple(myspotlist[distlist.index(min(distlist))])
	dview['nearestzero']=nearestzero
	background=numpy.zeros((size,size))
	spots=[None]*numworkers
	def updatemap():
		for spot in spots:
			background[spot[0],spot[1]]=background[spot[0],spot[1]]+1;

	#define different search methods and push to engines
	def purgelist(myspotlist,map,nope=False,best=False):
		if nope:
			if best:
				myspotlist.remove(nope)
			else:
				for i in range(len(nope)):
					if not len(nope[i])==2:
						aowrungoaew
					if nope[i] in myspotlist:
						myspotlist.remove(nope[i])
		listofbadspots=[]
		for i in range(0,len(myspotlist)):
			if len(map) in myspotlist[i] or -1 in myspotlist[i] or map[\
						 myspotlist[i][0],myspotlist[i][1]]!=0:
				listofbadspots.append(myspotlist[i])
		for i in listofbadspots:
			myspotlist.remove(i)
		return myspotlist
	dview["purgelist"]=purgelist
	def edgeseek(center,myspot,map,nope=False):
		if type(myspot[0])==tuple:
			myspot=myspot[0]
		oktogo=0
		repeats=0
		myspotlist=genmyspotlist(myspot)
		#if nope:
		#	if len(nope)>2:
		#		if nope[len(nope)-2]==nope[len(nope)-1]:
		#			nope=nope[len(nope)-1]
		myspotlist=purgelist(myspotlist,map,nope)
		if len(myspotlist)==0:
			return [nearestzero(myspot,map),0]
		#if len(myspotlist)==1:
		#	return list(tuple(myspotlist[0]),1)
		distlist=[None]*len(myspotlist)
		for i in range(len(distlist)):
			distlist[i]=sqrt((center[0]-myspotlist[i][0])**2+(center[1]-\
						myspotlist[i][1])**2)
		bestspot=tuple(myspotlist[distlist.index(max(distlist))])
		bestspotlist=purgelist(genmyspotlist(bestspot),map,myspot,1)
		locklist=[]
		needtoloop=len(bestspotlist)==1# and bestspotlist[0] in myspotlist
		oldbestspots=[]
		locklist=[]
		while needtoloop:
			if not len(locklist)==0:
				oldbestspots.append(deepbestspot)
			else:
				oldbestspots.append(myspot)
				oldbestspots.append(bestspot)
			deepbestspot=bestspotlist[0]
			locklist.append(deepbestspot)
			bestspotlist=purgelist(genmyspotlist(deepbestspot),map,oldbestspots)
			for spot in locklist:
				if spot in bestspotlist:
					bestspotlist.remove(spot)
			if len(bestspotlist)==1:
				deepbestspot=bestspotlist[0]
			else:
				needtoloop=0
			#return [bestspot,tuple(bestspotlist[0])]
		#if nope:
		#	if len(nope)==1:
		#		sys.stdout.write("something has gone terribly wrong"+str(nope))
		#		if list(bestspot)==list(nope[0]):
		#			aosinruaonergapojrg
		if len(locklist)>0:
			return [bestspot,tuple(locklist)]
		else:
			return [bestspot,0]
		#if len(myspotlist)==1:
		#	return [bestspot,myspotlist[0]]
		#return [bestspot,0]
	dview['edgeseek']=edgeseek
	def centerseek(center,myspot,map,nope=False):
		if type(myspot[0])==tuple:
			myspot=myspot[0]
		oktogo=0
		repeats=0
		#for now, redefining center to be center of map
	
		myspotlist=genmyspotlist(myspot)
		if nope:
			myspotlist.remove(nope)
		listofbadspots=[]
		for i in range(0,len(myspotlist)):
			if len(map) in myspotlist[i] or -1 in myspotlist[i] or map[\
						 myspotlist[i][0],myspotlist[i][1]]!=0:
				listofbadspots.append(myspotlist[i])
		for i in listofbadspots:
			myspotlist.remove(i)
		if len(myspotlist)==0:
			return nearestzero(myspot,map)
		#if len(myspotlist)==1:
		#	return list(tuple(myspotlist[0]),1)
		if len(myspotlist)==1:
			print "only one option"
			return tuple(myspotlist[0])
		distlist=[None]*len(myspotlist)
		for i in range(0,len(distlist)):
			distlist[i]=sqrt((center[0]-myspotlist[i][0])**2+(center[1]-\
						myspotlist[i][1])**2)
		return tuple(myspotlist[distlist.index(min(distlist))])
	#only difference between the 2 algorithms is min v max in the last line
	dview["centerseek"]=centerseek

	#initialize map w/ clustered drones
	midspot=tuple([size/2,size/2])
	midspots=genmyspotlist(midspot)
	background[midspot[0],midspot[1]]=1 #saying center of release is known
	if numworkers<=8:
		spots=midspots[:numworkers]
		for i in range(numworkers):
			exec 'alignbias='+dicname+'['+str(i)+']' in globals(), locals()
			exec 'c[c.ids[i]]["genmyspotlist"]=genmyspotlist'+str(alignbias) in globals(), locals()
			exec 'print str(c.ids[i])+" is algorithm "+str(alignbias)' in globals(), locals()
	else:
		for layer in range(2,(int(sqrt(numworkers))+1)/2+2):
			thislayerend=min(8*(layer-1),numworkers)
			thislayerstart=8*(layer-2)
			spots[thislayerstart:thislayerend]=createcenter(layer,midspot)[:thislayerend-thislayerstart]
	for worker in spots:
		print "worker at "+str(worker)
	updatemap()
	oldspots=[]
	oldspots.append(tuple(spots))
	iteration=1
	alert=0

	#start the search
	if clearprompt=='y':
		os.system('clear')
	print 'starting the search'
	print 'iteration '+str(iteration)
	print background

	while 0 in background:
		dview=c[:]
		if iteration==1:
			print 'starting at '+str(spots)
		#else:
		#	print str(oldspots[iteration-2])+' >>> '+str(spots)
		center=[None,None]
		center[0]=sum([x for x,y in spots])/len(spots)
		center[1]=sum([y for x,y in spots])/len(spots)
		starttime=time.time()
		dview.scatter('myspot',spots)
		dview['center']=center
		if algorithm=='centerseek':
			dview['center']=midspot
		dview['map']=background
		dview.execute('[newspot,mylocks]='+algorithm+'(center,myspot,map)')
		locklist=[]
		for i in c.ids:
			thislocks=c[i]["mylocks"]
			if thislocks:
				#print thislocks
				for j in thislocks:
					locklist.append(j)
		dview["locklist"]=locklist
		#print locklist
		for i in c.ids: #or use dview.gather, but duplicates
			intermid=c[i]['newspot']
			lockviolation=0
			if intermid in locklist:
				lockviolation=1
				#print "attempt to move into lock by "+str(i)
			if (not intermid in spots) and not lockviolation:
				spots[c.ids.index(i)]=intermid
			else:
				#print 'possible problem with '+str(i)
				#if crashtest==3:
				#	sys.exit('drone '+str(i)+' stalled')
				c[i].execute("locklist.append(newspot)")
				c[i].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist)')
				intermid=c[i]['newspot']
				if intermid in spots:
					#print "possible meta problem with "+str(c.ids[spots.index(intermid)])
					spots[c.ids.index(i)]=intermid
					c[c.ids[spots.index(intermid)]].execute("locklist.append(newspot)")
					c[c.ids[spots.index(intermid)]].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist)')
					spots[spots.index(intermid)]=c[c.ids[spots.index(intermid)]]["newspot"]
				#if spots[i]==oldspots[iteration-1][i]:
				#	crashtest=crashtest+1
					#print str(i)+"/"+str(intermid)+" got here, with other locklist "+str(c[c.ids[spots.index(intermid)]]["mylocks"])
					if intermid in spots:
						#print locklist
						#c[i].execute("locklist=[newspot,]")
						c[i]["locklist"]=[intermid,]
						#print c[i]["locklist"]
						c[i].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist)')
						intermid=c[i]['newspot']
						#print intermid
						#print "possible contradiction problem here with "+str(i)
						spots[c.ids.index(i)]=intermid
				else:
					spots[c.ids.index(i)]=intermid
		updatemap()
		oldspots.append(tuple(spots))
		iteration=iteration+1
		if clearprompt=='y':
			os.system('clear')
		print 'iteration '+str(iteration)
		print background
		print 'percent done: '+str(float((background>0).sum())/(size**2)*100)+'%'
		print str(oldspots[iteration-2])+' >>> '+str(spots)
		if (background>1).sum()>0 and alert==0:
			if raw_input("imperfect search. continue? y/n ")=='n':
				sys.exit("exiting")
			else:
				alert=1

	#once done, print the final report
	print 'final report: '
	print "moves wasted: (doesn't account for necessary moves) "+str(-size**2+numworkers*iteration+1)
	print 'workers: '+str(numworkers)
	print 'number of squares: '+str(size**2)
	print 'extra iterations: '+str(iteration-ceil(size**2/numworkers))
	print 'percent error in terms of iterations: '+str((iteration-\
					ceil(size**2/numworkers\
					))/iteration*100)+'%'
	if alert==1:
		print "imperfect"
	else:
		print "perfect"