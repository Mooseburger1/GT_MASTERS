---
---
# Spark MLlib and Scikit-learn

::: tip Learning Objectives

- Understand input to MLlib.
- Learn to run basic classification algorithms.
- Learn to export/load trained models.
- Develop models using python machine learning module.

:::

In this section, you will learn how to build a heart failure (HF) predictive model. You should have finished previous [Spark Application](/spark/spark-application.html) section. You will first learn how to train a model using Spark MLlib and save it. Next, you will learn how to achieve same goal using Python Scikit-learn machine learning module for verification purpose.

## MLlib

You will first load data and compute some high-level summary 
statistics, then train a classifier to predict heart failure.

### Load Samples

Loading data from previously saved data can be achieved by

``` scala
import org.apache.spark.mllib.util.MLUtils
val data = MLUtils.loadLibSVMFile(sc, "samples")
```

### Basic Statistics

Spark MLlib provides various functions to compute summary statistics that are useful when doing machine learning and data analysis tasks.

```scala
import org.apache.spark.mllib.stat.{MultivariateStatisticalSummary, Statistics}

// colStats() calculates the column statistics for RDD[Vector]
// we need to extract only the features part of each LabeledPoint:
//   RDD[LabeledPoint] => RDD[Vector] 
val summary = Statistics.colStats(data.map(_.features))

// summary.mean: a dense vector containing the mean value for each feature (column)
// the mean of the first feature is 0.3
summary.mean(0)

// the variance of the first feature
summary.variance(0)

// the number of non-zero values of the first feature
summary.numNonzeros(0)
```

### Split data

In a typical machine learning problem, we need to split data into training (60%) and testing (40%) set.

```scala
val splits = data.randomSplit(Array(0.6, 0.4), seed = 15L)
val train = splits(0).cache()
val test = splits(1).cache()
```

### Train classifier

Let's train a linear SVM model using Stochastic Gradient Descent (SGD) on the training set to predict heart failure

```scala
import org.apache.spark.mllib.classification.SVMWithSGD
val numIterations = 100
val model = SVMWithSGD.train(train, numIterations)
```

### Testing

For each sample in the testing set, output a (prediction, label) pair, and calculate the prediction accuracy. We use the broadcast mechanism to avoid unnecessary data copy.

```scala
val scModel = sc.broadcast(model)
val predictionAndLabel = test.map(x => (scModel.value.predict(x.features), x.label))
val accuracy = predictionAndLabel.filter(x => x._1 == x._2).count / test.count.toFloat
println("testing Accuracy  = " + accuracy)
```

### Save & load model

In real world setting, you may need to save the trained model. You can achieve that by directly serialize you model object using java `ObjectOutputStream` and save

```scala
  import java.io.{FileOutputStream, ObjectOutputStream, ObjectInputStream, FileInputStream}
  // save model
  val oos = new ObjectOutputStream(new FileOutputStream("model"))
  oos.writeObject(model)
  oos.close()

  // load model from disk
  val ois = new ObjectInputStream(new FileInputStream("model"))
  val loadedModel = ois.readObject().asInstanceOf[org.apache.spark.mllib.classification.SVMModel]
  ois.close()
```

## Scikit-learn

If typical data set is often small enough after feature construction described in previous [Spark Application](/spark/spark-application.html) section, you may consider running machine learning predictive model training and testing using your familiar tools like scikit-learn in Python or some R packages. Here we show how to do that in Scikit-learn, a Python machine learning library.

### Fetch data

In order to work with Scikit-learn, you will need to take data out of HDFS into a local file system. We can get the `samples` folder from your home directory in HDFS and merge content into one single file with the command below

``` bash
hdfs dfs -getmerge samples patients.svmlight
```

### Move on with Python

In later steps, you will use python interactive shell. To open a python interactive shell, just type  `python` in bash. You will get prompt similar to the sample below 

``` python
[hang@bootcamp1 ~]$ python
Python 2.7.10 |Continuum Analytics, Inc.| (default, Oct 19 2015, 18:04:42)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
>>>
```

