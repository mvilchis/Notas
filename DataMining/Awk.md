# AWK
## Conceptos generales
Awk es un lenguaje dentro de los comandos de linux que permite hacer busqueda sobre archivos o sobre unidades de texto para encontrar diversos patrones. Cuando una línea contiene algún patrón, awk realiza alguna acción definida por nosotros para esa línea.
La diferencia con otros programas es que awk trabaja orientado a líneas y no necesita cargar todo un archivo a memoria, en su lugar va procesando cada línea. Por ello puede ser una buena opción cuando queremos limpiar grandes archivos de texto. 

## Acciones básicas 

 * Ejecutar una rutina para el archivo _fileA_ y _fileB_. (Las comillas simples son necesarias, para decirle a awk que ahí está definida la rutina)

   `awk 'rutina_definida' fileA fileB ` 

 * Ejecutar una rutina almacenada en un archivo, para los archivos _fileA_ y _fileB_

   `awk -f program-file fileA fileB`

 * Dentro de las rutinas que awk acepta, es posible definir lo que se hará antes de comenzar a procesar cualquier línea, eso se realiza en la sección `BEGIN`. 

    `awk 'BEGIN {print "Hola mundo"}'`

 * Análogamente se puede definir una acción para cuando se terminen de procesar todas las líneas, esto en el bloque  `END`. Por ejemplo, imprimir el tamaño de la cadena más larga: 

    `awk 'BEGIN{max=0} {if (length($0) > max) max = length($0)} END {print max}' fileA `
 
   Resumiendo, el comando awk se ve de la siguiente manera: 
 
    `awk 'BEGIN{definicion_de_variables}{definicion_de_rutinas}END{acciones_al_terminar_de_leer}'`


 * Imprimir las líneas que contienen el patrón J. Hay que notar que en el área donde colocamos J, puede ir una expresión regular, con lo que podemos imprimir todas las líneas que cumplen con una expresión regular. 

    `awk '$0 ~ /J/' fileA`

    `awk '$0 ~/^a/' fileA` Imprime todas las líneas que comienzan con a.

 * En contraposición, para imprimir las líneas que no contienen el patrón J basta con hacer:

    `awk '$0 !~ /J/' fileA` 
 
 * Otro ejemplo con el if, imprimir las lineas con más de 80 caracteres.

    `awk 'length($0)>80' fileA`
 
 * Awk puede ser ligado a la salida de otros comandos a través de los pipes de linux:
 
    `ls -l | awk '{x += $5} END {print $5}'`Imprime el total de bytes de una carpeta

    `ls -l | awk  '$6== "Nov" {sum += $5} END {print $5}'`Imprime el tamaño de los archivos que se crearon en noviembre

## Formato de lectura de entrada
En los ejemplos de arriba hablamos de procesar línea por línea, es decir, que cada bloque procesado era definido por el inicio de la cadena hasta el salto de línea, sin embargo, awk permite cambiar ese funcionamiento a través de la variable: `RS` (Record Separator), donde se define que caracter usado como separador de línea, note que puede ser una expresion regular.
  Si nuestro archivo contiene:

  ```
       hola mundo esta es una
       prueba para mostrar como

       funciona el separador de registros
       usando doble enter en lugar de uno solo
  ```

  Y  nuestro comando es:

  `awk 'BEGIN{RS="\n\n"}{print length($0)}' fileA ` La salida será: 49 y 75

  Mientras que si el comando es:
  ` awk 'BEGIN{RS="\n"} {print length($0)}' fileA` La salida será: 23, 25, 0, 34 y 39.

