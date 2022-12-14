import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# terminal input 
network_argv = ["--model=models/security/ssd-mobilenet.onnx",
"--labels=models/security/labels.txt",
"--input-blob=input_0",
"--output-cvg=scores","--output-bbox=boxes","/dev/video0"]

# create video output object 
output = jetson.utils.videoOutput(opt.output_URI, argv=network_argv+is_headless)
# output = jetson.utils.videoOutput()
	
# load the object detection network
net = jetson.inference.detectNet(opt.network, network_argv, opt.threshold)
# net = jetson.inference.detectNet("ssd-mobilenet", threshold=0.5)

# create video sources
input = jetson.utils.videoSource(opt.input_URI, network_argv)
# input = jetson.utils.videoSource("/dev/video0")


# process frames until the user exits
while True:
	# capture the next image
	img = input.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img, overlay=opt.overlay)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
		print(detection)
		class_name = net.GetClassDesc(detection.ClassID)  # add line to show object ID and warning
		print(f"Detected '{class_name}'")
		if (class_name == 'knife'):
			print(f"ALERT: weapon detected!")

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

	# print out performance info
	net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break

