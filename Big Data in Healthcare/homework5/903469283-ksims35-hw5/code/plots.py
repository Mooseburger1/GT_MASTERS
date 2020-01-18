import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

# TODO: You can use other packages if you want, e.g., Numpy, Scikit-learn, etc.


def plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies):
	# TODO: Make plots for loss curves and accuracy curves.
	# TODO: You do not have to return the plots.
	# TODO: You can save plots as files by codes here or an interactive way according to your preference.
	plt.subplots(nrows=2, ncols = 2, figsize=(20,20))

	plt.subplot(221)
	plt.plot(range(len(train_losses)), train_losses, marker = '*', label = 'Train Loss')
	plt.legend()
	plt.xlabel('Epoch')
	plt.ylabel('Train Loss')

	plt.subplot(222)
	plt.plot(range(len(valid_losses)), valid_losses, marker = '*', label = 'Valid Loss')
	plt.legend()
	plt.xlabel('Epoch')
	plt.ylabel('Valid Loss')

	plt.subplot(223)
	plt.plot(range(len(train_accuracies)), train_accuracies, marker = '*', label = 'Train Accuracy', color = 'orange')
	plt.legend()
	plt.xlabel('Epoch')
	plt.ylabel('Train Accuracy')

	plt.subplot(224)
	plt.plot(range(len(valid_accuracies)), valid_accuracies, marker = '*', label = 'Valid Accuracy', color = 'orange')
	plt.xlabel('Epoch')
	plt.ylabel('Valid Accuracy')
	plt.legend()
	plt.savefig("Train_Summary.png", bbox_inches='tight')
	plt.show()


def plot_confusion_matrix(results, class_names):
	# TODO: Make a confusion matrix plot.
	# TODO: You do not have to return the plots.
	# TODO: You can save plots as files by codes here or an interactive way according to your preference.
	y_true  = [x[0] for x in results]
	y_pred = [x[1] for x in results]

	conf_matrix = confusion_matrix(y_true, y_pred)
	
	normalize = True
	if normalize:
		conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
	#Code for confusion matrix heatmap sourced from
	#https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
	fig, ax = plt.subplots(figsize=(20,20))
	im = ax.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
	ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
	ax.set(xticks=np.arange(conf_matrix.shape[1]),
           yticks=np.arange(conf_matrix.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=class_names, yticklabels=class_names,
           title='Confusion Matix',
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

	fmt = '.2f' if normalize else 'd'
	thresh = conf_matrix.max() / 2.
	for i in range(conf_matrix.shape[0]):
		for j in range(conf_matrix.shape[1]):
			ax.text(j, i, format(conf_matrix[i, j], fmt),
                    ha="center", va="center",
                    color="white" if conf_matrix[i, j] > thresh else "black")
	fig.tight_layout()
	plt.savefig("Confusion_Matrix")
	plt.show()