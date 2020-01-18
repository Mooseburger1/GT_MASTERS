/**
 * @author Hang Su <hangsu@gatech.edu>.
 */

package edu.gatech.cse6250.graphconstruct

import edu.gatech.cse6250.model._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

object GraphLoader {
  /**
   * Generate Bipartite Graph using RDDs
   *
   * @input: RDDs for Patient, LabResult, Medication, and Diagnostic
   * @return: Constructed Graph
   *
   */
  def load(patients: RDD[PatientProperty], labResults: RDD[LabResult],
    medications: RDD[Medication], diagnostics: RDD[Diagnostic]): Graph[VertexProperty, EdgeProperty] = {

    /** HINT: See Example of Making Patient Vertices Below */
    val sc = medications.sparkContext

    val vertices = sc.union(
      patients.map(patient => (patient.patientID.toLong, patient)).asInstanceOf[RDD[(VertexId, VertexProperty)]],

      diagnostics.map(x => (x.icd9code.hashCode.abs.toLong, DiagnosticProperty(x.icd9code))).asInstanceOf[RDD[(VertexId, VertexProperty)]],

      medications.map(x => (x.medicine.hashCode.abs.toLong, MedicationProperty(x.medicine))).asInstanceOf[RDD[(VertexId, VertexProperty)]],

      labResults.map(x => (x.labName.hashCode.abs.toLong, LabResultProperty(x.labName))).asInstanceOf[RDD[(VertexId, VertexProperty)]])

    /**
     * HINT: See Example of Making PatientPatient Edges Below
     *
     * This is just sample edges to give you an example.
     * You can remove this PatientPatient edges and make edges you really need
     */
    // case class PatientPatientEdgeProperty(someProperty: SampleEdgeProperty) extends EdgeProperty
    // val edgePatientPatient: RDD[Edge[EdgeProperty]] = patients
    //   .map({ p =>
    //     Edge(p.patientID.toLong, p.patientID.toLong, SampleEdgeProperty("sample").asInstanceOf[EdgeProperty])
    //   })
    val edgePatientDiagnostic: RDD[Edge[EdgeProperty]] = diagnostics.groupBy(x => (x.patientID, x.icd9code)).mapValues(_.toList).map { case (id, diagnostic) => diagnostic.sortBy(_.date).last }.map(x => Edge(x.patientID.toLong, x.icd9code.hashCode().abs, PatientDiagnosticEdgeProperty(x)))

    val edgeDiagnosticPatient: RDD[Edge[EdgeProperty]] = diagnostics.groupBy(x => (x.patientID, x.icd9code)).mapValues(_.toList).map { case (id, diagnostic) => diagnostic.sortBy(_.date).last }.map(x => Edge(x.icd9code.hashCode().abs, x.patientID.toLong, PatientDiagnosticEdgeProperty(x)))

    val edgePatientMedication: RDD[Edge[EdgeProperty]] = medications.groupBy(x => (x.patientID, x.medicine)).mapValues(_.toList).map { case (id, medicine) => medicine.sortBy(_.date).last }.map(x => Edge(x.patientID.toLong, x.medicine.hashCode().abs, PatientMedicationEdgeProperty(x)))

    val edgeMedicationPatient: RDD[Edge[EdgeProperty]] = medications.groupBy(x => (x.patientID, x.medicine)).mapValues(_.toList).map { case (id, medicine) => medicine.sortBy(_.date).last }.map(x => Edge(x.medicine.hashCode().abs, x.patientID.toLong, PatientMedicationEdgeProperty(x)))

    val edgePatientLabResult: RDD[Edge[EdgeProperty]] = labResults.groupBy(x => (x.patientID, x.labName)).mapValues(_.toList).map { case (id, labName) => labName.sortBy(_.date).last }.map(x => Edge(x.patientID.toLong, x.labName.hashCode().abs, PatientLabEdgeProperty(x)))

    val edgeLabResultPatient: RDD[Edge[EdgeProperty]] = labResults.groupBy(x => (x.patientID, x.labName)).mapValues(_.toList).map { case (id, labName) => labName.sortBy(_.date).last }.map(x => Edge(x.labName.hashCode().abs, x.patientID.toLong, PatientLabEdgeProperty(x)))

    val edges = sc.union(
      edgePatientDiagnostic,
      edgeDiagnosticPatient,
      edgePatientMedication,
      edgeMedicationPatient,
      edgePatientLabResult,
      edgeLabResultPatient)

    // Making Graph
    val graph: Graph[VertexProperty, EdgeProperty] = Graph(vertices, edges)

    graph
  }
}
