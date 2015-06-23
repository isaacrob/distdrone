This is much of the backbone for my, Isaac Robinson's, high school science project.
Although it may not seem like it, almost a year of work has gone into this.
The idea is that a drone swarm where the drones work together to process difficult tasts, 
such as image processing, will be much more efficient, especially if that task has 
a certain threshold beyond which it becomes relevant. Here, that task is facial detection
and soon-to-be facial recognition. 
I have also designed several search algorithms with which a drone swarm may search an area.
This package uses OpenCV and IPython to do its image processing and parallel computing,
respectively.
As this package is still in its basic development phases, I am not going to go into much 
detail here. If you have questions, email me at isaacrob@me.com.
This does not currently support other people, ie it is tailored to the way I've set things
up on my various computers.
After installation, running installdronedeps will install opencv, scipy, and numpy, along
with all their various dependencies, on a Raspberry Pi running Raspbian. Modifying the 
directory changes should make it install on any Ubuntu-based platform.
Running trigger will start a simple motion detector and face finder using opencv and any
attached camera in parallel across an ippython cluster with some specified name passed
as a command line argument and interpreted with click.
Running testpredictor will try to generate an opencv face recognizer, trying to best center
and align any faces in the images taken on cue by the camera.
Various other command line accessable scripts will be installed.
The distdrone module has several parts, notably the image processing portion, run with opencv,
the different motion algorithms, including a search algorithm on a simulated map run with
ipython which will perfectly search certain spaces with multiple simulated drones exploring
it at once without ever exploring the same portion of the simulated space twice. All of the
litte algorithms that make this, along with other things, possible are defined in gears.
There are other things provided by this package. Email me if you would care to know what 
they are, and I will provide a write up for all of them.

-------------------------------------------------------------------------------------------

note to self: after installation (both of package and dronedeps), add ip of new pi to cluster config and restart cluster, then run trigger. will upload exact configuration files soon
