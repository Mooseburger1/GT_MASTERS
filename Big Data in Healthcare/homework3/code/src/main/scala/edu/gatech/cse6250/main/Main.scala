package edu.gatech.cse6250.main

import java.text.SimpleDateFormat

import edu.gatech.cse6250.clustering.Metrics
import edu.gatech.cse6250.features.FeatureConstruction
import edu.gatech.cse6250.helper.{ CSVHelper, SparkHelper }
import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import edu.gatech.cse6250.phenotyping.T2dmPhenotype
import org.apache.spark.mllib.clustering.{ GaussianMixture, KMeans, StreamingKMeans }
import org.apache.spark.mllib.feature.StandardScaler
import org.apache.spark.mllib.linalg.{ DenseMatrix, Matrices, Vector, Vectors }
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.regexp_replace

import scala.io.Source

/**
 * @author Hang Su <hangsu@gatech.edu>,
 * @author Yu Jing <yjing43@gatech.edu>,
 * @author Ming Liu <mliu302@gatech.edu>
 */
object Main {
  def main(args: Array[String]) {
    import org.apache.log4j.{ Level, Logger }

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)

    val spark = SparkHelper.spark
    val sc = spark.sparkContext
    //  val sqlContext = spark.sqlContext

    /** initialize loading of data */
    val (medication, labResult, diagnostic) = loadRddRawData(spark)
    val (candidateMedication, candidateLab, candidateDiagnostic) = loadLocalRawData

    /** conduct phenotyping */
    val phenotypeLabel = T2dmPhenotype.transform(medication, labResult, diagnostic)

    /** feature construction with all features */
    val featureTuples = sc.union(
      FeatureConstruction.constructDiagnosticFeatureTuple(diagnostic),
      FeatureConstruction.constructLabFeatureTuple(labResult),
      FeatureConstruction.constructMedicationFeatureTuple(medication)
    )

    // =========== USED FOR AUTO GRADING CLUSTERING GRADING =============
    // phenotypeLabel.map{ case(a,b) => s"$a\t$b" }.saveAsTextFile("data/phenotypeLabel")
    // featureTuples.map{ case((a,b),c) => s"$a\t$b\t$c" }.saveAsTextFile("data/featureTuples")
    // return
    // ==================================================================

    val rawFeatures = FeatureConstruction.construct(sc, featureTuples)

    val (kMeansPurity, gaussianMixturePurity, streamingPurity) = testClustering(phenotypeLabel, rawFeatures)

    println(f"[All feature] purity of kMeans is: $kMeansPurity%.5f")
    println(f"[All feature] purity of GMM is: $gaussianMixturePurity%.5f")
    println(f"[All feature] purity of StreamingKmeans is: $streamingPurity%.5f")

    /** feature construction with filtered features */
    val filteredFeatureTuples = sc.union(
      FeatureConstruction.constructDiagnosticFeatureTuple(diagnostic, candidateDiagnostic),
      FeatureConstruction.constructLabFeatureTuple(labResult, candidateLab),
      FeatureConstruction.constructMedicationFeatureTuple(medication, candidateMedication)
    )

    val filteredRawFeatures = FeatureConstruction.construct(sc, filteredFeatureTuples)

