import jetson.inference
import jetson.utils

import argparse
import sys

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("high.mp4")
output = jetson.utils.videoOutput("display://0")

# process frames until the user exits
while True:
	# capture the next image
	img = camera.Capture()

	# detect objects in the image (with overlay)
	detections = net.Detect(img)

	# print the detections
	print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
		print(detection)

	# render the image
	output.Render(img)

	# update the title bar
	output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

	# print out performance info
	net.PrintProfilerTimes()

	# exit on input/output EOS
	if not input.IsStreaming() or not output.IsStreaming():
		break