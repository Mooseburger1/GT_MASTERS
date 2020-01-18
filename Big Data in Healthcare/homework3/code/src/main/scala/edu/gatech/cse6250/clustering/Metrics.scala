/**
 * @author Hang Su <hangsu@gatech.edu>.
 */

package edu.gatech.cse6250.clustering

import org.apache.spark.rdd.RDD

object Metrics {
  /**
   * Given input RDD with tuples of assigned cluster id by clustering,
   * and corresponding real class. Calculate the purity of clustering.
   * Purity is defined as
   * \fract{1}{N}\sum_K max_j |w_k \cap c_j|
   * where N is the number of samples, K is number of clusters and j
   * is index of class. w_k denotes the set of samples in k-th cluster
   * and c_j denotes set of samples of class j.
   *
   * @param clusterAssignmentAndLabel RDD in the tuple format
   *                                  (assigned_cluster_id, class)
   * @return
   */
  def purity(clusterAssignmentAndLabel: RDD[(Int, Int)]): Double = {
    /**
     * TODO: Remove the placeholder and implement your code here
     */

    val total = clusterAssignmentAndLabel.count
    clusterAssignmentAndLabel.map(x => (x, 1)). //convert (cluster#, class) to ((cluster#, class), 1)
      reduceByKey((x, y) => x + y). //sum the unique instances of (cluster#, class)
      map(x => (x._1._1, (x._1._2, x._2))). //convert ((cluster#, class), #ofInstances) to (cluster#, (class, #ofInstances))
      groupByKey(). //group the cluster# together
      map { case (x, y) => (x, y.toList.maxBy(_._2)) }. //convert grouped cluster values to list and select max #of Instances in (class, #ofInstances)
      map(x => x._2._2). // select the max #ofInstance for each cluster
      sum / total //sum the result and divide by the number of observations

  }
}
