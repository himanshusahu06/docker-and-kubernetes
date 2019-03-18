# Kubernetes upgrades and rollout

Record deployment history.
```shell
$ kubectl create -f helloworld-black.yaml --record

deployment.apps/navbar-deployment created
service/navbar-service created
```

Change the deployment container image.
```shell
$ kubectl set image deployment/navbar-deployment helloworld=karthequian/helloworld:blue --record
```

list deployment history
```shell
$ kubectl rollout history deployment/navbar-deployment

deployment.extensions/navbar-deployment
REVISION  CHANGE-CAUSE
1         kubectl create --filename=helloworld-black.yaml --record=true
2         kubectl set image deployment/navbar-deployment helloworld=karthequian/helloworld:blue --record=true
```

rollback deployment to last change
```shell
$ kubectl rollout undo deployment/navbar-deployment

deployment.extensions/navbar-deployment rolled back
```

rollback deployment to specific revision
```shell
$ kubectl rollout undo deployment/navbar-deployment --to-revision=3
```

NOTE: reverting a  deployment is itself a revision.


launch service in the browser
```shell
$ minikube service {service_name}
```