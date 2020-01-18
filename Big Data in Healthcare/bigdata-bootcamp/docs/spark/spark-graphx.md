---
---
# Spark GraphX

::: tip Learning Objectives

- Understand composition of a graph in Spark GraphX.
- Being able to create a graph.
- Being able to use the built-in graph algorithm.

:::

In this section we begin by creating a graph with patient and diagnostic codes. Later we will show how to run graph algorithms on the the graph you will create.

## Basic concept

Spark GraphX abstracts a graph as a concept named __Property Graph__, which means that each edge and vertex is associated with some properties. The `Graph` class has the following definition

```scala
class Graph[VD, ED] {
  val vertices: VertexRDD[VD]
  val edges: EdgeRDD[ED]
}
```

Where `VD` and `ED` define property types of each vertex and edge respectively. We can regard `VertexRDD[VD]` as RDD of `(VertexID, VD)` tuple and `EdgeRDD[ED]` as RDD of `(VertexID, VertexID, ED)`.

## Graph construction

Let's create a graph of patients and diagnostic codes. For each patient we can assign its patient id as vertex property, and for each diagnostic code, we will use the code as vertex property. For the edge between patient and diagnostic code, we will use number of times the patient is diagnosed with given disease as edge property.

### Define class

Let's first define  necessary data structure and import

```scala
import org.apache.spark.SparkContext._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

abstract class VertexProperty extends Serializable

case class PatientProperty(patientId: String) extends VertexProperty

case class DiagnosticProperty(icd9code: String) extends VertexProperty

case class PatientEvent(patientId: String, eventName: String, date: Int, value: Double)
```

### Load raw data

Load patient event data and filter out diagnostic related events only

```scala
val allEvents = sc.textFile("data/").
  map(_.split(",")).
  map(splits => PatientEvent(splits(0), splits(1), splits(2).toInt, splits(3).toDouble))

// get and cache diagnosticEvents as we will reuse
val diagnosticEvents = allEvents.
  filter(_.eventName.startsWith("DIAG")).cache()
```

### Create vertex

#### Patient vertex

Let's create patient vertex

```scala
// create patient vertex
val patientVertexIdRDD = diagnosticEvents.
  map(_.patientId).
  distinct.      // get distinct patient ids
  zipWithIndex     // assign an index as vertex id

val patient2VertexId = patientVertexIdRDD.collect.toMap
val patientVertex = patientVertexIdRDD.
  map{case(patientId, index) => (index, PatientProperty(patientId))}.
  asInstanceOf[RDD[(VertexId, VertexProperty)]]
```

In order to use the newly created vertex id, we finally `collect` all the patient to `VertrexID` mapping.

::: warning

Theoretically, collecting RDD to driver is not an efficient practice. One can obtain uniqueness of ID by calculating ID directly with a Hash.

:::

#### Diagnostic code vertex

Similar to patient vertex, we can create diagnostic code vertex with

```scala
// create diagnostic code vertex
val startIndex = patient2VertexId.size
val diagnosticVertexIdRDD = diagnosticEvents.
  map(_.eventName).
  distinct.
  zipWithIndex.
  map{case(icd9code, zeroBasedIndex) =>
    (icd9code, zeroBasedIndex + startIndex)} // make sure no conflict with patient vertex id

val diagnostic2VertexId = diagnosticVertexIdRDD.collect.toMap

val diagnosticVertex = diagnosticVertexIdRDD.
  map{case(icd9code, index) => (index, DiagnosticProperty(icd9code))}.
  asInstanceOf[RDD[(VertexId, VertexProperty)]]
```

Here we assign vertex id by adding the result of `zipWithIndex` with an offset obtained from previous patient vertex to avoid ID confliction between patient and diagnostic code.

### Create edge

In order to create edge, we will need to know vertext id of vertices we just created.

```scala
val bcPatient2VertexId = sc.broadcast(patient2VertexId)
val bcDiagnostic2VertexId = sc.broadcast(diagnostic2VertexId)

val edges = diagnosticEvents.
  map(event => ((event.patientId, event.eventName), 1)).
  reduceByKey(_ + _).
  map{case((patientId, icd9code), count) => (patientId, icd9code, count)}.
  map{case(patientId, icd9code, count) => Edge(
    bcPatient2VertexId.value(patientId), // src id
    bcDiagnostic2VertexId.value(icd9code), // target id
    count // edge property
  )}
```

We first broadcast patient and diagnostic code to vertext id mapping. Broadcast can avoid unnecessary copy in distributed setting thus will be more effecient. Then we count occurrence of `(patient-id, icd-9-code)` pairs with `map` and `reduceByKey`, finally we translate them to proper `VertexID`.

### Assemble vertex and edge

We will need to put vertices and edges together to create the graph

```scala
val vertices = sc.union(patientVertex, diagnosticVertex)
val graph = Graph(vertices, edges)
```

## Graph operation

Given the graph we created, we can run some basic graph operations.

### Connected components

