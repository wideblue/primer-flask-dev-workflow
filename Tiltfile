# -*- mode: Python -*-

docker_build('simple-fask-api-image', '.')
k8s_yaml('db-dump-configmap.yaml')
k8s_yaml('db-deployment.yaml')
k8s_yaml('db-service.yaml')
k8s_yaml('adminer-deployment.yaml')
k8s_yaml('flask-api-deployment.yaml')
k8s_yaml('flask-api-service.yaml')
k8s_yaml('flask-api-ingress.yaml')

k8s_resource('flask-api', port_forwards=8000)
k8s_resource('adminer', port_forwards=8080)

local_resource(name='fill db', cmd='kubectl exec $(kubectl get pod -l io.kompose.service=db -o jsonpath={.items[0].metadata.name}) -- bash -c  "gunzip -c /db_data_dump/idmm.gz | psql postgres -U postgres"', trigger_mode=TRIGGER_MODE_MANUAL )