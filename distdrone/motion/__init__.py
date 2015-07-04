from IPython.parallel import Client
import os, sys, pygame, Tkinter, tkMessageBox
from .gears import *

def centersearch(size,progo='picluster',clearprompt='n',algorithm='edgeseek'):
	#like ipparasearch, but start from a clustered position
	#use center-seeking and/or edge-seeking algorithm

	#start the controller and view
	#progo=raw_input('Profile? ')
	c=Client(profile=progo)
	dview=c[:]
	dview.block=False
	dview.use_dill()

	#import on engines
	with dview.sync_imports():
		import numpy
		from math import sqrt, ceil
		import time, sys
	
	pygame.init()

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
		myspotlist[4]=(myspot[0]-1,myspot[1]-1)
		myspotlist[5]=(myspot[0],myspot[1]-1)
		myspotlist[7]=(myspot[0]+1,myspot[1]-1)
		myspotlist[2]=(myspot[0]-1,myspot[1])
		myspotlist[6]=(myspot[0]+1,myspot[1])
		myspotlist[0]=(myspot[0]-1,myspot[1]+1)
		myspotlist[1]=(myspot[0],myspot[1]+1)
		myspotlist[3]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist2(myspot): #+1-1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[3]=(myspot[0]-1,myspot[1]-1)
		myspotlist[2]=(myspot[0],myspot[1]-1)
		myspotlist[0]=(myspot[0]+1,myspot[1]-1)
		myspotlist[6]=(myspot[0]-1,myspot[1])
		myspotlist[1]=(myspot[0]+1,myspot[1])
		myspotlist[7]=(myspot[0]-1,myspot[1]+1)
		myspotlist[5]=(myspot[0],myspot[1]+1)
		myspotlist[4]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist1(myspot): #0-1 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[2]=(myspot[0]-1,myspot[1]-1)
		myspotlist[0]=(myspot[0],myspot[1]-1)
		myspotlist[1]=(myspot[0]+1,myspot[1]-1)
		myspotlist[4]=(myspot[0]-1,myspot[1])
		myspotlist[3]=(myspot[0]+1,myspot[1])
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
		myspotlist[3]=(myspot[0]-1,myspot[1])
		myspotlist[4]=(myspot[0]+1,myspot[1])
		myspotlist[1]=(myspot[0]-1,myspot[1]+1)
		myspotlist[0]=(myspot[0],myspot[1]+1)
		myspotlist[2]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist4(myspot): #+10 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[6]=(myspot[0]-1,myspot[1]-1)
		myspotlist[4]=(myspot[0],myspot[1]-1)
		myspotlist[2]=(myspot[0]+1,myspot[1]-1)
		myspotlist[7]=(myspot[0]-1,myspot[1])
		myspotlist[0]=(myspot[0]+1,myspot[1])
		myspotlist[5]=(myspot[0]-1,myspot[1]+1)
		myspotlist[3]=(myspot[0],myspot[1]+1)
		myspotlist[1]=(myspot[0]+1,myspot[1]+1)
		return myspotlist
	def genmyspotlist3(myspot): #-10 biased. need to bias according to start
		myspot=list(myspot)
		myspotlist=[None]*8
		myspotlist[1]=(myspot[0]-1,myspot[1]-1)
		myspotlist[3]=(myspot[0],myspot[1]-1)
		myspotlist[5]=(myspot[0]+1,myspot[1]-1)
		myspotlist[0]=(myspot[0]-1,myspot[1])
		myspotlist[7]=(myspot[0]+1,myspot[1])
		myspotlist[2]=(myspot[0]-1,myspot[1]+1)
		myspotlist[4]=(myspot[0],myspot[1]+1)
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
	def findwalledge(myspot,wallspot,genmyspotlist,map,nope=False):
		myspotlist=[]
		for spot in genmyspotlist(wallspot):
			if not (-1 in spot or len(map) in spot):
				if map[spot[0],spot[1]]==-1 and any([map[spot2[0],spot2[1]]!=-1 for spot2 in genmyspotlist(spot) if not (-1 in spot2 or len(map) in spot2)]):
					myspotlist.append(spot)
		#myspotlist=[spot for spot in genmyspotlist(wallspot) if map[spot[0],spot[1]]==-1 and any([map[spot2[0],spot2[1]]!=-1 for spot2 in genmyspotlist(spot)])]
		fluffspots=set()
		for spot in myspotlist:
			for spot2 in genmyspotlist(spot):
				if not (-1 in spot2 or len(map) in spot2):
					if map[spot2[0],spot2[1]]!=-1 and checkcontinuity(myspot,genmyspotlist,map,spot2):
						fluffspots.add(tuple(spot2))
		if len(fluffspots)==0:
			returnlist=[]
			if abs(myspot[0]-wallspot[0])==1 and abs(myspot[1]-wallspot[1])==1:
				return [[wallspot[0],myspot[1]],[myspot[0],wallspot[1]]]
			elif abs(myspot[0]-wallspot[0])==1:
				if not myspot[1]-1<0:
					returnlist.append([wallspot[0],wallspot[1]-1])
					returnlist.append([myspot[0],myspot[1]-1])
				if not myspot[1]+1>=len(map):
					returnlist.append([wallspot[0],wallspot[1]+1])
					returnlist.append([myspot[0],myspot[1]+1])
				return returnlist
			elif abs(myspot[1]-wallspot[1])==1:
				if not myspot[0]-1<0:
					returnlist.append([wallspot[0]-1,wallspot[1]])
					returnlist.append([myspot[0]-1,myspot[1]])
				if not myspot[0]+1>=len(map):
					returnlist.append([wallspot[0]+1,wallspot[1]])
					returnlist.append([myspot[0]+1,myspot[1]])
				return returnlist
			return [spot for spot in nearestpurge(genmyspotlist(wallspot),map) if checkcontinuity(myspot,genmyspotlist,map,spot)]
		return [list(spot) for spot in list(fluffspots)]
	def nearestpurge(myspotlist,map,continuity=False,nope=False):
		origmyspotlist=tuple(myspotlist)
		listofbadspots=[]
		for i in range(0,8):
			if len(map) in myspotlist[i] or -1 in myspotlist[i] or (not continuity and map[myspotlist[i][0],myspotlist[i][1]]==-1):# or map[myspotlist[i][0],myspotlist[i][1]]>1:
				listofbadspots.append(myspotlist[i])
				#if continuity:
					#sys.exit(str(map[myspotlist[i][0],myspotlist[i][1]]))
		for i in listofbadspots:
			myspotlist.remove(i)
		if nope:
			for i in range(len(nope)):
				if nope[i] in myspotlist:
					myspotlist.remove(nope[i])
		for spot in myspotlist:
			if map[spot[0],spot[1]]>1:
				myspotlist.remove(spot)
		if len(myspotlist)==0:
			myspotlist=list(origmyspotlist)
			listofbadspots=[]
			for i in range(0,8):
				if len(map) in myspotlist[i] or -1 in myspotlist[i] or (not continuity and map[myspotlist[i][0],myspotlist[i][1]]==-1):# or map[myspotlist[i][0],myspotlist[i][1]]>1:
					listofbadspots.append(myspotlist[i])
			for i in listofbadspots:
				myspotlist.remove(i)
			lowestindex=min([map[spot[0],spot[1]] for spot in myspotlist])
			myspotlist=[spot for spot in myspotlist if map[spot[0],spot[1]]==lowestindex]
			if len(myspotlist)==0:
				oaoarairuguin
			return myspotlist
		return myspotlist
	def findbestdirection(startspot,genmyspotlist,closestzero,map,continuity=False,nope=False):
		myspotlist=nearestpurge(genmyspotlist(startspot),map,continuity,nope)
		distlist=[None]*len(myspotlist)
		for i in range(0,len(myspotlist)):
			distlist[i]=sqrt((closestzero[0]-myspotlist[i][0])**2+(closestzero[1]-myspotlist[i][1])**2)
		return tuple(myspotlist[distlist.index(min(distlist))])
	def checkcontinuity(start,genmyspotlist,map,end,returnfinalpoint=False,nope=False):
		if list(start)==list(end):
			if returnfinalpoint:
				return [False,start]
			return False
		bestdirection=findbestdirection(start,genmyspotlist,end,map,True,nope)
		origbestdirection=tuple(bestdirection)
		previousbest=origbestdirection
		count=0
		while map[bestdirection[0],bestdirection[1]]!=-1:
			bestdirection=findbestdirection(bestdirection,genmyspotlist,end,map,True,nope)
			if list(bestdirection)==list(end):
				if returnfinalpoint:
					return [True,bestdirection]
				return True
			if list(previousbest)==list(bestdirection) or list(start)==list(bestdirection):
				if returnfinalpoint:
					return [False,bestdirection]
				return False
			if list(origbestdirection)==bestdirection:
				zzzzzzzzzzzzzzz
			previousbest=tuple(bestdirection)
			count+=1
			if count>100:
				sys.exit('yeah this is just looping...gonna cut it off, heres the data: '+str([start,origbestdirection,bestdirection,end]))
		if returnfinalpoint:
			return [False,bestdirection]
		return False
	dview['checkcontinuity']=checkcontinuity
	dview['findbestdirection']=findbestdirection
	dview['nearestpurge']=nearestpurge
	dview['findwalledge']=findwalledge
	def nearestzero(myspot,map,nope,genmyspotlist):
		myspotlist=nearestpurge(genmyspotlist(myspot),map,nope=nope)
		x,y=numpy.where(map==0)
		zerospots=zip(x,y)
		if nope:
			for i in range(len(nope)):
				if nope[i] in zerospots:
					zerospots.remove(nope[i])
		if len(zerospots)==0:
			print 'could not find any zeros, will stay put'
			return myspot
		zerodists=[None]*len(zerospots)
		for i in range(0,len(zerospots)):
			zerodists[i]=sqrt((myspot[0]-zerospots[i][0])**2+(myspot[1]-zerospots[i][1])**2)
		closestzero=zerospots[zerodists.index(min(zerodists))]
		bestdirection=findbestdirection(myspot,genmyspotlist,closestzero,map,nope=nope)
		state,bestdirection2=checkcontinuity(bestdirection,genmyspotlist,map,closestzero,True,nope=nope)
		if state:
			return bestdirection
		fluffspots=findwalledge(myspot,bestdirection2,genmyspotlist,map,nope=nope)
		possiblebestspots=[]
		for spot in fluffspots:
			if checkcontinuity(closestzero,genmyspotlist,map,spot,nope=nope):
				possiblebestspots.append(spot)
		if len(possiblebestspots)==0:
			distlist=[]
			for spot in fluffspots:
				distlist.append(sqrt((spot[0]-myspot[0])**2+(spot[1]-myspot[1])**2))
			return findbestdirection(myspot,genmyspotlist,fluffspots[distlist.index(max(distlist))],map,nope=nope)
		distlist=[]
		for spot in possiblebestspots:
			distlist.append(sqrt((spot[0]-myspot[0])**2+(spot[1]-myspot[1])**2)+sqrt((spot[0]-closestzero[0])**2+(spot[1]-closestzero[1])**2))
		return findbestdirection(myspot,genmyspotlist,possiblebestspots[distlist.index(min(distlist))],map,nope=nope)
	dview['nearestzero']=nearestzero
	dims=(size,size)
	background=numpy.zeros(dims)
	boxsize=7
	screen=pygame.display.set_mode((dims[0]*boxsize,dims[1]*boxsize+20))
	Tkinter.Tk().withdraw()
	rectlist=numpy.zeros(dims,dtype=object)
	for i in xrange(dims[0]):
		for j in xrange(dims[1]):
			rectlist[i,j]=pygame.draw.rect(screen,(0,0,0),(i*boxsize,j*boxsize,boxsize,boxsize),0)
	pause=pygame.draw.rect(screen,(255,0,0),(0,dims[1]*boxsize,dims[0]*boxsize,20),0)
	back=pygame.draw.rect(screen,(255,0,0),(0,dims[1]*boxsize,20,20),0)
	forward=pygame.draw.rect(screen,(255,0,0),(20,dims[1]*boxsize,20,20),0)
	font=pygame.font.SysFont('Ariel',20)
	dfont=pygame.font.SysFont('Ariel',11)
	#background[4,0]=2
	spots=[None]*numworkers
	mostrecentoldspots=[]*numworkers
	def randcolor():
		val=lambda: numpy.random.randint(150,255)
		return (val(),val(),numpy.random.randint(0,150))
	def updatemap():
		for spot in mostrecentoldspots:
			screen.fill(randcolor(),rectlist[spot[0],spot[1]])
		for spot in spots:
			background[spot[0],spot[1]]=background[spot[0],spot[1]]+1
			screen.fill((0,0,255),rectlist[spot[0],spot[1]])
			screen.blit(dfont.render(' '+str(spots.index(spot)),1,(0,0,0)),rectlist[spot[0],spot[1]])
		pygame.display.update()
	def paused(done=False):
		screen.fill((0,255,0),pause)
		screen.fill((0,200,50),back)
		screen.fill((0,200,50),forward)
		screen.blit(font.render(' <',1,(0,0,0)),back)
		screen.blit(font.render(' >',1,(0,0,0)),forward)
		if done:
			screen.blit(font.render('           exit',1,(0,0,0)),pause)
		else:
			screen.blit(font.render('           continue',1,(0,0,0)),pause)
		pygame.display.update([pause,back,forward])
		proceed=0
		depth=1
		while proceed==0:
			event2=pygame.event.wait()
			if event2.type==pygame.MOUSEBUTTONDOWN:
				x2,y2=event2.pos
				if back.collidepoint(x2,y2):
					if depth>len(oldspots)-1:
						continue
					print 'go back here'
					for spot in oldspots[-depth]:
						screen.fill((0,0,0),rectlist[spot[0],spot[1]])
					depth=depth+1
					for spot in oldspots[-depth]:
						screen.fill((0,0,255),rectlist[spot[0],spot[1]])
						screen.blit(dfont.render(' '+str(oldspots[-depth].index(spot)),1,(0,0,0)),rectlist[spot[0],spot[1]])
					pygame.display.update()
				elif forward.collidepoint(x2,y2):
					if depth<2:
						continue
					print 'go forward here'
					for spot in oldspots[-depth]:
						screen.fill(randcolor(),rectlist[spot[0],spot[1]])
					depth=depth-1
					for spot in oldspots[-depth]:
						screen.fill((0,0,255),rectlist[spot[0],spot[1]])
						screen.blit(dfont.render(' '+str(oldspots[-depth].index(spot)),1,(0,0,0)),rectlist[spot[0],spot[1]])
					pygame.display.update()
				elif pause.collidepoint(x2,y2):
					if done:
						sys.exit("exiting")
					screen.fill((255,0,0),pause)
					screen.blit(font.render(' pause',1,(0,0,0)),pause)
					screen.fill((255,0,0),back)
					screen.fill((255,0,0),forward)
					for i in xrange(depth-1):
						for spot in oldspots[-depth+i]:
							screen.fill(randcolor(),rectlist[spot[0],spot[1]])
						for spot in oldspots[-depth+i+1]:
							screen.fill((0,0,255),rectlist[spot[0],spot[1]])
						time.sleep(.03)
						pygame.display.update()
					for spot in oldspots[-1]:
						screen.fill((0,0,255),rectlist[spot[0],spot[1]])
						screen.blit(dfont.render(' '+str(oldspots[-1].index(spot)),1,(0,0,0)),rectlist[spot[0],spot[1]])
					pygame.display.update()
					proceed=1
			if event2.type==pygame.QUIT:
				sys.exit("exiting")
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
			if len(map) in myspotlist[i] or -1 in myspotlist[i] or map[myspotlist[i][0],myspotlist[i][1]]!=0:
				listofbadspots.append(myspotlist[i])
		for i in listofbadspots:
			myspotlist.remove(i)
		return myspotlist
	dview["purgelist"]=purgelist
	def edgeseek(center,myspot,map,nope,genmyspotlist,counterpoints=False):
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
			if all([not map[testspot[0],testspot[1]]==0 for testspot in genmyspotlist(myspot)]):
				return [nearestzero(myspot,map,counterpoints,genmyspotlist),0]
			else:
				if counterpoints:
					return [nearestzero(myspot,map,locklist+counterpoints,genmyspotlist),0]
				else:
					return [nearestzero(myspot,map,locklist,genmyspotlist),0]
		#if len(myspotlist)==1:
		#	return list(tuple(myspotlist[0]),1)
		distlist=[None]*len(myspotlist)
		for i in range(len(distlist)):
			distlist[i]=sqrt((center[0]-myspotlist[i][0])**2+(center[1]-myspotlist[i][1])**2)
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
			if len(map) in myspotlist[i] or -1 in myspotlist[i] or map[myspotlist[i][0],myspotlist[i][1]]!=0:
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
			distlist[i]=sqrt((center[0]-myspotlist[i][0])**2+(center[1]-myspotlist[i][1])**2)
		return tuple(myspotlist[distlist.index(min(distlist))])
	#only difference between the 2 algorithms is min v max in the last line
	dview["centerseek"]=centerseek

	#initialize map w/ clustered drones
	midspot=tuple([size/2,size/2])
	midspots=genmyspotlist(midspot)
	midspotseven=[(midspot[0]-1,midspot[1]-1),(midspot[0],midspot[1]-1),(midspot[0]-1,midspot[1]),midspot]
	if numworkers<=8:
		if numworkers<=4 and size%2==0:
			spots=midspotseven[:numworkers]
			#midspot=(size/2)*2
			
		else:
			spots=midspots[:numworkers]
			background[midspot[0],midspot[1]]=1 #saying center of release is known
			screen.fill(randcolor(),rectlist[midspot[0],midspot[1]])
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
	screen.blit(font.render(' click here to proceed',1,(0,0,0)),pause)
	pygame.display.update(pause)
	pygame.display.set_caption("click to make wall")
	wall=0
	while True:
		event=pygame.event.wait()
		if event.type==pygame.QUIT:
			sys.exit("exiting")
		elif event.type==pygame.MOUSEBUTTONDOWN:
			x,y=event.pos
			if pause.collidepoint(x,y):
				screen.fill((255,0,0),pause)
				screen.blit(font.render(' pause',1,(0,0,0)),pause)
				pygame.display.update(pause)
				break
			else:
				thisrect=rectlist[x/boxsize,y/boxsize]
				if background[x/boxsize,y/boxsize]==0:
					screen.fill((255,255,255),thisrect)
					pygame.display.update(thisrect)
					background[x/boxsize,y/boxsize]=-1
					wall=wall+1
				else:
					screen.fill((0,0,0),thisrect)
					pygame.display.update(thisrect)
					background[x/boxsize,y/boxsize]=0
					wall=wall-1
		
	print 'starting the search'
	print 'iteration '+str(iteration)
	print background
	center=[None,None]
	pygame.display.set_caption("starting")
	while 0 in background:
		dview=c[:]
		mostrecentoldspots=list(spots)
		if iteration==1:
			print 'starting at '+str(spots)
		#else:
		#	print str(oldspots[iteration-2])+' >>> '+str(spots)
		center[0]=sum([x for x,y in spots])/float(len(spots))
		center[1]=sum([y for x,y in spots])/float(len(spots))
		starttime=time.time()
		dview.scatter('myspot',spots)
		dview['center']=center
		if algorithm=='centerseek':
			dview['center']=midspot
		dview['map']=background
		dview.execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,False,genmyspotlist)')
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
				c[i].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist,genmyspotlist)')
				intermid=c[i]['newspot']
				if intermid in spots:
					print "possible meta problem with "+str(c.ids[spots.index(intermid)])
					spots[c.ids.index(i)]=intermid
					c[c.ids[spots.index(intermid)]].execute("locklist.append(newspot)")
					c[c.ids[spots.index(intermid)]].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist,genmyspotlist)')
					spots[spots.index(intermid)]=c[c.ids[spots.index(intermid)]]["newspot"]
				#if spots[i]==oldspots[iteration-1][i]:
				#	crashtest=crashtest+1
					#print str(i)+"/"+str(intermid)+" got here, with other locklist "+str(c[c.ids[spots.index(intermid)]]["mylocks"])
					if intermid in spots:
						#print locklist
						#c[i].execute("locklist=[newspot,]")
						c[i]["locklist"]=[intermid,]
						c[i]['counterpoints']=spots
						print "possible contradiction problem here with "+str(i)+' and '+str(c.ids[spots.index(intermid)])
						#print c[i]["locklist"]
						#seems to be a problem with the next line and locking. setting locklist to locklist for now
						#if theres a problem with prediction check call to nearestzero
						c[i].execute('[newspot,mylocks]='+algorithm+'(center,myspot,map,locklist,genmyspotlist,counterpoints)')
						c[i]['counterpoints']=False
						intermid=c[i]['newspot']
						#print intermid
						#print "possible contradiction problem here with "+str(i)+' and '+str(spots.index(intermid))
						spots[c.ids.index(i)]=intermid
				else:
					spots[c.ids.index(i)]=intermid
		updatemap()
		oldspots.append(tuple(spots))
		iteration=iteration+1
		if clearprompt=='y':
			os.system('clear')
		percentdone=str(float((background>0).sum())/(size**2-wall)*100)+'%'
		print 'iteration '+str(iteration)
		print background
		print 'percent done: '+percentdone
		banner=percentdone
		if alert:
			banner=banner+' done, imperfect'
		else:
			banner=banner+' done, perfect'
		pygame.display.set_caption(banner) 
		print str(oldspots[iteration-2])+' >>> '+str(spots)
		if (background>1).sum()>0 and alert==0:
			#pygame.display.set_caption("
			#if wall==0:
				#if raw_input("imperfect search. continue? y/n ")=='n':
				#	sys.exit("exiting")
			if tkMessageBox.askyesno("imperfect search","Some element of this search is suboptimal. Pause?"):
				paused()
			alert=1
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				sys.exit("exiting")
			if event.type==pygame.MOUSEBUTTONDOWN:
				x,y=event.pos
				if pause.collidepoint(x,y):
					paused()
				#else:
				#	screen.fill((0,255,0),rectlist[x/boxsize,y/boxsize])

	#once done, print the final report
	print 'final report: '
	print "moves wasted: (doesn't account for necessary moves) "+str(-size**2+numworkers*iteration+1+wall)
	print 'workers: '+str(numworkers)
	print 'number of squares: '+str(size**2)
	print 'size of wall: '+str(wall)
	print 'extra iterations: '+str(iteration-ceil((size**2-wall)/numworkers))
	print 'percent error in terms of iterations: '+str((iteration-ceil((size**2-wall)/numworkers))/iteration*100)+'%'
	if alert==1:
		print "imperfect"
	else:
		print "perfect"
	paused(done=True)
