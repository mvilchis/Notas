
#Notas Spark
## Aspectos generales


* Spark es un motor general para procesar grandes cantidades de datos, responsable de calendarizar, distribuir y monitorear aplicaciones que consisten en multiples tareas en multiples maquinas.

![](https://bytebucket.org/mvilchis/notas/raw/1e9d3788d73c4a0d6683ad5dabcc13c688dabab5/Spark/img/stack.jpg)

* El core abarca funcionalidades básicas para Spark, como calendarización de tareas, manejo de memorias, recuperación de fallos e interaccipon con los sistemas de almacenamiento, entre otros.

* Para permitir una máxima flexibilidad, Spark puede correr sobre varios manejadores de clusters, como Hadoop YARN, Apache Mesos o solo Spark con su Standalone Scheduler.

* Cada aplicación es un driver que lanza varias tareas paralelas al cluster. Este driver contiene la función ``` main ``` y define los datasets distribuidos y las tareas sobre estos. 
* Los drivers acceden a Spark a través de ** SparkContext ** que representa una conexión al cluster. Y cada driver maneja varios nodos llamados ejecutores (executors)

![](https://bitbucket.org/mvilchis/notas/raw/888c4d9478f434b9972dcf34e009ca278d20fac2/Spark/img/drivers.jpg)

## RDD

* RDD es una colección distribuida de objetos inmutables. Cada RDD es dividido en multiples particiones, las cuales pueden ser calculadas en diferentes nodos de los clusters. 
* Recordar que Spark es lazy, generando un mapa de las dependencias para optimizar (lineage graph)
* Cada RDD ofrece dos operaciones, transformaciones y acciones. Donde las transformaciones generan un nuevo RDD y las acciones generan un resultado basado en un RDD y puede que regrese el resultado al driver o que lo guarde.
* Todo RDD es calculado al vuelo, si se quiere guardar uno en memoria para consultarlo constantemente se usa ```persist()```
* Transformaciones. 
  (Para ver los resultados finalizar con ```rdd.collect().mkString(","))```). Sea:
   ```val rdd = sc.parallelize(List(1,2,3,3)); ```
  ```val rdd2 = sc.parallelize(List(1,4,5))```
  | Nombre de la funcion | Objetivo  | Ejemplo  | Resultado|
  | ------------- |:-------------| :-----|:----|
  |map()      | Aplica la funcion a cada elemento  | rdd.map(x =>x.to(3)) | {[1,2,3][2,3],[3],[3]}
  |flatMap()  | Map, rdd con el contenido de los iteradores | rdd.flatMap(x=>x.to(3)) | {1,2,3,2,3,3,3}
  |filter()  | rdd con los que cumplen | rdd.filter(x => x!=3) | {1,2}
  |distinct()  | rdd sin duplicados ** Costosa** | rdd.distinct() | {1,2,3}
  |sample( withReplacement,fraction, << seed>>)  | sample de rdd ** take sesgado** | rdd.sample(false,0.5) | //
  |union()| union con repeticion| rdd.union(rdd2) | {1,2,3,3,1,4,5}
  |intersection()| **Cosotosa**| rdd.intersection(rdd2) | {1}
  |subtract()| **Costosa**| rdd.subtract(rdd2) | {2,3,3}
  |cartesian()| | rdd.cartesian(rdd2) | //
* Acciones
  Sea:
  ```val rdd = sc.parallelize(List(1,2,3,3)); ```
  ``` ```
  | Nombre de la funcion | Objetivo  | Ejemplo  | Resultado|
  | ------------- |:-------------| :-----|:----|
  |collect() |Regresa todos los elementos de rdd | rdd.collect()) | {1,2,3,3}
  |count()   || rdd.count() | 4
  |countByValue()   || rdd.countByValue() | {(1,1), (2,1), (3,2)}
  |take(#)   |Intentara hacer el menor # de llamadas entre workers| rdd.take(2) | {1,2}
  |takeOrdered(#)(ordering)|| rdd.takeOrdered(2)(myOrdering)| {5,4}
  |takeSample(withReplacement,fraction, << seed>>)|| rdd.takeOrdered(2)(myOrdering)| {5,4}
  |top(#)   || rdd.top(1) | {1}
  |reduce() |Combina los elementos **Tiene que regresar el mismo tipo que el rdd**| rdd.reduce((x,y) => x+y) | 9
  |fold(zero)(function)|Combina los elementos dando valor inicial. ** Tiene que regresar el mismo tipo que el rdd**| rdd.fold(0)((x,y) => x+y) | 9
   |aggregate(zero)(seqOp)(combOp)|Similar a reduce, sin regresar el mismo tipo |rdd.aggregate((0,0)) ((x,y) => (x._1 + y, x._2 +1), (x,y)=>(x._1+y._1, x._2 + y._2) ) | (9,4)
   |foreach(function)   |Aplica la función a cada elemento, sin regresar valor| rdd.foreach(func) | Nada

## Ejemplos

* Hola mundo ```  ./bin/spark-shell --master local ```
```scala
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
val conf = new SparkConf().setAppName("Test") //.setMaster("local")
val sc = new SparkContext(conf)
// Uso de parallelize
val lines = sc.parallelize(List("Hola", "Mundo"))
// Uso comun
var lines = sc.textFile("Temporal.txt")
lines.count()
```

