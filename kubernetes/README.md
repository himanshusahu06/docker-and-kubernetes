# K8s

## Node
Node is worker machine in k8s cluster where pods actually resides and runs. it can be virtual machine or a physical machine. It must have
1. kubelet, kube-proxy, docker process running.
2. supervisord (Process Control System) process running.

## Pods
Pods are one or more docker application container. It has it's own network-ip and storage resource. Pods are ephemeral.

#### Pod status
1. Pending - not created yet.
2. Running - at least one container of pod are running.
3. Succeeded - all container of pod are have exited with zero status code.
4. Failed - all container of pod are have exited with zero status code but at least one container has exited with non-zero status code.
5. CrashLoopBackOff - pod is not able to restart and k8s is trying to restart it again and again.
6. ContainerCreating - K8s is creating the container.

## Controllers
Controller controls, monitor and manages the lifecycle of pods. It is useful in

1. load balancing
2. scaling

Type of controllers - 
1. Replica set
2. deployment
3. deamon sets
4. services


## Replica Sets
Ensures that specific number of replica of a pod are running all the time to ensure reliability.

## Deployments
specifies desired state of pods using replicaset controller. Deployment controller will try to match the pod's actual state with desired state. On a high level, deployment controller controls replicasets as it can create, destroy the pods to align with desired state.

1. it keeps history of deployment so that in case of any failure, deployment can be rollbacked to the previous one.
2. Getting the status of deployment will give you health of pods.

Consider this as pod managenent or replicaset controller. REplicaset allows us to deploy a number of pods and check the status as a single unit.

## DaemonSets
It ensures that all nodes runs a copy of specific pods. As nodes are added or removed from the cluster, a DeamonSet will add or remove the required pods.

## Jobs
 YTD

## Services
It it logical groping of similar pods. They allow one set of pods to another set of pods.

1. Service provides unchanged address for reliability.

Type
1. Internal - ip is reachable within k8s cluster
2. external - endpoint availble through node ip:port (NodePort)
3. Load Balancer - load balance the traffic among set of pods that it is managing.

### Labels
key value pair and can be attached to any k8s object (pods, deployment, services).

### Selectors
1. Equality based selector 
    1. **=**  two labels value should be equal
    2. **!=**  two labels value should not be equal
2. Set based selector
    1. **IN** :a value should be inside a set of defined values
    2. **NOTIN** :a value shouldn't be inside a set of defined values
    3. **EXIST** :determines whether a label exists or not

### Namespaces
YTD

## Kubelet
1. k8s node agent
2. communicates with api server to see if pods have been assigned to nodes.
3. exeute pod containers via docker engine (or other container engine).
4. Mounts and runs volumes
5. execute health check to identify pod/node status

Podspec - YAML file that describes a pod

6. it takes a set of pod specs that are provided by the kube api server and ensures containers described in those podspecs are running and healthy.
7. It only manages containers that were create by k8s api server.


## Kube-proxy: The network proxy
1. process runs on all worker nodes

YTD

1. user space
2. iptables mode

kube proxy watches the api server for adition and removal of services. for each new service, kube-proxy opens a randomly chosen port on the local node. and request landing on that port are proxied to one of the pods.


### K8s Commands

#### create a deployment/services/pods
```shell
$ kubectl create -f {yaml_file_location}
```

#### update a deployment/services/pods
```shell
$ kubectl apply -f {yaml_file_location}
```

Note: A Deployment’s rollout is triggered if and only if the Deployment’s pod template (that is, .spec.template) is changed, for example if the labels or container images of the template are updated. Other updates, such as scaling the Deployment, do not trigger a rollout.

#### get all deployment/services/pods
```shell
$ kubectl get [deployments|pods|services] -o wide
```
-o wide will output more information of entities.

Ex:- filter entities based on selector.
```shell
$ kubectl get deployments -o wide --selector='app=helloworld-pod'
```

#### delete single deployment/services/pods
```shell
$ kubectl delete [deployments|pods|services] {name}
```

#### get all replicasets
```shell
$ kubectl get rs -o wide
```
Ex:- filter replicasets for a given deployment.
```shell
kubectl get rs -o wide --selector='app=anotherworld-pod'
```

#### list all resources
```shell
$ kubectl get all

NAME                                           READY   STATUS    RESTARTS   AGE
pod/anotherworld-deployment-68865b9545-qfz9n   1/1     Running   0          11m
pod/anotherworld-deployment-68865b9545-z5xz6   1/1     Running   0          11m
pod/helloworld-deployment-fc4c5966f-86klx      1/1     Running   0          32m
pod/helloworld-deployment-fc4c5966f-mp8n2      1/1     Running   0          32m
pod/helloworld-deployment-fc4c5966f-t9575      1/1     Running   0          26m

NAME                           TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/anotherworld-service   LoadBalancer   10.108.88.154    <pending>     80:30376/TCP   5m20s
service/helloworld-service     LoadBalancer   10.108.179.160   <pending>     80:31963/TCP   31m
service/kubernetes             ClusterIP      10.96.0.1        <none>        443/TCP        19h

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/anotherworld-deployment   2/2     2            2           11m
deployment.apps/helloworld-deployment     3/3     3            3           32m

NAME                                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/anotherworld-deployment-68865b9545   2         2         2       11m
replicaset.apps/helloworld-deployment-fc4c5966f      3         3         3       32m
```

arguments:
1. **--show-labels**: as name suggests

### scale deployment
```shell
$ kubectl scale --replicas={num_replicas} deploy/{deployment_name}
```
The number of replicas(number of pods) for the deployment **deployment_name** will be changed from whatever their existing value is to **num_replicas**.

### get deployment information
```shell
$ kubectl describe deployments

Name:                   helloworld-deployment
Namespace:              default
CreationTimestamp:      Fri, 15 Mar 2019 12:53:08 +0530
Labels:                 app=helloworld
                        author=himanshu
                        env=prod
                        release-version=1.0
                        tier=ui
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=helloworld
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=helloworld
           author=himanshu
           env=prod
           release-version=1.0
           tier=ui
  Containers:
   helloworld:
    Image:        karthequian/helloworld:latest
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   helloworld-deployment-6746cd7c6b (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  70s   deployment-controller  Scaled up replica set helloworld-deployment-6746cd7c6b to 3
```

### list resources with labels
```shell
$ kubectl get [deployments|pods|services|rs] --show-labels
```

### update pod labels
```shell
$ kubectl label pod/{pod_name} key=value --overwrite
```

### remove pod label
```shell
$ kubectl label pod/{pod_name} key-
```

### filter resources by labels
label match
```shell
$ kubectl get pods --selector key1=value1,key2=value2
```
label inclusion
```shell
kubectl get pods --selector 'app in (helloworld2, helloworld)'
```
label exclusion
```shell
kubectl get pods --selector 'app notin (helloworld2, helloworld)'
```

### delete a resource with given label
```shell
$ kubectl delete pods --selector {filter}
```
filters are same as in above example.