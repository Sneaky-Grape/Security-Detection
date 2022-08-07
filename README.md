# Security-Detection

Hello! This project is a program which uses Artificial Intelligence and a camera to detect different types of objects and classifies if they are either dangerous or safe!

Overview
In many public places, safety is a priority. Many areas like airports or important events require a team of professionals as well as many advanced technology to dig through your personal belongings to check for anything dangerous. With this program, sorting through items will never be simpler. 

How it Works
I had went over the long process of training my own detectnet network called ssd-mobilenet. I trained the program by taking and adjusting around 600 pictures with the objects in different positions and directions. Then I made a python code to incorporate the network so all the user needs to do is to download the python code and run it in jetson inference. In the python code, I added my own code to alert the user that it detects something dangerous. After running the program in the jetson nano, the camera is opened and detectnet starts. Detectnet would be able to "detect" the many different objects and if that object is a weapon(such as a knife) and it will alert the person of the threat. 

Materials
All you need is a webcam and a jetson nano kit, consisting of a power supply, HDMI cable, wifi dongle, mouse, and keyboard.
