---
sidebarDepth: 2
---
# Scala Introduction

::: tip Learning Objectives

- Provide more details of scala language

:::

## Basic Gramma

### Start using Scala

After installed [scala](https://www.scala-lang.org/download/), you can type `scala` in command line and get result as follow:

```scala
$ scala
Welcome to Scala version 2.11.7
Type in expressions to have them evaluated.
Type :help for more information.

scala> println("Hello, World!")
Hello, World!
```

The synopsis of a varialbe is:

```scala
scala> val i:String = "abc"
i: String = abc
```

- val means it it is immutable variable, you can use "var" to define a mutable variable
- i is the name of this variable
- String is the type of this string, it can be omitted here
- "abc" is the value of this variable

Define a function:

```scala
scala> def foo(v0:Int, v1:Int):Int = {
     |     println(v0 max v1)
     |     v0 + v1
     | }
foo: (v0: Int, v1: Int)Int

scala> foo(1, 2)
2
res0: Int = 3
```

Define a class:

```scala
scala> class Foo(a:String, b:Int) {
     |     def length = a.length
     | }
defined class Foo

scala> val foo:Foo = new Foo("Hello, World!", 3)
foo: Foo = Foo@6438a396

scala> println(foo.length)
13
```

Define a case class:

```scala
scala> case class Foo(a:String, b:Int)
defined class Foo

scala> val foo:Foo = Foo(a = "Hello, World!", b = 3)
foo: Foo = Foo(Hello, World!,3)

scala> println(foo.a)
Hello, World!
```

[Differences between case class and class](http://stackoverflow.com/questions/2312881/what-is-the-difference-between-scalas-case-class-and-class)

Define an Object

```scala
scala> object Foo {
     |     def greeting() {
     |         println("Greeting from Foo")
     |     }
     | }
defined object Foo

scala> Foo.greeting()
Greeting from Foo
```

Functions/variables in Object is similar to the static function and variable in Java.

What is ought to be highligted is the use of "apply". SomeObject.apply(v:Int) equals SomeObject(v:Int)

```scala
scala> :paste
// Entering paste mode (ctrl-D to finish)

case class Foo(a:String, b:Int)
object Foo {
	def apply(a:String): Foo =
		Foo(a, a.length)
}

// Exiting paste mode, now interpreting.

defined class Foo
defined object Foo

scala> val foo = Foo("Hello, World!")
foo: Foo = Foo(Hello, World!,13)
```

Finally, we should know the usage of code block.

We can create a code block anywhere, and the last line is the result of this block.

For example,

```scala
def foo(i:Int) = {
	println(s"value: $i")
	i * 2
}

val newList = List[Int](1, 2, 3).map(i => foo(i))
```

We can use the follow lines instead:

```scala
val newList = List[Int](1, 2, 3).map(i => {
    println(s"value: $i")
	i * 2
})
```

A better practice here is:

```scala
val newList = List[Int](1, 2, 3).map{i =>
    println(s"value: $i")
	i * 2
}
```

## Case Study of some Common Types

### Option, Some, None

We can use `null` in Scala as null pointer, but it is not recommended. We are supposed to use `Option[SomeType]` to indicate this variable is optional.

We can assueme every variable without `Option` are not null pointer if we are not calling java code. This help us reduce a lot of code.

If we wanna to get a variable with Option, here are two method

```scala
val oi = Option(1)
val i = oi match {
	case Some(ri) => ri
	case None => -1
}
println(i)
```

Besides, we can also use method "isDefined/isEmpty".

```scala
val oi = Option(1)
if(oi.isDefined) {
	println(s"oi: ${oi.get}")
} else {
	println("oi is empty")
}
```

What should be highlighted is `Option(null)` returns `None`, 
but `Some(null)` is `Some(null)` which is not equals `None`.

`match` is a useful reserved words, we can use it in various of situations 

Firstly, we can use it as "switch" & "case" in some other programming languages.

```scala
true match {
    case true => println("true")
    case false => println("false")
}
```

Secondly, we can find it by the type of the data, 

```scala
case class A(i:Int,j:Double)
case class B(a:A, k:Double)
val data = B(A(1,2.0),3.14)
data match {
    case B(A(_,v),_) =>
        println(s"required value: $v")
    case _ =>
        println("match failed")
}
```

Given a case class B, but we only wish to retrievee the value B.a.j, we can use "_" as placeholder.

### Common methods in List, Array, Set, and so on

In scala, we always transfer the List( Array, Set, Map etc.) from one status to another status. the methods of 

- **toList**, **toArray**, **toSet** -- convert each other

- **par** -- Parallelize List, Array and Map, the result of `Seq[Int]().par` is `ParSeq[Int]`, you will able to process each element in parallel when you are using foreach, map  etc., and unable to call "sort" before you are using "toList".

- **distinct** -- Removes duplicate elements

- **foreach** -- Process each element and return nothing

```scala
List[Int](1,2,3).foreach{ i =>
	println(i)
}
```

It wil print 1, 2, 3 in order

```scala
List[Int](1,2,3).par.foreach{ i =>
	println(i)
}
```

It will print 1, 2, 3, but the order is not guaranteed.


- **map** -- Process each element and construct a List using return value

```scala
List[Int](1,2,3).map{ i => i + 1}
```

It will return `List[Int](2,3,4)`

The result of `List[A]().map(some-oper-return-type-B)`  is `List[B]`, while the result of `Array[A]().map` map is `Array[B]`.

- **flatten** -- The flatten method takes a list of lists and flattens it out to a single list:

```scala
scala> List[List[Int]](List(1,2),List(3,4)).flatten
res1: List[Int] = List(1, 2, 3, 4)

scala> List[Option[Integer]](Some(1),Some[Integer](null),Some(2),None,Some(3)).flatten
res2: List[Integer] = List(1, null, 2, 3)
```

- **flatMap** -- The flatMap is similar to map, but it takes a function returning a list of elements as its right operand. It applies the function to each list element and returns the concatenation of all function results.
The result equals to map + flatten

- **collect** -- The iterator obtained from applying the partial function to every element in it for which it is defined and collecting the results.

```scala
scala> List(1,2,3.4,"str") collect {
     |   case i:Int => (i * 2).toString
     |   case f:Double => f.toString
     | }
res0: List[String] = List(2, 4, 3.4)
```

The function match elements in Int and Double, process them and return the value, but ignore string elements.

- **filter** -- Filter this list

```scala
scala> List(1,2,3).filter(_ % 2 == 0)
res1: List[Int] = List(2)
```

- **filterNot** -- Similar to filter

```scala
scala> List(1,2,3).filterNot(_ % 2 == 0)
res2: List[Int] = List(1, 3)
```

- **forall** -- Return true if **All** elements are return true by the partial function. It will immediately return once one element returns false, and ignore the rest elements.

```scala
scala> List(2,1,0,-1).forall{ i =>
     |   val res = i > 0
     |   println(s"$i > 0? $res")
     |   res
     | }
2 > 0? true
1 > 0? true
0 > 0? false
res0: Boolean = false
```

- **exists** -- Return true if there are at least **One** element returns true.

```scala
scala> List(2,1,0,-1).exists{ i =>
     |   val res = i <= 0
     |   println(s"$i <= 0? $res")
     |   res
     | }
2 <= 0? false
1 <= 0? false
0 <= 0? true
res2: Boolean = true
```

- **find** -- Return the first element returns true by the partial function. Return None if no elemet found.

```scala
scala> List(2,1,0,-1).find{ i =>
     |   val res = i <= 0
     |   println(s"$i <= 0? $res")
     |   res
     | }
2 <= 0? false
1 <= 0? false
0 <= 0? true
res3: Option[Int] = Some(0)
```

- **sortWith** -- sort the elements

```scala
scala> List(1,3,2).sortWith((leftOne,rightOne) => leftOne > rightOne)
res5: List[Int] = List(3, 2, 1)
```

- **zipWithIndex** --

```scala
List("a","b").zipWithIndex.foreach{ kv:(String,Int) => println(s"k:${kv._1}, v:${kv._2}")}
```

It will rebuild a List with index

```
k:a, v:0
k:b, v:1
```


- **for** - Scala's keyword `for` can be used in various of situations.

Basically,

```scala
for{
  i <- List(1,2,3)
} yield (i,i+1)
```

It equals:

```scala
List(1,2,3).map(i => (i, i+1))
```

Besides,

```scala
for{
  i <- List(1,2,3)
  j <- List(4,5,6)
} yield (i,j)
```

We will get the cartesian product of  `List(1,2,3)` and `List(4,5,6)`: `List((1,4), (1,5), (1,6), (2,4), (2,5), (2,6), (3,4), (3,5), (3,6))`

We can add a filter in condition:

```scala
for{
  i <- List(1,2,3)
  if i != 1
  j <- List(4,5,6)
  if i * j % 2 == 1
} yield (i,j)
```

the result is : `List((3,5))`

Another usage of for is as follow:

Let's define variables as follow:
```
val a = Some(1)
val b = Some(2)
val c = Some(3)
```

We can execute like this:

```scala
for {
	i <- a
	j <- b
	k <- c
	r <- {
		println(s"i: $i, j:$i, k:$k")
		Some(i * j * k)
	}
} yield r
```

The response is:

```scala
i: 1, j:1, k:3
res9: Option[Int] = Some(6)
```

Let's define b as None:

```scala
scala> val b:Option[Int] = None
b: Option[Int] = None

scala> for {
     |   i <- a
     |   j <- b
     |   k <- c
     |   r <- {
     |           println(s"i: $i, j:$i, k:$k")
     |           Some(i * j * k)
     |   }
     | } yield r
res14: Option[Int] = None
```

- **while** - Similar to while in java

```scala
var i = 0
while ({
	i = i + 1
	i < 1000
}){
	// body of while
	println(s"i: $i")
}
```

- **to**, **until** — (1 to 10) will generate a Seq, with the content of (1,2,3,4…10), (0 until 10) will generate a sequence from 0 to 9. With some test, (0 until 1000).map(xxx) appears to be slower than `var i=0; while( i < 1000) { i += 1; sth. else}`, but if the body of map is pretty heavy, this cost can be ignored.

- **headOption** - Get the head of one list, return None if this list is empty

- **head** - Get the head of one list, throw exception if this list is empty

- **take** -- Get first at most N elements. (from left to right)

```scala
scala> List(1,2,3).take(2)
res0: List[Int] = List(1, 2)

scala> List(1,2).take(3)
res1: List[Int] = List(1, 2)

```

- **drop** --  Drop first at most N elements.

```scala
scala> List(1,2,3).drop(2)
res2: List[Int] = List(3)

scala> List(1,2).drop(3)
res3: List[Int] = List()
```

`dropRight` will drop elements from right to left.

- **slice** -- Return list in `[start-offset, end-offset)`

```scala
scala> List(1,2,3).slice(1,2)
res7: List[Int] = List(2)

scala> List(1,2,3).slice(2,2)
res8: List[Int] = List()
```

```scala
val offset = 1
val size = 3
List(1,2,3,4,5).slice(offset, size + offset)
```

If the end-offset is greater than the length of this list, it will not throw exception.


- **splitAt** -- Split this list into two from offset i

```scala
scala> List(1,2,3).splitAt(1)
res10: (List[Int], List[Int]) = (List(1),List(2, 3))
```

- **groupBy** -- Partitions a list into a map of collections according to a discriminator function

```scala
scala> List(1,2,3).groupBy(i => if(i % 2 == 0) "even" else "odd" )
res11: scala.collection.immutable.Map[String,List[Int]] = Map(odd -> List(1, 3), even -> List(2))
```

- **partition** -- Splits a list into a pair of collections; one with elements that satisfy the predicate, the other with elements that do not, giving the pair of collections (xs filter p, xs.filterNot p).

```scala
scala> List(1,2,3).partition(_ % 2 == 0)
res12: (List[Int], List[Int]) = (List(2),List(1, 3))
```

- **grouped** -- The grouped method chunks its elements into increments.

```scala
scala> List(1,2,3,4,5).grouped(2)
res13: Iterator[List[Int]] = Iterator(List(1, 2), List(3, 4), List(5))
```

You can visit [this PDF](https://www.scala-lang.org/docu/files/ScalaByExample.pdf) for an official guide.

We also highly recomended to read the book [Programming in Scala](https://www.amazon.com/dp/B004Z1FTXS) for more detail instruction.