which show version and distribution of the python installation you are using. Here we pre-installed [Anaconda](https://www.continuum.io/downloads)

### Load and split data

Now we can load data and split it into training and testing set in similar way as the MLlib approach.

```python
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_svmlight_file

X, y = load_svmlight_file("patients.svmlight")
X = X.toarray() # make it dense
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=41)
```

### Train classifier

Let's train a linear SVM model again on the training set to predict heart failure

```python
from sklearn.svm import LinearSVC
model = LinearSVC(C=1.0, random_state=42)
model.fit(X_train, y_train)
```

### Testing

We can get prediction accuracy and [AUC](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) on testing set as

``` python
from sklearn.metrics import roc_auc_score
accuracy = model.score(X_test, y_test)

y_score = model.decision_function(X_test)
auc = roc_auc_score(y_test, y_score)

print "accuracy = %.3f, AUC = %.3f" % (accuracy, auc)
```

### Save & load model

We can save and load the trained model via [pickle](https://docs.python.org/2/library/pickle.html) serialization module in Python like
``` python
import pickle
with open('pysvcmodel.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('pysvcmodel.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
```

### Sparsity and predictive features
Since we have limited training data but a large number of features, we may consider using L1 penalty on model to regularize parameters.

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

l1_model = LinearSVC(C=1.0, random_state=42, dual=False, penalty='l1')
l1_model.fit(X_train, y_train)

accuracy = l1_model.score(X_test, y_test)

y_score = l1_model.decision_function(X_test)
auc = roc_auc_score(y_test, y_score)

print "for sparse model, accuracy = %.3f, auc = %.3f" % (accuracy, auc)
```

Before fitting a model, we scaled the data to make sure weights of features are comparable. With the sparse model we get from previous example, we can actually identify predictive features according to their coefficients. Here we assume you did the last exercise of previous section about Spark Application. If not, please do that first.

```python
import numpy as np

## loading mapping
mapping = []
with open('mapping.txt') as f:
    for line in f.readlines():
        splits = line.split('|') # feature-name | feature-index
        mapping.append(splits[0])

## get last 10 - the largest 10 indices
top_10 =np.argsort(l1_model.coef_[0])[-10:]

for index, fid in enumerate(top_10[::-1]): #read in reverse order
    print "%d: feature [%s] with coef %.3f" % (index, mapping[fid], l1_model.coef_[0][fid])
```

<NotInUse>

## Regression

Suppose now instead of predicting whether a patient has heart failure, we want to predict the total amount of payment for each patient. This is no longer a binary classification problem, because the labels we try to predict are real-valued numbers. In this case, we can use the regression methods in MLlib.

### Construct data

We need to construct a new dataset for this regression problem. The only difference is that we change the label from `heartfailure` (binary) to `PAYMENT` (real value).

```scala
scala> val labelID = featureMap("PAYMENT")
scala> val data = features.map{ case ((patient, feature), value) =>
                    (patient, (feature, value))
                  }.
                  groupByKey().
                  map{ x =>
                    val label = x._2.find(_._1 == labelID).get._2
                    val featureNoLabel = x._2.toSeq.filter(_._1 != labelID)
                    LabeledPoint(label, Vectors.sparse(numOfFeatures, featureNoLabel))
                  }
```

### Split data

2. Split data into training (60%) and test (40%) set.

```scala
scala> val splits = data.randomSplit(Array(0.6, 0.4), seed = 0L)
scala> val train = splits(0).cache()
scala> val test = splits(1).cache()
```

### Training
Train a linear regression model using SGD on the training set

```scala
import org.apache.spark.mllib.regression.LinearRegressionWithSGD
scala> val numIterations = 100
scala> val model = LinearRegressionWithSGD.train(training, numIterations)
```

### Testing
For each example in the testing set, output a (prediction, label) pair, and calculate the mean squared error.

```scala
scala> val predictionAndLabel = test.map(x => (model.predict(x.features), x.label))
scala> val MSE = predictionAndLabel.map{case(p, l) => math.pow((p - l), 2)}.mean()
scala> println("testing Mean Squared Error = " + MSE)
```

</NotInUse>