from setuptools import setup

def readme():
	with open("README.txt") as f:
		return f.read()

setup(name="distdrone",
	version="1.41",
	description="package to drive parallel drone swarm",
	url="https://github.com/isaacrob/distdrone",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="GNU",
	packages=["distdrone","distdrone.motion","distdrone.imgproc"],
	scripts=["bin/trigger","bin/testpredictor","bin/centersearch","bin/installdronedeps"],
	keywords=['drone','OpenCV','IPython','parallel'],
	install_requires=['ipython==2.1','psutil>=3','paramiko>=1.15'],
	zip_safe=False)

#build picluster now
from subprocess import call
import os, socket

#call(['sudo','tcpdump','-Z','pi'])
os.chdir('/home/pi/.ipython')
call(['rm','-rf','profile_picluster'])
call(['sudo','-u','pi','git','clone','https://github.com/isaacrob/picluster','profile_picluster'])
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
myip=s.getsockname()[0]
os.chdir('profile_picluster')
call(['sudo','-u','pi','python','writeremotehosts.py','--controller_ip='+myip])
