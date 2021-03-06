#
from itertools import cycle

__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '10/31/2019 5:50 PM'

import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier

if __name__ == "__main__":
	iris = datasets.load_iris()
	X = iris.data
	y = iris.target

	# Binarize the output
	y = label_binarize(y, classes=[0, 1, 2])
	n_classes = y.shape[1]

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)

	classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,
											 random_state=0))
	y_score = classifier.fit(X_train, y_train).decision_function(X_test)
	print(y_score[:2])

	print("----------------")

	print(y_test[:2])
	print("----------------")

	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(n_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])
	colors = cycle(['blue', 'red', 'green'])
	for i, color in zip(range(n_classes), colors):
		plt.plot(fpr[i], tpr[i], color=color, lw=1,
				 label='ROC curve of class {0} (area = {1:0.2f})'
					   ''.format(i, roc_auc[i]))
	plt.plot([0, 1], [0, 1], 'k--', lw=1)
	plt.xlim([-0.05, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic for multi-class data')
	plt.legend(loc="lower right")
	plt.show()
