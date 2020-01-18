import os
import pickle
import pandas as pd
import numpy as np

##### DO NOT MODIFY OR REMOVE THIS VALUE #####
checksum = '169a9820bbc999009327026c9d76bcf1'
##### DO NOT MODIFY OR REMOVE THIS VALUE #####

PATH_TRAIN = "../data/mortality/train/"
PATH_VALIDATION = "../data/mortality/validation/"
PATH_TEST = "../data/mortality/test/"
PATH_OUTPUT = "../data/mortality/processed/"


def convert_icd9(icd9_object):
	"""
	:param icd9_object: ICD-9 code (Pandas/Numpy object).
	:return: extracted main digits of ICD-9 code
	"""
	icd9_str = str(icd9_object)
	# TODO: Extract the the first 3 or 4 alphanumeric digits prior to the decimal point from a given ICD-9 code.
	# TODO: Read the homework description carefully.
	
	if icd9_str.lower().startswith('e'): return icd9_str.split('.')[0][:4]
	else: return icd9_str.split('.')[0][:3]


def build_codemap(df_icd9, transform):
	"""
	:return: Dict of code map {main-digits of ICD9: unique feature ID}
	"""
	# TODO: We build a code map using ONLY train data. Think about how to construct validation/test sets using this.
	df_digits = df_icd9.dropna(subset=['ICD9_CODE']).ICD9_CODE.apply(convert_icd9).unique()

	
	return {str(x):pos for pos,x in enumerate(df_digits)}

def apply_codemap(x, codemap):
	try:
		return codemap[x]
	except:
		return np.nan

def create_dataset(path, codemap, transform):
	"""
	:param path: path to the directory contains raw files.
	:param codemap: 3-digit ICD-9 code feature map
	:param transform: e.g. convert_icd9
	:return: List(patient IDs), List(labels), Visit sequence data as a List of List of List.
	"""
	# TODO: 1. Load data from the three csv files
	# TODO: Loading the mortality file is shown as an example below. Load two other files also.
	df_mortality = pd.read_csv(os.path.join(path, "MORTALITY.csv"))
	df_diagnosis = pd.read_csv(os.path.join(path, "DIAGNOSES_ICD.csv"))
	df_admissions = pd.read_csv(os.path.join(path, "ADMISSIONS.csv"))

	# TODO: 2. Convert diagnosis code in to unique feature ID.
	# TODO: HINT - use 'transform(convert_icd9)' you implemented and 'codemap'.
	df_diagnosis.ICD9_CODE = df_diagnosis.ICD9_CODE.apply(convert_icd9).apply(lambda x: apply_codemap(x, codemap))
	df_diagnosis = df_diagnosis.dropna(subset=['ICD9_CODE'])
	
	

	# TODO: 3. Group the diagnosis codes for the same visit.
	# TODO: 4. Group the visits for the same patient.
	# TODO: 5. Make a visit sequence dataset as a List of patient Lists of visit Lists
	# TODO: Visits for each patient must be sorted in chronological order.
	diag_admiss = pd.merge(left=df_diagnosis.loc[:,['SUBJECT_ID','HADM_ID','ICD9_CODE']], right=df_admissions.loc[:,['SUBJECT_ID','HADM_ID','ADMITTIME']], how='inner', on=['SUBJECT_ID', 'HADM_ID']).drop('HADM_ID', axis=1).sort_values(['SUBJECT_ID', 'ADMITTIME']).groupby(['SUBJECT_ID','ADMITTIME'])['ICD9_CODE'].apply(list).reset_index().groupby('SUBJECT_ID')['ICD9_CODE'].apply(list)


	# TODO: 6. Make patient-id List and label List also.
	# TODO: The order of patients in the three List output must be consistent.
	patient_ids = diag_admiss.index.tolist()
	labels = df_mortality.sort_values('SUBJECT_ID').MORTALITY.tolist()
	seq_data = diag_admiss.tolist()
	return patient_ids, labels, seq_data


def main():
	# Build a code map from the train set
	print("Build feature id map")
	df_icd9 = pd.read_csv(os.path.join(PATH_TRAIN, "DIAGNOSES_ICD.csv"), usecols=["ICD9_CODE"])
	codemap = build_codemap(df_icd9, convert_icd9)
	os.makedirs(PATH_OUTPUT, exist_ok=True)
	pickle.dump(codemap, open(os.path.join(PATH_OUTPUT, "mortality.codemap.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Train set
	print("Construct train set")
	train_ids, train_labels, train_seqs = create_dataset(PATH_TRAIN, codemap, convert_icd9)

	pickle.dump(train_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.train"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(train_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.train"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Validation set
	print("Construct validation set")
	validation_ids, validation_labels, validation_seqs = create_dataset(PATH_VALIDATION, codemap, convert_icd9)

	pickle.dump(validation_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(validation_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.validation"), 'wb'), pickle.HIGHEST_PROTOCOL)

	# Test set
	print("Construct test set")
	test_ids, test_labels, test_seqs = create_dataset(PATH_TEST, codemap, convert_icd9)

	pickle.dump(test_ids, open(os.path.join(PATH_OUTPUT, "mortality.ids.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_labels, open(os.path.join(PATH_OUTPUT, "mortality.labels.test"), 'wb'), pickle.HIGHEST_PROTOCOL)
	pickle.dump(test_seqs, open(os.path.join(PATH_OUTPUT, "mortality.seqs.test"), 'wb'), pickle.HIGHEST_PROTOCOL)

	print("Complete!")


if __name__ == '__main__':
	main()
