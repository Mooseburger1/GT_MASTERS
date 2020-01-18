package edu.gatech.cse6250.features

import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.{ Vector, Vectors }
import org.apache.spark.rdd.RDD

/**
 * @author Hang Su
 */
object FeatureConstruction {

  /**
   * ((patient-id, feature-name), feature-value)
   */
  type FeatureTuple = ((String, String), Double)

  /**
   * Aggregate feature tuples from diagnostic with COUNT aggregation,
   *
   * @param diagnostic RDD of diagnostic
   * @return RDD of feature tuples
   */
  def constructDiagnosticFeatureTuple(diagnostic: RDD[Diagnostic]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //diagnostic.sparkContext.parallelize(List((("patient", "diagnostics"), 1.0)))
    diagnostic.map(x => ((x.patientID, x.code.toLowerCase), 1.0)).reduceByKey((x, y) => x + y).map(x => x.asInstanceOf[FeatureTuple])
  }

  /**
   * Aggregate feature tuples from medication with COUNT aggregation,
   *
   * @param medication RDD of medication
   * @return RDD of feature tuples
   */
  def constructMedicationFeatureTuple(medication: RDD[Medication]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //medication.sparkContext.parallelize(List((("patient", "med"), 1.0)))
    medication.map(x => ((x.patientID, x.medicine.toLowerCase), 1.0)).reduceByKey((x, y) => x + y).map(x => x.asInstanceOf[FeatureTuple])
  }

  /**
   * Aggregate feature tuples from lab result, using AVERAGE aggregation
   *
   * @param labResult RDD of lab result
   * @return RDD of feature tuples
   */
  def constructLabFeatureTuple(labResult: RDD[LabResult]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //labResult.sparkContext.parallelize(List((("patient", "lab"), 1.0)))
    labResult.map(x => ((x.patientID, x.testName.toLowerCase), (x.value, 1.0))).reduceByKey((x, y) => ((x._1 + y._1), (x._2 + y._2))).map(x => (x._1, x._2._1 / x._2._2).asInstanceOf[FeatureTuple])
  }

  /**
   * Aggregate feature tuple from diagnostics with COUNT aggregation, but use code that is
   * available in the given set only and drop all others.
   *
   * @param diagnostic   RDD of diagnostics
   * @param candiateCode set of candidate code, filter diagnostics based on this set
   * @return RDD of feature tuples
   */
  def constructDiagnosticFeatureTuple(diagnostic: RDD[Diagnostic], candiateCode: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //diagnostic.sparkContext.parallelize(List((("patient", "diagnostics"), 1.0)))
    diagnostic.filter(x => candiateCode.contains(x.code)).map(x => ((x.patientID, x.code.toLowerCase), 1.0)).reduceByKey((x, y) => x + y).map(x => x.asInstanceOf[FeatureTuple])
  }

  /**
   * Aggregate feature tuples from medication with COUNT aggregation, use medications from
   * given set only and drop all others.
   *
   * @param medication          RDD of diagnostics
   * @param candidateMedication set of candidate medication
   * @return RDD of feature tuples
   */
  def constructMedicationFeatureTuple(medication: RDD[Medication], candidateMedication: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //medication.sparkContext.parallelize(List((("patient", "med"), 1.0)))
    medication.filter(x => candidateMedication.contains(x.medicine)).map(x => ((x.patientID, x.medicine.toLowerCase), 1.0)).reduceByKey((x, y) => x + y).map(x => x.asInstanceOf[FeatureTuple])
  }

  /**
   * Aggregate feature tuples from lab result with AVERAGE aggregation, use lab from
   * given set of lab test names only and drop all others.
   *
   * @param labResult    RDD of lab result
   * @param candidateLab set of candidate lab test name
   * @return RDD of feature tuples
   */
  def constructLabFeatureTuple(labResult: RDD[LabResult], candidateLab: Set[String]): RDD[FeatureTuple] = {
    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */
    //labResult.sparkContext.parallelize(List((("patient", "lab"), 1.0)))
    labResult.filter(x => candidateLab.contains(x.testName)).map(x => ((x.patientID, x.testName.toLowerCase), (x.value, 1.0))).reduceByKey((x, y) => ((x._1 + y._1), (x._2 + y._2))).map(x => (x._1, x._2._1 / x._2._2).asInstanceOf[FeatureTuple])
  }

  /**
   * Given a feature tuples RDD, construct features in vector
   * format for each patient. feature name should be mapped
   * to some index and convert to sparse feature format.
   *
   * @param sc      SparkContext to run
   * @param feature RDD of input feature tuples
   * @return
   */
  def construct(sc: SparkContext, feature: RDD[FeatureTuple]): RDD[(String, Vector)] = {

    /** save for later usage */
    feature.cache()

    /** create a feature name to id map */

    /** transform input feature */

    /**
     * Functions maybe helpful:
     * collect
     * groupByKey
     */

    /**
     * TODO implement your own code here and remove existing
     * placeholder code
     */

    val feature_to_id = feature.map(x => x._1._2).distinct.collect().zipWithIndex.toMap

    val scFeatureMap = sc.broadcast(feature_to_id)
    val result = feature.map(x => (x._1._1, (x._1._2, x._2))).groupByKey().map {
      case (id, features) =>
        val size = scFeatureMap.value.size
        val mappedFeatures = features.toList.map { case (feature, value) => (scFeatureMap.value(feature), value) }
        val featureVector = Vectors.sparse(size, mappedFeatures)
        val sparseVector = (id, featureVector)
        sparseVector
    }

    // val result = sc.parallelize(Seq(
    //   ("Patient-NO-1", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-2", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-3", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-4", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-5", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-6", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-7", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-8", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-9", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)),
    //   ("Patient-NO-10", Vectors.dense(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0))))
    result

    /** The feature vectors returned can be sparse or dense. It is advisable to use sparse */

  }
}

