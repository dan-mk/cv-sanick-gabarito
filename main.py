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


def loadLabels(videoId):
	global currentLabelId

	labelsPath = '%s/labels' % videoId
	labelFilenames = os.listdir(labelsPath)

	labels = [[] for _ in range(len(frames))]
	for labelFilename in labelFilenames:
		labelPath = '%s/%s' % (labelsPath, labelFilename)

		currentLabelId = max(currentLabelId, int(labelFilename) + 1)

		with open(labelPath, 'r+') as labelFile:
			for line in labelFile:
				frameId, x, y = map(int, line.split())
				labels[frameId // 6].append((x, y, int(labelFilename)))

	return labels


def joinLabels(labels1, labels2):
	labelsR = []
	for i in range(len(frames)):
		labelsR.append(labels1[i] + labels2[i])
	return labelsR


def updateView():
	global currentFrameIndex
	global mode

	frame = frames[currentFrameIndex]

	labelsInFrame = joinLabels(labels, tmpLabels)[currentFrameIndex]

	frameShow = frame.copy()
	for x, y, labelId in labelsInFrame:
		frameShow = cv2.circle(frameShow, (x, y), 6, (labelId * 20, labelId * 20, labelId * 20), 8)

	cv2.imshow('Gabarito do desafio de visao computacional Sanick', frameShow)


def onMouse(event, x, y, flags, param):
	global currentFrameIndex
	global mode
	global tmpLabels
	global currentLabelId

	if event == cv2.EVENT_LBUTTONDOWN and mode == 'adding':
		tmpLabels[currentFrameIndex] = [(x, y, currentLabelId)]

	updateView()


def saveLabel(videoId, currentLabelId):
	labelsPath = '%s/labels' % videoId
	labelFilenames = os.listdir(labelsPath)

	newLabelFile = open('%s/%d' % (labelsPath, currentLabelId), 'w+')
	for frameIndex, labelsInFrame in enumerate(tmpLabels):
		if len(labelsInFrame) == 0:
			continue
		x, y, labelId = labelsInFrame[0]
		frameId = frameIndex * 6
		newLabelFile.write('%d %d %d\n' % (frameId, x, y))
	newLabelFile.close()


videoId = sys.argv[1]

currentLabelId = 1

frames = loadFrames(videoId)
labels = loadLabels(videoId)

currentFrameIndex = 0
mode = 'normal'
tmpLabels = [[] for _ in range(len(frames))]

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

	if key == ord('x'):
		currentFrameIndex = min(len(frames) - 1, currentFrameIndex + 1)

	if key == ord('a') and mode != 'adding':
		mode = 'adding'

	if key == ord('s') and mode == 'adding':
		labels = joinLabels(labels, tmpLabels)

		saveLabel(videoId, currentLabelId)
		currentLabelId += 1

		tmpLabels = [[] for _ in range(len(frames))]
		mode = 'normal'

	if key == ord('c') and mode == 'adding':
		tmpLabels = [[] for _ in range(len(frames))]
		mode = 'normal'

	updateView()
