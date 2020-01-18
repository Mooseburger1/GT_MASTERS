import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import numpy as np

##### DO NOT MODIFY OR REMOVE THIS VALUE #####
checksum = '169a9820bbc999009327026c9d76bcf1'
##### DO NOT MODIFY OR REMOVE THIS VALUE #####
seed = 42
np.random.seed(seed)
torch.manual_seed(seed)

class MyMLP(nn.Module):
	def __init__(self):
		super(MyMLP, self).__init__()
		# self.hidden1 = nn.Linear(178,16,bias=True)
		# self.hidden2 = nn.Linear(16, 5, bias=True)
		# self.sigmoid=nn.Sigmoid()

		self.hidden1 = nn.Linear(178, 100, bias=True)
		self.hidden2 = nn.Linear(100, 50, bias=True)
		self.hidden3 = nn.Linear(50, 24, bias=True)
		self.hidden4 = nn.Linear(24, 12, bias=True)
		self.sigmoid = nn.Sigmoid()
		self.relu = nn.ReLU(inplace=False)
		self.output = nn.Linear(12,5, bias=True)

	def forward(self, x):
		# x = self.hidden1(x)
		# x = self.sigmoid(x)
		# x = self.hidden2(x)

		x = self.hidden1(x)
		x = self.relu(x)

		x = self.hidden2(x)
		x = self.relu(x)

		x = self.hidden3(x)
		x = self.relu(x)

		x = self.hidden4(x)
		x = self.sigmoid(x)

		x = self.output(x)
		return x


class MyCNN(nn.Module):
	def __init__(self):
		super(MyCNN, self).__init__()
		# self.conv1 = nn.Conv1d(in_channels = 1, out_channels = 6, kernel_size=5)
		# self.conv2 = nn.Conv1d(in_channels = 6, out_channels = 16, kernel_size=5)
		# self.relu = nn.ReLU(inplace=False)
		# self.pool = nn.MaxPool1d(kernel_size=2, stride=2)
		# self.fc1 = nn.Linear(in_features = 16 * 41, out_features=128, bias=True)
		# self.fc2 = nn.Linear(in_features=128, out_features=5, bias=True)

		self.conv1 = nn.Conv1d(in_channels=1, out_channels=3, kernel_size=3)
		self.relu = nn.ReLU(inplace=False)
		self.sigmoid = nn.Sigmoid()
		self.max_pool = nn.MaxPool1d(kernel_size=2, stride=2)

		self.conv2 = nn.Conv1d(in_channels=3, out_channels=15, kernel_size=3)

		self.conv3 = nn.Conv1d(in_channels=15, out_channels=20, kernel_size=3)

		self.conv4 = nn.Conv1d(in_channels=20, out_channels=30, kernel_size=3)

		self.conv5 = nn.Conv1d(in_channels=30, out_channels=100, kernel_size=3)

		self.fc1 = nn.Linear(in_features = 100 * 8, out_features=100)
		self.fc2 = nn.Linear(in_features = 100, out_features = 50)
		self.fc3 = nn.Linear(in_features = 50, out_features = 25)
		self.fc4 = nn.Linear(in_features = 25, out_features = 5)

	def forward(self, x):
		#conv block 1
		x = self.conv1(x)
		x = self.relu(x)
		x = self.max_pool(x)
		
		#conv block 2
		x = self.conv2(x)
		x = self.relu(x)
		x = self.max_pool(x)
		
		#conv block 3
		x = self.conv3(x)
		x = self.relu(x)
		x = self.max_pool(x)
		
		#conv block 4
		x = self.conv4(x)
		x = self.relu(x)
		self.max_pool(x)
		
		#conv block 5
		x = self.conv5(x)
		x = self.relu(x)
		x = self.max_pool(x)
		

		#flaten
		x = x.view(-1, 100 * 8)

		#fully connected
		x = self.fc1(x)
		x = self.relu(x)
		x = self.fc2(x)
		x = self.relu(x)
		x = self.fc3(x)
		x = self.sigmoid(x)
		x = self.fc4(x)

		# x = self.conv1(x)
		# x = self.relu(x)
		# x = self.pool(x)

		# x= self.conv2(x)
		# x = self.relu(x)
		# x = self.pool(x)

		# x = x.view(-1, 16 * 41)
		# x = self.fc1(x)
		# x = self.relu(x)
		# x = self.fc2(x)



		return x


class MyRNN(nn.Module):
	def __init__(self):
		super(MyRNN, self).__init__()
		# self.rnn = nn.GRU(input_size=1, hidden_size=16, num_layers=2, batch_first=True, dropout=0.5)
		# self.fc = nn.Linear(in_features=16, out_features=5)
		self.rnn1 = nn.GRU(input_size=1, hidden_size=20, num_layers=2, batch_first=True, dropout=0.5)
		self.rnn2 = nn.GRU(input_size=20, hidden_size=10, num_layers=2, batch_first=True, dropout=0.5)
		self.fc = nn.Linear(in_features=10, out_features=5)
	def forward(self, x):
		# x , _ = self.rnn(x)
		# x = self.fc(x[:, -1, :])
		x, h = self.rnn1(x)
		x, h = self.rnn2(x, h[:, :, -10:])
		x = self.fc(x[:, -1, :])
		return x


class MyVariableRNN(nn.Module):
	def __init__(self, dim_input):
		super(MyVariableRNN, self).__init__()
		self.fc1 = nn.Sequential(
			nn.Linear(in_features= dim_input, out_features=100, bias=True),
			nn.Dropout(),
			nn.LeakyReLU(),
			nn.Linear(in_features=100, out_features=100, bias=True),
			nn.Dropout(),
			nn.LeakyReLU(),
			nn.Linear(in_features=100, out_features=50, bias=True),
			nn.Dropout(),
			nn.ReLU(),
			nn.Linear(in_features=50, out_features=25, bias=True),
			nn.Dropout(),
			nn.ReLU())
		self.gru = nn.GRU(input_size=25, hidden_size=16, num_layers = 2, batch_first=True)
		self.gru2 = nn.GRU(input_size=16, hidden_size=8, num_layers=2, batch_first=True)
		self.fc2 = nn.Linear(in_features=8, out_features=2)

		
		# You may use the input argument 'dim_input', which is basically the number of features
		# self.fc1 = nn.Linear(in_features = dim_input, out_features=32, bias=True)
		# self.gru = nn.GRU(input_size=32, hidden_size=16, batch_first=True)
		# self.fc2 = nn.Linear(in_features=16, out_features=2)
		# self.tanh = nn.Tanh()
	def forward(self, input_tuple):
		# HINT: Following two methods might be useful
		# 'pack_padded_sequence' and 'pad_packed_sequence' from torch.nn.utils.rnn
		
		#pack = nn.utils.rnn.pack_padded_sequence(input_tuple[0], input_tuple[1], batch_first=True)
		# x = self.fc1(input_tuple[0])
		
		# x = self.tanh(x)
		
		# x, _ = self.gru(x)

		# x = self.fc2(x[:, -1, :])
		x = self.fc1(input_tuple[0])
		x,h = self.gru(x)
		x,_ = self.gru2(x, h[:, :, -8:])
		x = self.fc2(x[:, -1, :])
		return x