[Connected component][connected-component-wiki] can help find disconnected subgraphs. GraphX provides the API to get connected components as below

```scala
val connectedComponents = graph.connectedComponents
```

The return result is a graph and assigned components of original graph is stored as `VertexProperty`. For example

```scala
scala> connectedComponents.vertices.take(5)
Array[(org.apache.spark.graphx.VertexId, org.apache.spark.graphx.VertexId)] = 
Array((2556,0), (1260,0), (1410,0), (324,0), (180,0))
```

The first element of the tuple is `VertexID` identical to original graph. The second element in the tuple is `connected component` represented by the lowest-numbered `VertexID` in that component. In above example, five vertices belong to same component.

We can easily get number of connected components using operations on RDD as below.

```scala
scala> connectedComponents.vertices.map(_._2).distinct.collect
Array[org.apache.spark.graphx.VertexId] = Array(0, 169, 239)
```

### Degree

The property graph abstraction of GraphX is a directed graph. It provides computation of in-dgree, out-degree and total degree. For example, we can get degrees as

```scala
val inDegrees = graph.inDegrees
val outDegrees = graph.outDegrees
val totalDegrees = graph.degrees
```

### PageRank

GraphX also provides implementation of the famous [PageRank] algorithm, which can compute the 'importance' of a vertex. The graph we generated above is a bipartite graph and not suitable for PageRank. To gve an example of PageRank, we randomly generate a graph and run fixed iteration of PageRank algorithm on it.

```scala
import org.apache.spark.graphx.util.GraphGenerators


val randomGraph:Graph[Long, Int] = 
   GraphGenerators.logNormalGraph(sc, numVertices = 100)


val pagerank = randomGraph.staticPageRank(20)
```

Or, we can run PageRank until converge with tolerance as `0.01` using `randomGraph.pageRank(0.01)`

## Application

Next, we show some how we can ultilize the graph operations to solve some practical problems in the healthcare domain.

### Explore comorbidities

[Comorbidity] is additional disorders co-occuring with primary disease. We know all the case patients have heart failure, we can explore possible comorbidities as below (see comments for more explaination)

```scala
// get all the case patients
val casePatients = allEvents.
  filter(event => event.eventName == "heartfailure" && event.value == 1.0).
  map(_.patientId).
  collect.
  toSet

// broadcast
val scCasePatients = sc.broadcast(casePatients)

//filter the graph with subGraph operation
val filteredGraph = graph.subgraph(vpred = {case(id, attr) =>
    val isPatient = attr.isInstanceOf[PatientProperty]
    val patient = if(isPatient) attr.asInstanceOf[PatientProperty] else null
    // return true iff. isn't patient or is case patient
    !isPatient || (scCasePatients.value contains patient.patientId)
  })

//calculate indegrees and get top vertices
val top5ComorbidityVertices = filteredGraph.inDegrees.
    takeOrdered(5)(scala.Ordering.by(-_._2))
```

We have

```scala
top5ComorbidityVertices: Array[(org.apache.spark.graphx.VertexId, Int)] = Array((3129,86), (335,63), (857,58), (2048,49), (669,48))
```

And we can check the vertex of index 3129 in original graph is

```scala
scala> graph.vertices.filter(_._1 == 3129).collect
Array[(org.apache.spark.graphx.VertexId, VertexProperty)] = 
Array((3129,DiagnosticProperty(DIAG4019)))
```

The 4019 code correponds to [Hypertension](http://www.hipaaspace.com/Medical_Billing/Coding/ICD-9/Diagnosis/4019), which is reasonable.

### Similar patients

Given a patient diagnostic graph, we can also find similar patients. One of the most straightforward approach is shortest path on the graph.

```scala
val sssp = graph.
  mapVertices((id, _) => if (id == 0L) 0.0 else Double.PositiveInfinity).
  pregel(Double.PositiveInfinity)(
    (id, dist, newDist) => math.min(dist, newDist), // Vertex Program
    triplet => {  // Send Message
      var msg: Iterator[(org.apache.spark.graphx.VertexId, Double)] = Iterator.empty
      if (triplet.srcAttr + 1 < triplet.dstAttr) {
        msg = msg ++ Iterator((triplet.dstId, triplet.srcAttr + 1))
      }

      if (triplet.dstAttr + 1 < triplet.srcAttr) {
        msg = msg ++ Iterator((triplet.srcId, triplet.dstAttr + 1))
      }
      println(msg)
      msg
    },
    (a,b) => math.min(a,b) // Merge Message
  )

// get top 5 most similar
sssp.vertices.filter(_._2 < Double.PositiveInfinity).
    filter(_._1 < 300).
    takeOrdered(5)(scala.Ordering.by(-_._2))
```

[Comorbidity]: http://en.wikipedia.org/wiki/Comorbidity
[pagerank]: http://en.wikipedia.org/wiki/PageRank
[connected-component-wiki]: https://en.wikipedia.org/wiki/Connected_component_(graph_theory)
