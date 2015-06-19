from setuptools import setup

def readme():
	with open("README.txt") as f:
		return f.read()

setup(name="distdrone",
	version="1.37",
	description="package to drive parallel drone swarm",
	url="https://github.com/isaacrob/distdrone",
	author="Isaac Robinson",
	author_email="isaacrob@me.com",
	license="MIT",
	packages=["distdrone","distdrone.motion","distdrone.imgproc"],
	scripts=["bin/trigger","bin/testpredictor","bin/centersearch","bin/installdronedeps"],
	keywords=['drone','OpenCV','IPython','parallel'],
	zip_safe=False)