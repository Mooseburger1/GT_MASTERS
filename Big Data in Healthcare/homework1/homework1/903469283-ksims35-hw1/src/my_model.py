import utils
import utils
from etl import *
import pandas as pd
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
import warnings

warnings.filterwarnings('ignore')
#Note: You can reuse code that you wrote in etl.py and models.py and cross.py over here. It might help.
# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

'''
You may generate your own features over here.
Note that for the test data, all events are already filtered such that they fall in the observation window of their respective patients. Thus, if you were to generate features similar to those you constructed in code/etl.py for the test data, all you have to do is aggregate events for each patient.
IMPORTANT: Store your test data features in a file called "test_features.txt" where each line has the
patient_id followed by a space and the corresponding feature in sparse format.
Eg of a line:
60 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514
Here, 60 is the patient id and 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514 is the feature for the patient with id 60.

Save the file as "test_features.txt" and save it inside the folder deliverables

input:
output: X_train,Y_train,X_test
'''
def my_features():
	#TODO: complete this
	train_path = '../deliverables/features_svmlight.train'
	test_path = '../data/test/'

	#load train data
	X_train, Y_train = utils.get_data_from_svmlight(train_path)

	#load test data
	events_test = pd.read_csv(test_path + 'events.csv')
	efm_test = pd.read_csv(test_path + 'event_feature_map.csv')


	#create features from test data
	def create_test_features(events, feature_map):
		aggregated_events = aggregate_events(events, '_', feature_map, '_')
		grp = aggregated_events.groupby('patient_id').agg(list)
		def tuples(x,y):
			return zip(x,y)
		patient_features = pd.Series.to_dict(grp[['feature_id','feature_value']].apply(lambda x: list(tuples(*x)), axis = 1))
		return patient_features

	patient_test_features = create_test_features(events_test, efm_test)

	#save test features
	def save_test_features_svm(features, output):
		file = open(output, 'wb')
		#svm format for test_features
		for k in features.keys():
			features[k] = sorted(features[k])
			file.write(bytes(("{} ".format(int(k))),'UTF-8'))
			for v in features[k]:
				file.write(bytes(("{}:{} ".format(v[0],v[1])),'UTF-8'))
			file.write(bytes(("\n"),'UTF-8'))
		file.close()


	save_test_features_svm(patient_test_features, "../deliverables/test_features.txt")

    #load X_test from svmlight
	X_test = load_svmlight_file("../deliverables/test_features.txt", n_features=3190)[0]
    
	return X_train,Y_train,X_test


'''
You can use any model you wish.

input: X_train, Y_train, X_test
output: Y_pred
'''
def my_classifier_predictions(X_train,Y_train,X_test):
	random_state=42
	#TODO: complete this

	pca = PCA(n_components = 45)
	pca.fit(X_train.toarray())
	X_train = pca.transform(X_train.toarray())
	X_test = pca.transform(X_test.toarray())
	
	svm = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0,
			decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
			max_iter=-1, probability=True, random_state=49, shrinking=True,
			tol=0.001, verbose=False)

	rf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=25,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=500, n_jobs=1,
            oob_score=False, random_state=49, verbose=0, warm_start=False)

	gb = GradientBoostingClassifier(criterion='friedman_mse', init=None,
              learning_rate=0.1, loss='deviance', max_depth=15,
              max_features=None, max_leaf_nodes=None,
              min_impurity_decrease=0.0, min_impurity_split=None,
              min_samples_leaf=1, min_samples_split=2,
              min_weight_fraction_leaf=0.0, n_estimators=4, presort='auto',
              random_state=49, subsample=1.0, verbose=0, warm_start=False)

	nn = MLPClassifier(activation='tanh', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(5, 2), learning_rate='adaptive',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=49, shuffle=True,
       solver='adam', tol=0.0001, validation_fraction=0.1, verbose=False,
       warm_start=False)

	ab = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
          learning_rate=1.0, n_estimators=50, random_state=49)

	lr = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=49, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)

	nb_clf = GaussianNB()
	nb_clf.fit(X_train,Y_train)
	nb = nb_clf

	gpc = GaussianProcessClassifier(copy_X_train=True, kernel=None,
             max_iter_predict=100, multi_class='one_vs_rest', n_jobs=1,
             n_restarts_optimizer=0, optimizer='fmin_l_bfgs_b',
             random_state=49, warm_start=False)

	#create ensemble classifier
	estimators=[('gpc', gpc), ('ab', ab), ('nn', nn), ('svm', svm), ('random_forest', rf), ('gradient_boost', gb), ('logistic_regression', lr), ('naive_bayes', nb)]
	ensemble = VotingClassifier(estimators, voting='hard')
	ensemble.fit(X_train, Y_train)

	return ensemble.predict(X_test)


def main():
	X_train, Y_train, X_test = my_features()
	Y_pred = my_classifier_predictions(X_train,Y_train,X_test)
	utils.generate_submission("../deliverables/test_features.txt",Y_pred)
	#The above function will generate a csv file of (patient_id,predicted label) and will be saved as "my_predictions.csv" in the deliverables folder.

if __name__ == "__main__":
    main()

	