# Kubernetes 

## Conceptos generales 

* **Pod**: Un pod consiste en uno mas contenedores que tienen el mismo ```host```, 
  permitiendo compartir el stack de red(permitiendo comunicarse por localhost),
  volumenes entre otros.


## Network 
Es importante recordar que la red de docker en el host se encuentra ligada como bridge.
* **Pod**: Sea ```veth0``` la interfaz virtual de red del pod. Esta será ligada a 
 la red de docker (Funcionando como gateway para la interfaz ```veth0```). 

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

