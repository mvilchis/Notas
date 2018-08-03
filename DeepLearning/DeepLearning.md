#Notas Deep Learning
##Definiciones generales
* Recordar que el objetivo es encontrar la función que logra clasificar correctamente cada entrada.
* Funciones de activación: Se usan funciones no lineales para poder aprender funciones no lineales.
* Parametrización: Proceso de definir que parametros son necesarios para un modelo dado.
* Función de perdida: Cuantifica que tan bien la clase de salida se apega a la verdadera clase. (Buscamos minimizar dicha función)
* Función de Scoring: Esta función acepta los datos como entrada y los mapea a una etiqueta de clase. 
  Ejemplo: 
  <a href="https://www.codecogs.com/eqnedit.php?latex=f(x_i,&space;W,b)&space;=&space;Wx_i&plus;b" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x_i,&space;W,b)&space;=&space;Wx_i&plus;b" title="f(x_i, W,b) = Wx_i+b" /></a>
Donde: ```W = [K x D]```, ```x_i = [D x 1]``` y ```b = [K x 1] ```. Siendo K el número de clases para clasificar.
* Bias: Permite recorrer o transladar nuestra función de escoring en una u otra dirección sin modificar la matriz de pesos.

## Función de perdida
Comúnmente es común usar funciones *hinge* para *cross-entropy loss* y *softmax* en el contexto de deep learning y redes convolucionales.
* Multi-class svm loss
	Agregando la columna de bias a la matriz de pesos, sea:
	<a href="https://www.codecogs.com/eqnedit.php?latex=f(x_i,&space;W,b)&space;=&space;Wx_i&plus;b" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s = f(x_i,&space;W)&space;=&space;Wx_i" /></a>
	Dado el punto *i-esimo*, el score predicho de la clase *jth* queda definido como:
	<a href="https://www.codecogs.com/eqnedit.php?latex=f(x_i,&space;W,b)&space;=&space;Wx_i&plus;b" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s_j = f(x_i,&space;W)_j" /></a>

	De aquí obtenemos la función *hinge loss function* (sumando las clasificaciones incorrectas de cada clase y comparandola con la salida de la función score):
	<a href="https://www.codecogs.com/eqnedit.php?latex=L_i=&space;\sum_{j\neq&space;y_i}&space;max(0,&space;s_j-s_y_i&plus;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?L_i=&space;\sum_{j\neq&space;y_i}&space;max(0,&space;s_j-s_y_i&plus;1)" title="L_i= \sum_{j\neq y_i} max(0, s_j-s_y_i+1)" /></a>
	Mientras que la función *squared hinge loss* (penaliza mas la perdida) se define como:
	<a href="https://www.codecogs.com/eqnedit.php?latex=L_i=&space;\sum_{j\neq&space;y_i}&space;max(0,&space;s_j-s_y_i&plus;1)^2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?L_i=&space;\sum_{j\neq&space;y_i}&space;max(0,&space;s_j-s_y_i&plus;1)^2" title="L_i= \sum_{j\neq y_i} max(0, s_j-s_y_i+1)^2" /></a>

* Softmax: Esta función regresa probabilidades para cada clase mientras que la función *hinge* nos da el margen. 

