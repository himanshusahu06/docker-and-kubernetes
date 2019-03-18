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
6. ErrImagePull - K8s is unable to pull image from docker.

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

### describe resources
It is very useful to debug any resources.
```shell
$ kubectl describe [deployments|pods|services|rs] {name}
```
ex. get deployment information
```shell
$ kubectl describe deployment helloworld-deployment
Name:                   navbar-deployment
Namespace:              default
CreationTimestamp:      Fri, 15 Mar 2019 16:24:56 +0530
Labels:                 app=helloworld
                        author=himanshu
                        env=prod
                        release-version=1.0
                        tier=ui
Annotations:            deployment.kubernetes.io/revision: 3
                        kubernetes.io/change-cause: kubectl create --filename=helloworld-black.yaml --record=true
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
    Image:        karthequian/helloworld:black
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
NewReplicaSet:   navbar-deployment-f778cfd96 (3/3 replicas created)
Events:
  Type    Reason             Age                    From                   Message
  ----    ------             ----                   ----                   -------
  Normal  ScalingReplicaSet  8m17s                  deployment-controller  Scaled up replica set navbar-deployment-5f957545c7 to 1
  Normal  ScalingReplicaSet  8m16s                  deployment-controller  Scaled down replica set navbar-deployment-f778cfd96 to 2
  Normal  ScalingReplicaSet  8m16s                  deployment-controller  Scaled up replica set navbar-deployment-5f957545c7 to 2
  Normal  ScalingReplicaSet  8m15s                  deployment-controller  Scaled down replica set navbar-deployment-f778cfd96 to 1
  Normal  ScalingReplicaSet  8m15s                  deployment-controller  Scaled up replica set navbar-deployment-5f957545c7 to 3
  Normal  ScalingReplicaSet  8m14s                  deployment-controller  Scaled down replica set navbar-deployment-f778cfd96 to 0
  Normal  ScalingReplicaSet  6m54s                  deployment-controller  Scaled up replica set navbar-deployment-f778cfd96 to 1
  Normal  ScalingReplicaSet  6m52s                  deployment-controller  Scaled down replica set navbar-deployment-5f957545c7 to 2
  Normal  ScalingReplicaSet  6m51s (x2 over 9m38s)  deployment-controller  Scaled up replica set navbar-deployment-f778cfd96 to 3
  Normal  ScalingReplicaSet  6m49s (x3 over 6m52s)  deployment-controller  (combined from similar events): Scaled down replica set navbar-deployment-5f957545c7 to 0
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
```shell
$ kubectl get pods --selector {filter}
```
filter can be:
1. label match - `key1=value1,key2=value2`
2. label inclusion `'key in (value1, value2)'`
3. label exclusion `'key notin (value1, value2)'`

### delete resources by labels
```shell
$ kubectl delete [deployments|pods|services|rs] --selector {filter}
```
filters are same as in above example.

### Logging into pods
you log into the containers not the pods. Thi command is almost similar to docker exec.
```exec
$ kubectl -ti exec <pod_name> -c <container_name> bash
```
You can omit **container name** if pod have only one container.


## Passing Dynamic Configuration to pods using configmap
1. create a configuration map
	```shell
	$ kubectl create configmap <map-name> <data-source>
	```

	ex:-
	create from literal
	```shell
	$ kubectl create configmap <map-name> --from-literal=key1=value1 --from-literal=key2=value2
	```
	create from file
	```shell
	$ kubectl create configmap yo2 --from-file=a.config
	configmap/yo2 created
	$ kubectl describe configmaps/yo2
	Name:         yo2
	Namespace:    default
	Labels:       <none>
	Annotations:  <none>

	Data
	====
	a.config:
	----
	enemies=aliens
	lives=3
	enemies.cheat=true
	enemies.cheat.level=noGoodRotten
	secret.code.passphrase=UUDDLRLRBABAS
	secret.code.allowed=true
	secret.code.lives=30

	Events:  <none>
	```

2. apply this configmap in pod template of deployment yaml

	```
	apiVersion: extensions/v1beta1
	kind: Deployment
	metadata:
	name: logreader-dynamic
	spec:
	replicas: 1
	template:
		metadata:
		labels:
			name: logreader-dynamic
		spec:
		containers:
		- name: logreader
			image: karthequian/reader:latest
			env:
			- name: log_level
			valueFrom:
				configMapKeyRef:
				name: logger    # Read from a configmap called log-level
				key: log_level  # Read the key called log_level
	```

https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/


## Passing sensitive data to pods using secrets
1. create secret (params of creating secret is same as configmap)
	```shell
	$ kubectl create secret generic <secret_name> --from-literal=key1=value1 --from-literal=key2=value2
	```

	ex:-
	```shell
	$ kubectl create secret generic my_secret --from-literal=api_key=1234567
	```
	describe secret `$ kubectl get secret my_secret -o yaml`
	```
	apiVersion: v1
	data:
		api_key: MTIzNDU2Nw==
	kind: Secret
	metadata:
		creationTimestamp: "2019-03-18T06:26:34Z"
		name: my-secret
		namespace: default
		resourceVersion: "35797"
		selfLink: /api/v1/namespaces/default/secrets/my-secret
		uid: c7183229-4946-11e9-81a4-080027afc910
	type: Opaque
	```

2. use the secret within container
	```
	apiVersion: extensions/v1beta1
	kind: Deployment
	metadata:
	name: secretreader
	spec:
	replicas: 1
	template:
		metadata:
		labels:
			name: secretreader
		spec:
		containers:
		- name: secretreader
			image: karthequian/secretreader:latest
			env:				  # api_key will be availble as env
			- name: api_key
			valueFrom:
				secretKeyRef:
				name: my_secret   # Read from a secret called my_secret 
				key: api_key      # Read the key called api_key
	```
https://kubernetes.io/docs/concepts/configuration/secret/

## Jobs
Jobs run a pod once and then stops. Output of jobs is persisted.

1. Simple job (Job) - this runs once.
	```
	apiVersion: batch/v1
	kind: Job
	metadata:
	name: finalcountdown
	spec:
	template:
		metadata:
		name: finalcountdown
		spec:
		containers:
		- name: counter
			image: busybox
			command:
			- bin/sh
			- -c
			- "for i in 9 8 7 6 5 4 3 2 1 ; do echo $i ; done"
		restartPolicy: Never #could also be Always or OnFailure
	```
	get simple job details -
	```shell
	$ kubectl get jobs
	NAME             COMPLETIONS   DURATION   AGE
	finalcountdown   1/1           8s         73s
	```
	pod will be in `Complete` state after execution. you can get the output of jobs by running `kubectl logs <pod_name>`

	https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

2. Schedule a Job (CronJob) - runs periodically
	```text
	apiVersion: batch/v1beta1
	kind: CronJob
	metadata:
	name: hellocron
	spec:
	schedule: "*/1 * * * *" #Runs every minute (cron syntax) or @hourly.
	jobTemplate:
	  spec:
		template:
		  spec:
		  containers:
		  - name: hellocron
		    image: busybox
		    args:
		    - /bin/sh
				- -c
				- date; echo Hello from your Kubernetes cluster
			restartPolicy: OnFailure #could also be Always or Never
	suspend: false #Set to true if you want to suspend in the future
	```

	get cron job details -
	```shell
	$ kubectl get cronjobs
	NAME        SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
	hellocron   */1 * * * *   False     0        <none>          15s
	```
	pod will be in `Complete` state after execution. you can get the output of jobs by running `kubectl logs <pod_name>`

	stop cron job - edit jobs by running `kubectl edit cronjobs/hellocron` and turn the `suspend` variable to `True`.

	https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/


----

## Deamon sets
YTD