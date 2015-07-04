from setuptools import setup
from subprocess import call
import os, socket, sys
from distutils.command.install import install as _install

def _post_install(dir):
	global call
	call(['pip','install','-e','.'])
	try:
		os.chdir('/home/pi/.ipython')
	except:
		os.mkdir('/home/pi/.ipython')
		call(['chown','pi','/home/pi/.ipython'])
		call(['chmod','777','/home/pi/.ipython'])
		os.chdir('/home/pi/.ipython')
	call(['rm','-rf','profile_picluster'])
	call(['sudo','-u','pi','git','clone','https://github.com/isaacrob/picluster','profile_picluster'])
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(('8.8.8.8',80))
	myip=s.getsockname()[0]
	os.chdir('profile_picluster')
	call(['sudo','-u','pi','python','writeremotehosts.py','--controller_ip='+myip])

class install(_install):
	def run(self):
		_install.run(self)
		self.execute(_post_install, (self.install_lib,),msg='running post install')

def readme():
	with open("README.txt") as f:
		return f.read()

setup(name="distdrone",
	cmdclass={'install':install},
	version="1.43",
	description="package to drive parallel drone swarm",
	url="https://github.com/isaacrob/distdrone",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="GNU",
	packages=["distdrone","distdrone.motion","distdrone.imgproc"],
	scripts=["bin/trigger","bin/testpredictor","bin/centersearch","bin/installdronedeps"],
	keywords=['drone','OpenCV','IPython','parallel'],
	install_requires=['ipython==2.1','psutil>=3','paramiko>=1.15','click>=4','pyzmq>=14'],
	zip_safe=False)
