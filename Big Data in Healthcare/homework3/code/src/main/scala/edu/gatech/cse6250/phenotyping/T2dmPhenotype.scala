package edu.gatech.cse6250.phenotyping

import edu.gatech.cse6250.model.{ Diagnostic, LabResult, Medication }
import org.apache.spark.rdd.RDD

/**
 * @author Hang Su <hangsu@gatech.edu>,
 * @author Sungtae An <stan84@gatech.edu>,
 */
object T2dmPhenotype {

  /** Hard code the criteria */
  val T1DM_DX = Set("250.01", "250.03", "250.11", "250.13", "250.21", "250.23", "250.31", "250.33", "250.41", "250.43",
    "250.51", "250.53", "250.61", "250.63", "250.71", "250.73", "250.81", "250.83", "250.91", "250.93")

  val T2DM_DX = Set("250.3", "250.32", "250.2", "250.22", "250.9", "250.92", "250.8", "250.82", "250.7", "250.72", "250.6",
    "250.62", "250.5", "250.52", "250.4", "250.42", "250.00", "250.02")

  val T1DM_MED = Set("lantus", "insulin glargine", "insulin aspart", "insulin detemir", "insulin lente", "insulin nph", "insulin reg", "insulin,ultralente")

  val T2DM_MED = Set("chlorpropamide", "diabinese", "diabanase", "diabinase", "glipizide", "glucotrol", "glucotrol xl",
    "glucatrol ", "glyburide", "micronase", "glynase", "diabetamide", "diabeta", "glimepiride", "amaryl",
    "repaglinide", "prandin", "nateglinide", "metformin", "rosiglitazone", "pioglitazone", "acarbose",
    "miglitol", "sitagliptin", "exenatide", "tolazamide", "acetohexamide", "troglitazone", "tolbutamide",
    "avandia", "actos", "actos", "glipizide")

  val DM_DX = Set("790.21", "790.22", "790.2", "790.29", "648.81", "648.82", "648.83", "648.84", "648", "648.01",
    "648.02", "648.03", "648.04", "791.5", "277.7", "V77.1", "256.4", "250.*")

