import cv2
import numpy as np
import os

from KNN import knn
from Attendence import markattendence

# Init Camera
cap = cv2.VideoCapture(0)

# Face Detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip = 0
dataset_path = './data/'

face_data = []
labels = []

class_id = 0  # Labels for the given file
names = {}  # Mapping btw id - name

# Data Preparation
for fx in os.listdir(dataset_path):
	if fx.endswith('.npy'):

		# Create a mapping btw class_id and name
		names[class_id] = fx[:-4]

		data_item = np.load(dataset_path + fx)
		face_data.append(data_item)

		# Create Labels for the class
		target = class_id * np.ones((data_item.shape[0],))
		class_id += 1
		labels.append(target)

face_dataset = np.concatenate(face_data, axis=0)
face_labels = np.concatenate(labels, axis=0).reshape((-1, 1))

print(face_dataset.shape)
print(face_labels.shape)


trainset = np.concatenate((face_dataset, face_labels), axis=1)
print(trainset.shape)

while True:
	ret, frame = cap.read()
	if ret is False:
		continue

	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	if len(faces) == 0:
		continue

	for face in faces:
		x, y, w, h = face

#Get the face ROI
		offset = 10
		face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
		face_section = cv2.resize(face_section, (100, 100))

#Predicted Label (out)
		output = knn(trainset, face_section.flatten())

#Display on the screen the name and rectangle around it
		pred_name = names[int(output)]
		markattendence(pred_name)
		cv2.putText(frame, pred_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.imshow("Faces", frame)

	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
