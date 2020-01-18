/**
 *
 * students: please put your implementation in this file!
 */
package edu.gatech.cse6250.jaccard

import edu.gatech.cse6250.model._
import edu.gatech.cse6250.model.{ EdgeProperty, VertexProperty }
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

object Jaccard {

  def jaccardSimilarityOneVsAll(graph: Graph[VertexProperty, EdgeProperty], patientID: Long): List[Long] = {
    /**
     * Given a patient ID, compute the Jaccard similarity w.r.t. to all other patients.
     * Return a List of top 10 patient IDs ordered by the highest to the lowest similarity.
     * For ties, random order is okay. The given patientID should be excluded from the result.
     */

    //PatientIDs range from 2 to 1000 - all other unique IDs are not patients in the graph
    val PatientIdCutoff: Long = 1000

    //Get neighbors for each patientID
    val neighbors: RDD[(VertexId, Array[VertexId])] = graph.collectNeighborIds(EdgeDirection.Out)

    // Cache neighbors for multiple use
    neighbors.cache()

    //Get neighbors specifically for patient of interest
    val subject: Array[Long] = neighbors.filter(x => x._1.toLong == patientID).map(x => x._2).flatMap(x => x).collect()

    //Remove current patientID of interest and get data for everyone else
    val everyone_else: RDD[(VertexId, Array[VertexId])] = neighbors.filter(x => x._1.toLong != patientID).filter(x => x._1.toLong <= PatientIdCutoff)

    //calculate the jaccard and take top 10 and return list
    val jac = everyone_else.map(x => (x._1, jaccard(subject.toSet, x._2.toSet)))

    val ordered = jac.takeOrdered(10)(Ordering[Double].reverse.on(x => x._2))
    ordered.map(_._1.toLong).toList
  }

  def jaccardSimilarityAllPatients(graph: Graph[VertexProperty, EdgeProperty]): RDD[(Long, Long, Double)] = {
    /**
     * Given a patient, med, diag, lab graph, calculate pairwise similarity between all
     * patients. Return a RDD of (patient-1-id, patient-2-id, similarity) where
     * patient-1-id < patient-2-id to avoid duplications
     */

    /** Remove this placeholder and implement your code */
    val sc = graph.edges.sparkContext

    //Get neighbors for each patientID - unique ID up to 1000 still applies as in jaccardSimilarityOneVsAll
    val neighbors: RDD[(VertexId, Array[VertexId])] = graph.collectNeighborIds(EdgeDirection.Out) // returns VertexId, Array[VertexIds]
    val neighbors_patients = neighbors.filter(x => x._1.toLong <= 1000) // Filter all IDs for those <= 1000 so it is only patient IDs

    //Cartesian example from here http://homepage.cs.latrobe.edu.au/zhe/ZhenHeSparkRDDAPIExamples.html#cartesian
    //where cartesian of {(1,2), (3,4)} and {(5,6), (7,8)} = [( (1,2), (5,6) ) , ( (1,2), (7,8) ), ( (3,4), (5,6) ) , ( (3,4), (7,8) )]
    val neighbors_cartesian_product = neighbors_patients.cartesian(neighbors_patients) //returns cartesian product of the graph with itself

    val neighbors_cartesian_product_no_duplicates = neighbors_cartesian_product.filter(x => x._1._1 < x._2._1) //filters out duplicates per requirements in comment code

    val jac = neighbors_cartesian_product_no_duplicates.map(x => (x._1._1, x._2._1, jaccard(x._1._2.toSet, x._2._2.toSet))) // Calculate the jaccard
    jac.cache()
    jac

  }

  def jaccard[A](a: Set[A], b: Set[A]): Double = {
    /**
     * Helper function
     *
     * Given two sets, compute its Jaccard similarity and return its result.
     * If the union part is zero, then return 0.
     */

    /** Remove this placeholder and implement your code */
    if (a.isEmpty || b.isEmpty) {
      return 0.0
    } else {
      a.intersect(b).size / a.union(b).size.toDouble
    }
  }
}
