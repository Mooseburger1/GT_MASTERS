import numpy as np
import pandas as pd
from scipy import sparse
import torch
from torch.utils.data import TensorDataset, Dataset
from scipy.sparse import csr_matrix

##### DO NOT MODIFY OR REMOVE THIS VALUE #####
checksum = '169a9820bbc999009327026c9d76bcf1'
##### DO NOT MODIFY OR REMOVE THIS VALUE #####

def load_seizure_dataset(path, model_type):
	"""
	:param path: a path to the seizure data CSV file
	:return dataset: a TensorDataset consists of a data Tensor and a target Tensor
	"""
	# TODO: Read a csv file from path.
	df = pd.read_csv(path)
	# TODO: Please refer to the header of the file to locate X and y.
	# TODO: y in the raw data is ranging from 1 to 5. Change it to be from 0 to 4.
	df.y = df.y.apply(lambda x: x-1)
	# TODO: Remove the header of CSV file of course.
	# TODO: Do Not change the order of rows.
	# TODO: You can use Pandas if you want to.
	X = df.iloc[:, :-1].values
	y = df.iloc[:, -1].values

	if model_type == 'MLP':
		#data = torch.zeros((2, 2))
		data = torch.from_numpy(X).float()
		#target = torch.zeros(2)
		target = torch.from_numpy(y).long()
		dataset = TensorDataset(data, target)
	elif model_type == 'CNN':
		#data = torch.zeros((2, 2))
		data = torch.from_numpy(X).float().unsqueeze(1)
		#target = torch.zeros(2)
		target = torch.from_numpy(y).long()
		dataset = TensorDataset(data, target)
	elif model_type == 'RNN':
		#data = torch.zeros((2, 2))
		data = torch.from_numpy(X).float().unsqueeze(2)
		#target = torch.zeros(2)
		target = torch.from_numpy(y).long()
		dataset = TensorDataset(data, target)
	else:
		raise AssertionError("Wrong Model Type!")

	return dataset


def calculate_num_features(seqs):
	"""
	:param seqs:
	:return: the calculated number of features
	"""
	# TODO: Calculate the number of features (diagnoses codes in the train set)

	return len(np.unique(np.concatenate([np.array(j) for i in seqs for j in i])))


class VisitSequenceWithLabelDataset(Dataset):
	def __init__(self, seqs, labels, num_features):
		"""
		Args:
			seqs (list): list of patients (list) of visits (list) of codes (int) that contains visit sequences
			labels (list): list of labels (int)
			num_features (int): number of total features available
		"""

		if len(seqs) != len(labels):
			raise ValueError("Seqs and Labels have different lengths")

		self.labels = labels

		# TODO: Complete this constructor to make self.seqs as a List of which each element represent visits of a patient
		# TODO: by Numpy matrix where i-th row represents i-th visit and j-th column represent the feature ID j.
		# TODO: You can use Sparse matrix type for memory efficiency if you want

		self.seqs = []

		for i in seqs:
			matrix = np.zeros((len(i), num_features))
			for pos, j in enumerate(i):
				for k in j:
					matrix[pos, int(k)] = 1
			self.seqs.append(csr_matrix(matrix))

	def __len__(self):
		return len(self.labels)

	def __getitem__(self, index):
		# returns will be wrapped as List of Tensor(s) by DataLoader
		return self.seqs[index], self.labels[index]


def visit_collate_fn(batch):
	"""
	DataLoaderIter call - self.collate_fn([self.dataset[i] for i in indices])
	Thus, 'batch' is a list [(seq1, label1), (seq2, label2), ... , (seqN, labelN)]
	where N is minibatch size, seq is a (Sparse)FloatTensor, and label is a LongTensor

	:returns
		seqs (FloatTensor) - 3D of batch_size X max_length X num_features
		lengths (LongTensor) - 1D of batch_size
		labels (LongTensor) - 1D of batch_size
	"""

	# TODO: Return the following two things
	# TODO: 1. a tuple of (Tensor contains the sequence data , Tensor contains the length of each sequence),
	# TODO: 2. Tensor contains the label of each sequence
	max_ = 0
	for x in batch:
		if x[0].shape[0] > max_:
			max_ = x[0].shape[0]
	
	batch.sort(key = lambda x: x[0].shape[0], reverse=True)

	lengths = []
	for x in batch:
		length, width = x[0].shape
		lengths.append(length)
		x[0].resize(max_, width)

	seqs_tensor = torch.FloatTensor([x[0].toarray() for x in batch])
	lengths_tensor = torch.LongTensor(lengths)
	labels_tensor = torch.LongTensor([x[1] for x in batch])

	return (seqs_tensor, lengths_tensor), labels_tensor
