# Kubernetes 

## Conceptos generales 

* **Pod**: Un pod consiste en uno mas contenedores que tienen el mismo ```host```, 
  permitiendo compartir el stack de red(permitiendo comunicarse por localhost). También comparten volumenes y otros recursos.


## Network 
Es importante recordar que la red de docker en el host se encuentra ligada como bridge.
* **Pod**: Sea ```veth0``` la interfaz virtual de red del pod. Esta será ligada a 
 la red de docker (Funcionando como gateway para la interfaz ```veth0```). 

 <img src="https://raw.githubusercontent.com/mvilchis/Notas/master/kubernetes/images/host.png" height="240">


 En la imagen se muestran dos contenedores compartiendo la una interfaz existente. Esta funcionalidad es herdedada de docker y kubernetes la implementa creando un pod especial iniciado en ```pause```. 
 El esquema con mas nodos se vería: 


 <img src="https://raw.githubusercontent.com/mvilchis/Notas/master/kubernetes/images/hosts.png" height="240">


Este esquema genera un problema, en cada nodo no se sabe que espacio de direcciones privadas se le asigno a los otros nodos para su servicio de docker. Por lo que kubernetes ofrece un espacio de direcciones: ```overall address space ```   asignando las direcciones basado en cada nodo. La otra solución es una tabla de ruteo.
 
 

## Comandos principales 
* Listar los pods del cluster, mostrando en que nodo estan

  ```kubectl get pods -o wide ```
* Aplicar un comando a un pod dado, (para este ejemplo supongamos que el pod tiene 
  nombre igual a django_ldap) . Este comando puede ser abrir una terminal.

 ``` kubectl exec -it django_ldap bash ```

 Otro ejemplo puede ser un cat al archivo hosts:

 ```kubectl exec -it django_ldap cat /etc/host ```
* Ver los logs del pod (Mostrará la salida stdout de los comandos que esten 
  ejecutandose en el pod)

  ``` kubectl logs --follow django_ldap```
* Ver la configuración y los ultimos eventos del pod
  ``` kubectl describe pod django_ldap```


## Instalación
### Master
  Agregamos el repositorio de kubernetes (y apagamos el swap)
  ``` 
     # apt-get update && apt-get install -y apt-transport-https   && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
     # echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
     # swapoff -a
```
  Actualizamos la lista de repositorios e instalamos el manejador de kubernetes para ubuntu
```
     # apt-get update  
     # apt-get install -y kubelet kubeadm kubernetes-cni docker.io 
 ```
 Iniciamos el nodo master de kubernetes, con la red 10.130.0.0/22 para los pods. 
 Con este comando obtendremos un **_TOKEN_** y un **_CERTIFICADO_**, los cuales usaremos para conectar a los workers
 ```
     # kubeadm init --pod-network-cidr=10.130.0.0/22 --apiserver-advertise-address=10.90.0.30 --kubernetes-version stable-1.11
```
Agregamos la configuración como usuarios normales
```
      $ mkdir -p $HOME/.kube
      $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
      $ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
Agregamos al manejador de red, flannel

```
      $ sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
      $ sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
  ```
### Workers
  Agregamos el repositorio de kubernetes (y apagamos el swap)
  ``` 
     # apt-get update && apt-get install -y apt-transport-https   && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
     # echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
     # swapoff -a
```
  Actualizamos la lista de repositorios e instalamos el manejador de kubernetes para ubuntu
```
     # apt-get update  
     # apt-get install -y kubelet kubeadm kubernetes-cni docker.io 
 ```
 Agregamos el nodo al worker con el  **_TOKEN_**  y **_CERTIFICADO_** del master.
 ```
  kubeadm join 10.90.0.30:6443 --token TOKEN --discovery-token-ca-cert-hash sha256:CERTIFICADO
  ```
  
  Una vez terminado el proceso, podremos listar a nuestros nodos: 
  ```
  kubectl get nodes
  NAME         STATUS    ROLES     AGE       VERSION
  k8           Ready     master    36s       v1.11.2
  k8-worker1   Ready     <none>    34s       v1.11.2
  k8-worker2   Ready     <none>    34s       v1.11.2
  ```