    val (kMeansPurity2, gaussianMixturePurity2, streamingPurity2) = testClustering(phenotypeLabel, filteredRawFeatures)
    println(f"[Filtered feature] purity of kMeans is: $kMeansPurity2%.5f")
    println(f"[Filtered feature] purity of GMM is: $gaussianMixturePurity2%.5f")
    println(f"[Filtered feature] purity of StreamingKmeans is: $streamingPurity2%.5f")
  }

  def testClustering(phenotypeLabel: RDD[(String, Int)], rawFeatures: RDD[(String, Vector)]): (Double, Double, Double) = {
    import org.apache.spark.mllib.linalg.Matrix
    import org.apache.spark.mllib.linalg.distributed.RowMatrix

    println("phenotypeLabel: " + phenotypeLabel.count)
    /** scale features */
    val scaler = new StandardScaler(withMean = true, withStd = true).fit(rawFeatures.map(_._2))
    val features = rawFeatures.map({ case (patientID, featureVector) => (patientID, scaler.transform(Vectors.dense(featureVector.toArray))) })
    println("features: " + features.count)
    val rawFeatureVectors = features.map(_._2).cache()
    println("rawFeatureVectors: " + rawFeatureVectors.count)

    /** reduce dimension */
    val mat: RowMatrix = new RowMatrix(rawFeatureVectors)
    val pc: Matrix = mat.computePrincipalComponents(10) // Principal components are stored in a local dense matrix.
    val featureVectors = mat.multiply(pc).rows

    val densePc = Matrices.dense(pc.numRows, pc.numCols, pc.toArray).asInstanceOf[DenseMatrix]

    def transform(feature: Vector): Vector = {
      val scaled = scaler.transform(Vectors.dense(feature.toArray))
      Vectors.dense(Matrices.dense(1, scaled.size, scaled.toArray).multiply(densePc).toArray)
    }

    /**
     * TODO: K Means Clustering using spark mllib
     * Train a k means model using the variabe featureVectors as input
     * Set maxIterations =20 and seed as 6250L
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */
    val km = new KMeans().setK(3).setSeed(6250L).setMaxIterations(20)
    val model = km.run(featureVectors)

    val predicted = rawFeatures.map(x => x._1).zip(model.predict(featureVectors)) // (patientID, predicted cluster)

    val results = predicted.join(phenotypeLabel).map(_._2) // (predicted cluster#, actual class)

    // val case1_total = results.filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val case2_total = results.filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val case3_total = results.filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster1 = results.filter(x => x._1 == 0).count.asInstanceOf[Double]
    // val cluster1_class1 = results.filter(x => x._1 == 0).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster1_class2 = results.filter(x => x._1 == 0).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster1_class3 = results.filter(x => x._1 == 0).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster2 = results.filter(x => x._1 == 1).count.asInstanceOf[Double]
    // val cluster2_class1 = results.filter(x => x._1 == 1).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster2_class2 = results.filter(x => x._1 == 1).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster2_class3 = results.filter(x => x._1 == 1).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster3 = results.filter(x => x._1 == 2).count.asInstanceOf[Double]
    // val cluster3_class1 = results.filter(x => x._1 == 2).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster3_class2 = results.filter(x => x._1 == 2).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster3_class3 = results.filter(x => x._1 == 2).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // println("total cluster1: " + total_cluster1)
    // println("cluster1 class1: " + cluster1_class1 + "=" + (cluster1_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster1 class2: " + cluster1_class2 + "=" + (cluster1_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster1 class3: " + cluster1_class3 + "=" + (cluster1_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster2: " + total_cluster2)
    // println("cluster2 class1: " + cluster2_class1 + "=" + (cluster2_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster2 class2: " + cluster2_class2 + "=" + (cluster2_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster2 class3: " + cluster2_class3 + "=" + (cluster2_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster3: " + total_cluster3)
    // println("cluster3 class1: " + cluster3_class1 + "=" + (cluster3_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster3 class2: " + cluster3_class2 + "=" + (cluster3_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster3 class3: " + cluster3_class3 + "=" + (cluster3_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("Cluster totals: " + (total_cluster1 + total_cluster2 + total_cluster3))

    val kMeansPurity = Metrics.purity(results)

    /**
     * TODO: GMMM Clustering using spark mllib
     * Train a Gaussian Mixture model using the variabe featureVectors as input
     * Set maxIterations =20 and seed as 6250L
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */

    val gmm = new GaussianMixture().setMaxIterations(20).setK(3).setSeed(6250L)
    val model2 = gmm.run(featureVectors)

    val predictedgmm = rawFeatures.map(x => x._1).zip(model2.predict(featureVectors)) // (patientID, predicted cluster)

    val resultsgmm = predictedgmm.join(phenotypeLabel).map(_._2)

    // val case1_total = resultsgmm.filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val case2_total = resultsgmm.filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val case3_total = resultsgmm.filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster1 = resultsgmm.filter(x => x._1 == 0).count.asInstanceOf[Double]
    // val cluster1_class1 = resultsgmm.filter(x => x._1 == 0).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster1_class2 = resultsgmm.filter(x => x._1 == 0).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster1_class3 = resultsgmm.filter(x => x._1 == 0).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster2 = resultsgmm.filter(x => x._1 == 1).count.asInstanceOf[Double]
    // val cluster2_class1 = resultsgmm.filter(x => x._1 == 1).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster2_class2 = resultsgmm.filter(x => x._1 == 1).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster2_class3 = resultsgmm.filter(x => x._1 == 1).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster3 = resultsgmm.filter(x => x._1 == 2).count.asInstanceOf[Double]
    // val cluster3_class1 = resultsgmm.filter(x => x._1 == 2).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster3_class2 = resultsgmm.filter(x => x._1 == 2).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster3_class3 = resultsgmm.filter(x => x._1 == 2).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // println("total cluster1: " + total_cluster1)
    // println("cluster1 class1: " + cluster1_class1 + "=" + (cluster1_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster1 class2: " + cluster1_class2 + "=" + (cluster1_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster1 class3: " + cluster1_class3 + "=" + (cluster1_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster2: " + total_cluster2)
    // println("cluster2 class1: " + cluster2_class1 + "=" + (cluster2_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster2 class2: " + cluster2_class2 + "=" + (cluster2_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster2 class3: " + cluster2_class3 + "=" + (cluster2_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster3: " + total_cluster3)
    // println("cluster3 class1: " + cluster3_class1 + "=" + (cluster3_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster3 class2: " + cluster3_class2 + "=" + (cluster3_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster3 class3: " + cluster3_class3 + "=" + (cluster3_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("Cluster totals: " + (total_cluster1 + total_cluster2 + total_cluster3))

    val gaussianMixturePurity = Metrics.purity(resultsgmm)

    /**
     * TODO: StreamingKMeans Clustering using spark mllib
     * Train a StreamingKMeans model using the variabe featureVectors as input
     * Set the number of cluster K = 3, DecayFactor = 1.0, number of dimensions = 10, weight for each center = 0.5, seed as 6250L
     * In order to feed RDD[Vector] please use latestModel, see more info: https://spark.apache.org/docs/2.2.0/api/scala/index.html#org.apache.spark.mllib.clustering.StreamingKMeans
     * To run your model, set time unit as 'points'
     * Assign each feature vector to a cluster(predicted Class)
     * Obtain an RDD[(Int, Int)] of the form (cluster number, RealClass)
     * Find Purity using that RDD as an input to Metrics.purity
     * Remove the placeholder below after your implementation
     */

    val skm = new StreamingKMeans(3, 1.0, "points").setRandomCenters(10, 0.5, 6250L)
    val model3 = skm.latestModel.update(featureVectors, 1.0, "points")

    val predictskm = rawFeatures.map(x => x._1).zip(model3.predict(featureVectors))

    val resultsskm = predictskm.join(phenotypeLabel).map(_._2)
    val streamKmeansPurity = Metrics.purity(resultsskm)

    // val case1_total = resultsskm.filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val case2_total = resultsskm.filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val case3_total = resultsskm.filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster1 = resultsskm.filter(x => x._1 == 0).count.asInstanceOf[Double]
    // val cluster1_class1 = resultsskm.filter(x => x._1 == 0).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster1_class2 = resultsskm.filter(x => x._1 == 0).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster1_class3 = resultsskm.filter(x => x._1 == 0).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster2 = resultsskm.filter(x => x._1 == 1).count.asInstanceOf[Double]
    // val cluster2_class1 = resultsskm.filter(x => x._1 == 1).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster2_class2 = resultsskm.filter(x => x._1 == 1).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster2_class3 = resultsskm.filter(x => x._1 == 1).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // val total_cluster3 = resultsskm.filter(x => x._1 == 2).count.asInstanceOf[Double]
    // val cluster3_class1 = resultsskm.filter(x => x._1 == 2).filter(x => x._2 == 1).count.asInstanceOf[Double]
    // val cluster3_class2 = resultsskm.filter(x => x._1 == 2).filter(x => x._2 == 2).count.asInstanceOf[Double]
    // val cluster3_class3 = resultsskm.filter(x => x._1 == 2).filter(x => x._2 == 3).count.asInstanceOf[Double]

    // println("total cluster1: " + total_cluster1)
    // println("cluster1 class1: " + cluster1_class1 + "=" + (cluster1_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster1 class2: " + cluster1_class2 + "=" + (cluster1_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster1 class3: " + cluster1_class3 + "=" + (cluster1_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster2: " + total_cluster2)
    // println("cluster2 class1: " + cluster2_class1 + "=" + (cluster2_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster2 class2: " + cluster2_class2 + "=" + (cluster2_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster2 class3: " + cluster2_class3 + "=" + (cluster2_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("total cluster3: " + total_cluster3)
    // println("cluster3 class1: " + cluster3_class1 + "=" + (cluster3_class1 / case1_total).asInstanceOf[Double] + "%")
    // println("cluster3 class2: " + cluster3_class2 + "=" + (cluster3_class2 / case2_total).asInstanceOf[Double] + "%")
    // println("cluster3 class3: " + cluster3_class3 + "=" + (cluster3_class3 / case3_total).asInstanceOf[Double] + "%")

    // println("Cluster totals: " + (total_cluster1 + total_cluster2 + total_cluster3))

    (kMeansPurity, gaussianMixturePurity, streamKmeansPurity)
  }

  /**
   * load the sets of string for filtering of medication
   * lab result and diagnostics
   *
   * @return
   */
  def loadLocalRawData: (Set[String], Set[String], Set[String]) = {
    val candidateMedication = Source.fromFile("data/med_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    val candidateLab = Source.fromFile("data/lab_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    val candidateDiagnostic = Source.fromFile("data/icd9_filter.txt").getLines().map(_.toLowerCase).toSet[String]
    (candidateMedication, candidateLab, candidateDiagnostic)
  }

  def sqlDateParser(input: String, pattern: String = "yyyy-MM-dd'T'HH:mm:ssX"): java.sql.Date = {
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssX")
    new java.sql.Date(dateFormat.parse(input).getTime)
  }

  def loadRddRawData(spark: SparkSession): (RDD[Medication], RDD[LabResult], RDD[Diagnostic]) = {
    /* the sql queries in spark required to import sparkSession.implicits._ */
    import spark.implicits._
    val sqlContext = spark.sqlContext

    /* a helper function sqlDateParser may useful here */

    /**
     * load data using Spark SQL into three RDDs and return them
     * Hint:
     * You can utilize edu.gatech.cse6250.helper.CSVHelper
     * through your sparkSession.
     *
     * This guide may helps: https://bit.ly/2xnrVnA
     *
     * Notes:Refer to model/models.scala for the shape of Medication, LabResult, Diagnostic data type.
     * Be careful when you deal with String and numbers in String type.
     * Ignore lab results with missing (empty or NaN) values when these are read in.
     * For dates, use Date_Resulted for labResults and Order_Date for medication.
     *
     */

    /**
     * TODO: implement your own code here and remove
     * existing placeholder code below
     */

    val med = CSVHelper.loadCSVAsTable(spark, "data/medication_orders_INPUT.csv", "Medication")
    med.createOrReplaceTempView("med")
    val medication: RDD[Medication] = spark.sql("""SELECT Member_ID as patientID, to_date(Order_Date) as date, Drug_Name AS medicine FROM med""").map(x => Medication(x.getString(0), x.getDate(1), x.getString(2))).rdd

    val lab = CSVHelper.loadCSVAsTable(spark, "data/lab_results_INPUT.csv", "LabResult").na.drop("all", Seq("Numeric_Result")).withColumn("Numeric_Result", regexp_replace($"Numeric_Result", ",", ""))
    lab.createOrReplaceTempView("lab")
    val labResult: RDD[LabResult] = spark.sql("""SELECT Member_ID AS patientID, to_date(Date_Resulted) as date, Result_Name AS testName, DOUBLE(Numeric_Result) AS value FROM lab""").map(x => LabResult(x.getString(0), x.getDate(1), x.getString(2), x.getDouble(3))).rdd

    val diag = CSVHelper.loadCSVAsTable(spark, "data/encounter_INPUT.csv", "Diagnostic")
    val diag_dx = CSVHelper.loadCSVAsTable(spark, "data/encounter_dx_INPUT.csv", "Diagnosticdx")
    diag.createOrReplaceTempView("diag")
    diag_dx.createOrReplaceTempView("diag_dx")
    val diagnostic: RDD[Diagnostic] = spark.sql("""SELECT a.Member_ID AS patientID,to_date(a.Encounter_DateTime) as date , b.code AS code FROM diag AS a JOIN diag_dx AS b ON a.Encounter_ID = b.Encounter_ID """).map(x => Diagnostic(x.getString(0), x.getDate(1), x.getString(2))).rdd

    (medication, labResult, diagnostic)
  }

}
