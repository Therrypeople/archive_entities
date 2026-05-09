standup:
	k3d cluster create archive_entities -p "8081:80@loadbalancer"
	
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/
	helm repo update
	helm install kuberay-operator kuberay/kuberay-operator --version 1.6.0

	helm dependency build ./archive_entities_helm
	helm install archive_entities archive_entities_helm

standdown:
	k3d cluster delete archive_entities