En la sección anterior hemos utilizado `$0` para referirnos a toda la línea, esto es debido a que en awk `$0` se refiere a toda la línea, `$1` a la primera palabra (o campo), `$2` a la segunda palabra y así sucesivamente hasta `$NF` (Number of fields, variable definida en awk para el número total de palabras en una línea). Algo importante a mencionar es que awk también permite la modificación del separador de palabras o campos a traves de la variable `FS` (Field Separator), en donde se define que caracter o expresión regular es usado para separar las palabras:
  Si nuestro archivo contiene:

   ```
   hola,esto,es un,csv,simple
   ```

  Con awk podemos imprimir el tercer campo del csv:

  `awk 'BEGIN{FS=","}{print $3 $NF}' fileA`  Cuya salida será: "_es un_" y "_simple_"

  Otro separador comúnmente usado es `FS="[ \t\n]+"`

Hay ciertas acciones curiosas como :
  > Definir una variable por cada línea, llamada nboxes que contendrá el tercer campo, depués sobreescribir el tercer campo con lo que contiene dicho campo menos 10 en entero a imprimir el antiguo tercer campo y el nuevo tercer campo (el cambio en el  tercer campo solo es dentro de la rutina awk, no se modificará el archivo origen):
   `echo "ahora,usamos el numero,20, en el campo 3"| awk 'BEGIN{FS=","}{nboxes = $3; $3 = $3-10; print nboxes, $3}'` La salida será "_20_" y "_10_"



## Formato de lectura de salida:
* Analogó a las variables para definir una línea de entrada, podemos definir como se verá nuestra salida con `ORS` definimos el separador de las líneas de salida, por default \n, entonce si nuestro archivo A es:
   ```
      Hola mundo
      Adios mundo
   ```
   Y nuetro comando: `awk 'BEGIN{ORS="."} {print $0}'` La salida será  "_Hola mundo. Adios mundo._"

* Con `OFS` modificamos el separador de cada campo, por default espacio, entonces:

   `awk 'BEGIN {ORS="\n\n"; OFS = ";"} {print $1, $2}' fileA` Modifica el separador de campo y de registro

* Con `OFMT` se especifica el formato de impresión

   `awk 'BEGIN {OFMT = "%.0f";print 13.21, 12.42}'` Imprime sin punto decimal

* Y la función `printf` funciona como en C

   `awk 'BEGIN {msg="Hola mundo"; printf "%s \n", msg}'` Imprime Hola mundo, pero no hace uso del ORS ni del OFS

* Signo - define el ancho de un campo

   `awk '{printf "%-10s %s\n", $1, $2}' file` Imprime en formato tabla de ancho 10

* Redirección dentro de print

   `awk '{ print $2 > "archivo_a"; print $3 > "archivo_b"}' fileA`  Redirecciona a dos archivo con diferente contenido

## Expresiones

* Las variables pueden ser definidas dentro del programa o entre cada archivo 

    `awk '{print $n} n=4 fileA n=5 fileB'` Imprime 4 y 5

    `awk -v s=4 'BEGIN {print s}'` Uso de la bandera -v para definir una variable, analogo a: `awk 'BEGIN {s=4;print s}'` Ambos Imprime el valor 4

* El signo + convierte a numero

    `awk 'BEGIN{s="4.2"; printf "%d\n", +s+2}'` Convierte la cadena a numero

* Podemos usar or para patrones con "|" o "||":

    `awk '/foo|faa/ {print $0}' fileA`  Equivalente a:

    `awk '/foo/ || /faa/' fileA` Ambas imprimen las líneas con alguno de los patrones "_faa_" o "_foo_"
    
* Los patrones pueden ser definidos al vuelo, por ejemplo dependiendo de una variable de shell:

      > `export patron=,`

    `awk -v pat="$patron" '$0  ~ pat { nmatches++ } END { print "Total de lineas encontradas:", nmatches }' fileA`


* Awk cuneta con sentencias de control, if, while, for, continue y break.

     `awk '{ i = 1; while (i <= 3) { print $i; i++ } }' fileA`  Imprime los campos _$1_ _$2_ y _$3_

     `awk '{ for (i = 1; i <= 3; i++) print $i }'fileA` Analogo al caso de arriba

# Referencias
[Robbins, A.,Effective Awk Programming: Text Processing and Pattern Matching, 2001, O'Reilly Media, Incorporated](http://shop.oreilly.com/product/9780596000707.do)


