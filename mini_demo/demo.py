# Demo for Demon Hacks 2019 (DePaul University)

from absl import flags
from absl import logging
from absl import app

import numpy as np
import time
import os

# Using matplotlib for images
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image

from sklearn.linear_model import LogisticRegression
from sklearn import ensemble
from sklearn import tree
from sklearn import svm

# Using OpenCV
# import cv2

FLAGS = flags.FLAGS

flags.DEFINE_string('CAM_ID', '', '1 - 9')
flags.DEFINE_integer('method', 0, 'Machine Learning Method')
flags.DEFINE_float('pause', 0.01, 'Pause time for the demo')
flags.DEFINE_integer('w_patch', 25, 'Patch width size')
flags.DEFINE_integer('h_patch', 25, 'Patch height size')

flags.DEFINE_string('DIR', 'data/FULL_IMAGE_1000x750', 'Directory')
flags.DEFINE_string('WEATHER', 'SUNNY', 'SUNNY, OVERCAST, RAINY')
flags.DEFINE_string('W_ID', 'S', 'S, O, R')

nRows_old = 2592
nCols_old = 1944
nRows_new = 1000
nCols_new = 750
nRows_factor = nRows_new / nRows_old
nCols_factor = nCols_new / nCols_old

def load_positions(file_fn):
	file = open(file_fn, "r")
	count_line = 0
	result = []
	for line in file:
		count_line += 1
		if count_line > 1:
			info = [int(x) for x in line.strip().split(',')]
			X = int(info[1] * nRows_factor)
			Y = int(info[2] * nCols_factor)
			W = int(info[3] * nRows_factor)
			H = int(info[4] * nCols_factor)
			result.append([info[0], X, Y, W, H])

	file.close()
	return result

def load_train_data(file_fn, W_ID):
	file = open(file_fn, "r")
	result = []
	for line in file:
		example = line.strip().split(' ')
		if example[0][0] == W_ID:
			result.append(["data/PATCHES/" + example[0], example[1]])
	file.close()
	return result

def rgb2gray(rgb):
	return np.dot(rgb[:, :, :], [0.2989, 0.5870, 0.1140])

def process_data(data, w_patch, h_patch):
	X = []
	y = []
	for example in range(len(data)):
		img = Image.open(data[example][0])
		img = img.resize((w_patch, h_patch))
		a = np.asarray(img)
		X.append(rgb2gray(a).reshape(w_patch * h_patch))
		y.append(int(data[example][1]))

		# plt.imshow(img)
		# plt.show()
	X = np.asarray(X)
	y = np.asarray(y)
	return (X, y)

def train_process(train_data, method):
	X = train_data[0] / 256.0
	y = train_data[1]

	assert method >= 0
	assert method < 4

	# Logistic regression
	if method == 0:
		clf = LogisticRegression(random_state = 0,  solver = 'lbfgs', multi_class = 'multinomial')

	# Decision tree
	if method == 1:
		clf = tree.DecisionTreeClassifier()

	# Gradient boosting
	if method == 2:
		params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 2, 'learning_rate': 0.01, 'loss': 'ls'}
		clf = ensemble.GradientBoostingRegressor(**params)
	
	# Support vector machine
	if method == 3:
		clf = svm.SVC(gamma = 'scale')

	# Fit
	clf.fit(X, y)

	print("Done fitting")
	return clf

def main(argv):
	DIR = FLAGS.DIR
	WEATHER = FLAGS.WEATHER
	CAM_ID = FLAGS.CAM_ID
	W_ID = FLAGS.W_ID
	pause = FLAGS.pause
	w_patch = FLAGS.w_patch
	h_patch = FLAGS.h_patch
	method = FLAGS.method

	train_data = load_train_data("data/LABELS/camera" + CAM_ID + ".txt", W_ID)
	train_data = process_data(train_data, w_patch, h_patch)
	clf = train_process(train_data, method)

	slots = load_positions("data/camera" + CAM_ID + ".csv")

	dates = [element for element in next(os.walk(DIR + "/" + WEATHER))[1]]
	dates.sort()

	for CAPTURE_DATE in dates:
		image_names = [element[2] for element in os.walk(DIR + "/" + WEATHER + "/" + CAPTURE_DATE + "/camera" + CAM_ID)]
		image_names = image_names[0]
		image_names.sort()

		for image_name in image_names:
			image_fn = DIR + "/" + WEATHER + "/" + CAPTURE_DATE + "/camera" + CAM_ID + "/" + image_name
			# print('Image file:', image_fn)

			# Using matplotlib for images
			img = Image.open(image_fn)
			img = np.copy(np.asarray(img))

			for slot in slots:
				x1 = slot[1]
				y1 = slot[2]
				w = slot[3]
				h = slot[4]
				x2 = x1 + w
				y2 = y1 + h

				x = Image.fromarray(img[y1:y2, x1:x2, :])
				x = x.resize((w_patch, h_patch))
				x = np.asarray(x)
				x = rgb2gray(x).reshape(w_patch * h_patch)
				predict = clf.predict([x])[0]

				if predict == 0:
					img[y1:y2, x1, :] = 255
					img[y1:y2, x2, :] = 255
					img[y1, x1:x2, :] = 255
					img[y2, x1:x2, :] = 255
				else:
					img[y1:y2, x1, :] = 0
					img[y1:y2, x2, :] = 0
					img[y1, x1:x2, :] = 0
					img[y2, x1:x2, :] = 0

					img[y1:y2, x1, 0] = 255
					img[y1:y2, x2, 0] = 255
					img[y1, x1:x2, 0] = 255
					img[y2, x1:x2, 0] = 255

			plt.imshow(img)
			plt.pause(pause)
	plt.show()

	# Using OpenCV
	# img = cv2.imread(image_fn)
	# cv2.imshow('image', img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

if __name__ == '__main__':
	app.run(main)