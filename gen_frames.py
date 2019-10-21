import numpy as np
import cv2
import sys

video_path = sys.argv[1]
dest_folder_path = sys.argv[2]

if dest_folder_path[-1] != '/':
	dest_folder_path += '/'

frame_index = 0
cap = cv2.VideoCapture(video_path)
while cap.isOpened():
	ret, colored_frame = cap.read()

	if not np.any(colored_frame):
		# Final do vídeo
		cap.release()
		continue

	if frame_index % 6 == 0:
		cv2.imwrite('%s%d.jpg' % (dest_folder_path, frame_index), colored_frame)

	frame_index += 1

'''
python3 gen_frames.py soja-treinamento/sojaTreinamento.mp4 soja-treinamento/frames
python3 gen_frames.py soja-teste/sojaTeste.mp4 soja-teste/frames

python3 gen_frames.py capsula-marrom-treinamento/capsulaMarromTreinamento.mp4 capsula-marrom-treinamento/frames
python3 gen_frames.py capsula-marrom-teste/capsulaMarromTeste.mp4 capsula-marrom-teste/frames

python3 gen_frames.py capsula-rosa-treinamento/capsulaRosaTreinamento.mp4 capsula-rosa-treinamento/frames
python3 gen_frames.py capsula-rosa-teste/capsulaRosaTeste.mp4 capsula-rosa-teste/frames
'''