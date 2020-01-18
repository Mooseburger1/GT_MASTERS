---
---
# Spark Gotchas

::: tip Learning Objectives

- Understanding runtime pitfalls that may arise

:::

::: danger

This doc is required to be updated.

:::

## Overview

Spark has a handful of gotchas that exist while running in any clustered environment (standalone, K8s, Mesos, Yarn) which can cause runtime issues
late in the execution of a job depending how it is coded.  It is better to know of these pitfalls ahead of time as the scala compiler will not alert you of them as syntactically your code may be perfect.

__Member Serialization__

The following is a remarkably unrealistic example as _why would you not just create the variable in the main?_.  
However, there are instances when sub-classing that you may want to override values that are a member
of the base.  In that, it should be known serialization issues can arise.  Spark serializes entire objects with their
initial state to workers but deal with implicits differently -- it's always better to declare and initialize variables that will *not* 
change locally in the call stack from _main()_.  
*Note:* Spark uses closures to defined execution strategies but these closures do not operate in the same fashion as in Scala itself.

```scala
case class Test(x: String)

object ObjectMemberIssue {

	// When foo is accessed via a map operation (transformation) on a worker
	// it will be null
	var foo: String = null

	def main(args: Array[String]) : Unit = {

		val session = SparkSession.builder().appName("foo").getOrCreate()

		foo = "bar"

		import session.implicits._

		val dsOfStrings = (1 to 100).map(new Test(_.toString)).toDS()

		// This will produce a NullPointerException on the worker which will
		// cause it to die if the job is not running in local mode in the same JVM
		// as the driver.  In cluster mode (standalone or otherwise) MemberIssue
		// will be serialized in its default state to the worker causing 
		// the access of foo and the append to x to produce the NPE
		dsOfStrings.map(i => i.copy(i.x ++ foo)).collect().foreach(println)
	}
}
```


An alternative solution is to use an implicit val:

```scala

object ObjectMemberIssueSolution {

	var foo: String = null

	// implicits are searched for and are contexually bound for serialization
	// at runtime time but are intrinsically value structures and will not change
	def append(base: String)(implicit val s: String) = base ++ s

	def main(args: Array[String]) : Unit = {

		val session = SparkSession.builder().appName("foo").getOrCreate()

		foo = "bar"

		// implicits are contexual serialized 
		// especially when passed through another method which forces it to be bound
		// in the Spark serializer as the scala compiler guarantees implicits are bound
		// at compile time based upon references
		implicit val _foo = foo

		import session.implicits._

		val dsOfStrings = (1 to 100).map(new Test(_.toString)).toDS()

		// This will produce a NullPointerException on the worker which will
		// cause it to die if the job is not running in local mode in the same JVM
		// as the driver.  In cluster mode (standalone or otherwise) MemberIssue
		// will be serialized in its default state to the worker but b/c the 
		// _foo is an implicit val prior to access subsequent invocations of append will not
		// cause issue.
		//
		// The implicit does not need to be passed as it is automagically wired in via 
		// 
		dsOfStrings.map(i => i.copy(append(i.x)).collect().foreach(println)
	}
}
```

__Accumulators__
* are write only on the worker (_unless running in local mode in the same JVM_)
* only the driver can read a value of an accumulator or reset the value of the accumlator

__Broadcast variables__
* are meant to serialize large amounts of data to each worker for fast access.  This data should not change frequently and be relatively static.
* data can be reset via _unpersist(blocking=True)_ which will force each worker to delete its cached version of the broadcast variable *but* the broadcast
	will stay in memory for the remaining stage execution.  Upon the next stage execution on the worker the updated state of the broadcast variable will
	be re-transmitted.
** an elegant way to handle the eviction of Broadcast data (or accessing of accumulators) is by registering a _SparkListener_ implementation with the _SparkSession_
