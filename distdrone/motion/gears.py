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

