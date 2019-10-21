import sys
import os
import cv2
import numpy as np

def loadFrames(videoId):
	framesPath = '%s/frames' % videoId
	frameFilenames = os.listdir(framesPath)

	frames = [[] for _ in range(len(frameFilenames))]
	for frameFilename in frameFilenames:
		framePath = '%s/%s' % (framesPath, frameFilename)
		frameId = int(frameFilename.split('.')[0])

		frame = cv2.imread(framePath)
		h, w, c = frame.shape
		frame = cv2.resize(frame, (w // 2, h // 2), interpolation = cv2.INTER_AREA)

		frames[frameId // 6] = frame

	return frames


def loadLabels(videoId, lenFrames):
	labelsPath = '%s/labels' % videoId
	labelFilenames = os.listdir(labelsPath)

	labels = [[] for _ in range(lenFrames)]
	for labelFilename in labelFilenames:
		labelPath = '%s/%s' % (labelsPath, labelFilename)

		with open(labelPath, 'r+') as labelFile:
			for line in labelFile:
				frameId, x, y = map(int, line.split())
				labels[frameId // 6].append((x, y, (0, 0, 255)))

	return labels


def updateView():
	global currentFrameIndex
	global mode

	frame = frames[currentFrameIndex]

	if mode == 'adding':
		labelsInFrame = tmpLabels[currentFrameIndex]
	else:
		labelsInFrame = labels[currentFrameIndex]

	frameShow = frame.copy()
	for x, y, bgr in labelsInFrame:
		frameShow = cv2.circle(frameShow, (x, y), 6, bgr, 8)

	cv2.imshow('Gabarito do desafio de visao computacional Sanick', frameShow)


def onMouse(event, x, y, flags, param):
	global currentFrameIndex
	global mode
	global tmpLabels

	if event == cv2.EVENT_LBUTTONDOWN and mode == 'adding':
		tmpLabels[currentFrameIndex].append((x, y, (0, 0, 255)))

	updateView()


videoId = sys.argv[1]

frames = loadFrames(videoId)
labels = loadLabels(videoId, len(frames))

currentFrameIndex = 0
mode = 'normal'
tmpLabels = labels.copy()

cv2.namedWindow('Gabarito do desafio de visao computacional Sanick')
updateView()
cv2.setMouseCallback('Gabarito do desafio de visao computacional Sanick', onMouse)

while True:
	key = cv2.waitKey(0) & 0xFF

	if key == ord('q'):
		cv2.destroyAllWindows()
		break

	if key == ord('z'):
		currentFrameIndex = max(0, currentFrameIndex - 1)
		updateView()

	if key == ord('x'):
		currentFrameIndex = min(len(frames) - 1, currentFrameIndex + 1)
		updateView()

	if key == ord('a') and mode != 'adding':
		tmpLabels = labels.copy()

		mode = 'adding'

	if key == ord('s') and mode == 'adding':
		labels = tmpLabels.copy()

		mode = 'normal'

	if key == ord('c') and mode == 'adding':
		mode = 'normal'
