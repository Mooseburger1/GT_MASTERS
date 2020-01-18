package edu.gatech.cse6250.randomwalk

import edu.gatech.cse6250.model.{ PatientProperty, EdgeProperty, VertexProperty }
import org.apache.spark.graphx._

object RandomWalk {

  def randomWalkOneVsAll(graph: Graph[VertexProperty, EdgeProperty], patientID: Long, numIter: Int = 100, alpha: Double = 0.15): List[Long] = {
    /**
     * Given a patient ID, compute the random walk probability w.r.t. to all other patients.
     * Return a List of patient IDs ordered by the highest to the lowest similarity.
     * For ties, random order is okay
     */

    /** Remove this placeholder and implement your code */

    // First transform the input row node a into a (k+n) x 1 query vector qa with 1 in the a-th row
    // and 0 otherwise

    // Second compute the (k + n) x 1 steady-state probability vector "ua" over all the nodes in G.

    // Last, extract the probabilities of the row nodeas as the score vectors

    // "ua" = (1 -c)Pa"ua" + cqa
    // where Pa is already the column normalized
    var epoch = 0
    // {outerjoin} Update Vertices to (id, outdegrees)) - Code was derived from example code seen at http://ampcamp.berkeley.edu/5/exercises/graph-analytics-with-graphx.html
    // {mapTriplets} Use the outdegrees to normalize weight vectors => normalized == 1 / outdegrees for each node
    // {mapVertices} Reset graph vertices to (id, alpha) - only patientID should be equal to alpha, all other IDs should be alpha=0
    var InitialGraph: Graph[Double, Double] = graph.outerJoinVertices(graph.outDegrees) { (id, attr, outdegree) => outdegree.getOrElse(0) }.mapTriplets(x => 1.0 / x.srcAttr, TripletFields.Src).mapVertices { (id, attr) => if (id == patientID) alpha else 0.0 }
    //returns graph with:
    // Vertices => (id, alpha)
    // Edges => (src, dest, normalized weight)

    while (epoch < numIter) {

      //cache InitialGraph since it will be used multiple times per epoch
      //InitialGraph.cache()

      // Multiply vertices alpha by each edge weight and reduce by addition
      // Faciliation for this was derived from https://medium.com/@gangareddy619/advanced-graph-algorithms-in-spark-using-graphx-aggregated-messages-and-collective-communication-f3396c7be4aa
      val ranks = InitialGraph.aggregateMessages[Double](
        x => x.sendToDst(x.srcAttr * x.attr), //map function
        _ + _, TripletFields.Src) //reduce function

      //Update Initial Graph with new probabilites - replace alpha with new ranks calculated above
      InitialGraph = InitialGraph.joinVertices(ranks) { (id, rank, probs) =>
        if (id == patientID)
          alpha + (1.0 - alpha) * probs
        else
          (1.0 - alpha) * probs
      }

      epoch += 1
    }
    //return top 10
    val winnerwinnerchickendinner = InitialGraph.vertices.filter(x => x._1 <= 1000).takeOrdered(11)(Ordering[Double].reverse.on(x => x._2)).map(_._1)
    winnerwinnerchickendinner.slice(1, winnerwinnerchickendinner.length).toList
  }
}