  /**
   * Transform given data set to a RDD of patients and corresponding phenotype
   *
   * @param medication medication RDD
   * @param labResult  lab result RDD
   * @param diagnostic diagnostic code RDD
   * @return tuple in the format of (patient-ID, label). label = 1 if the patient is case, label = 2 if control, 3 otherwise
   */
  def transform(medication: RDD[Medication], labResult: RDD[LabResult], diagnostic: RDD[Diagnostic]): RDD[(String, Int)] = {

    /**
     * Remove the place holder and implement your code here.
     * Hard code the medication, lab, icd code etc. for phenotypes like example code below.
     * When testing your code, we expect your function to have no side effect,
     * i.e. do NOT read from file or write file
     *
     * You don't need to follow the example placeholder code below exactly, but do have the same return type.
     *
     * Hint: Consider case sensitivity when doing string comparisons.
     */
    val sc = medication.sparkContext

    ////CASES///////////////////////////
    //686 (OTHER) yes @ type1 diagnosis
    val type1_id = diagnostic.filter(x => T1DM_DX.contains(x.code)).map(x => x.patientID).distinct.collect().toSet
    //3002 no @ type1 diagnosis
    val no_type1_id = diagnostic.filter(x => !type1_id.contains(x.patientID)).map(x => x.patientID).distinct.collect().toSet
    //1265 yes @type2 diagnosis
    val type2_id = diagnostic.filter(x => no_type1_id.contains(x.patientID)).filter(x => T2DM_DX.contains(x.code)).map(x => x.patientID).distinct.collect().toSet
    //1737 (OTHER) no @type2 diagnosis
    val no_type2_id = diagnostic.filter(x => no_type1_id.contains(x.patientID)).filter(x => !type2_id.contains(x.patientID)).map(x => x.patientID).distinct.collect().toSet

    val med_lower: RDD[Medication] = medication.map(x => Medication(x.patientID, x.date, x.medicine.toLowerCase))

    //838 yes @type1 medication
    val type1_med = med_lower.filter(x => (type2_id.contains(x.patientID)) && (T1DM_MED.contains(x.medicine))).map(x => x.patientID).distinct.collect().toSet
    //427 CASE!!!!!! no @type1 medication
    val no_type1_med = type2_id.filterNot(type1_med)

    //583 Yes @type2 medication
    val type2_med = med_lower.filter(x => (type1_med.contains(x.patientID)) && (T2DM_MED.contains(x.medicine))).map(x => x.patientID).distinct.collect().toSet
    //255 CASE!!!!!!!! No @type2 medication
    val no_type2_med = type1_med.filterNot(type2_med)

    // remaining patientID
    val remaining = med_lower.filter(x => type2_med.contains(x.patientID))
    // Separate data between med1 and med2
    val med1 = remaining.filter(x => T1DM_MED.contains(x.medicine))
    val med2 = remaining.filter(x => T2DM_MED.contains(x.medicine))
    //get the first order date ever for med1 for each patient
    val med1_min_date = med1.map(x => (x.patientID, x.date.getTime())).groupByKey.mapValues(_.toList).map { case (k, v) => (k, v.min) }.sortByKey()
    //get the first order date ever for med2 for each patient
    val med2_min_date = med2.map(x => (x.patientID, x.date.getTime())).groupByKey.mapValues(_.toList).map { case (k, v) => (k, v.min) }.sortByKey()

    //294 CASE!!!! join med1 and med2 min dates rdds (patientid, (med1_mindate, med2_mindate)) and subtract med1_mindate - med2_mindate and filter positive results for type2 medication precedes type1 medication
    val type2med_before_type1med = med1_min_date.join(med2_min_date).map { case (k, (vls, vrs)) => (k, (vls - vrs)) }.filter(x => x._2 > 0).map(x => x._1).collect().toSet
    //{OTHER} repeat and filer negative results for the opposite
    val type1med_before_type2med = med1_min_date.join(med2_min_date).map { case (k, (vls, vrs)) => (k, (vls - vrs)) }.filter(x => x._2 < 0).map(x => x._1).collect().toSet
    //CASES AGG
    val cases = (no_type1_med ++ no_type2_med ++ type2med_before_type1med)

    //CONTROL/////////////////////////////////////
    //patientID: String, date: java.sql.Date, testName: String, value: Double
    val lr = labResult.map(x => LabResult(x.patientID, x.date, x.testName.toLowerCase, x.value))

    //1823 @ yes to glucose
    val yes_to_glucose = lr.filter(x => x.testName.contains("glucose")).map(x => x.patientID).distinct.collect().toSet
    //1864 (OTHER) @ no_to_glucose
    val no_to_glucose = lr.filter(x => !yes_to_glucose.contains(x.patientID)).map(x => x.patientID).distinct.collect().toSet

    //870 (OTHER) Yes @ abnormal lab value
    val yes_to_abnormal_lab_value = lr.filter(x => x.testName == "hba1c").filter(x => x.value >= 6.0).map(x => x.patientID).distinct.union(
      lr.filter(x => x.testName == "hemoglobin a1c").filter(x => x.value >= 6.0).map(x => x.patientID).distinct).union(
        lr.filter(x => x.testName == "fasting glucose").filter(x => x.value >= 110.0).map(x => x.patientID).distinct).union(
          lr.filter(x => x.testName == "fasting blood glucose").filter(x => x.value >= 110.0).map(x => x.patientID).distinct).union(
            lr.filter(x => x.testName == "fasting plasma glucose").filter(x => x.value >= 110.0).map(x => x.patientID).distinct).union(
              lr.filter(x => x.testName == "glucose").filter(x => x.value > 110.0).map(x => x.patientID).distinct).union(
                lr.filter(x => x.testName == "glucose, serum").filter(x => x.value > 110.0).map(x => x.patientID).distinct).distinct.filter(x => yes_to_glucose.contains(x)).collect().toSet

    //953 NO @ abnormal lab value
    val no_abnormal_lab = lr.filter(x => yes_to_glucose.contains(x.patientID)).filter(x => !yes_to_abnormal_lab_value.contains(x.patientID)).map(x => x.patientID).distinct.collect().toSet

    //5 (OTHER) Yes @ diabetes milletes
    val yes_diabetes_milletes = diagnostic.filter {
      case x =>
        val pat = "250.*".r
        pat.pattern.matcher(x.code).matches
    }.map(x => x.patientID).distinct.filter(x => no_abnormal_lab.contains(x)).distinct.collect().toSet

    //948 CONTROL NO @ diabetes milletes
    val control = no_abnormal_lab.filterNot(yes_diabetes_milletes)

    //OTHER AGG
    val other = diagnostic.map(x => x.patientID).distinct.filter(x => (!cases.contains(x)) && (!control.contains(x)))

    /** Hard code the criteria */
    // val type1_dm_dx = Set("code1", "250.03")
    // val type1_dm_med = Set("med1", "insulin nph")
    // use the given criteria above like T1DM_DX, T2DM_DX, T1DM_MED, T2DM_MED and hard code DM_RELATED_DX criteria as well

    /** Find CASE Patients */
    val casePatients = sc.parallelize(cases.toSeq.map(x => (x, 1)))

    /** Find CONTROL Patients */
    val controlPatients = sc.parallelize(control.toSeq.map(x => (x, 2)))

    /** Find OTHER Patients */
    val others = other.map(x => (x, 3))

    /** Once you find patients for each group, make them as a single RDD[(String, Int)] */
    val phenotypeLabel = sc.union(casePatients, controlPatients, others)

    /** Return */
    phenotypeLabel
  }
}