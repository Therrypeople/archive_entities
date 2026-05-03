standup:
	k3d cluster create parishrecordskg -p "8081:80@loadbalancer"
	
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/
	helm repo update
	helm install kuberay-operator kuberay/kuberay-operator --version 1.6.0

	helm dependency build ./parish_records_helm
	helm install parishrecordskg parish_records_helm

standdown:
	k3d cluster delete parishrecordskg
