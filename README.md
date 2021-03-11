

gunzip -c ime_datoteke | psql ime_baze -U ime_uporabnika

k3d registry create myregistry.localhost --port 5111

k3d cluster create newcluster --registry-use k3d-myregistry.localhost:5111 --api-port 6550 -p "8081:80@loadbalancer"


kubectl exec $(kubectl get pod -l io.kompose.service=db -o jsonpath={.items[0].metadata.name}) -- bash -c  "gunzip -c /db_data_dump/idmm.gz | psql postgres -U postgres"

Pods evicted due to lack of disk space
https://k3d.io/faq/faq/#pods-evicted-due-to-lack-of-disk-space
