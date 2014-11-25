from setuptools import setup

def readme():
	with open("README.txt") as f:
		return f.read()

setup(name="distdrone",
	version="1.23",
	description="package to drive parallel drone swarm",
	url="http://github.com/isaacrob/paradrone",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="MIT",
	packages=["distdrone","distdrone.motion","distdrone.imgproc"],
	scripts=["bin/trigger","bin/testpredictor","bin/centersearch","bin/installdronedeps"],
	zip_safe=False)