standup:
	k3d cluster create archive-entities -p "8080:80@loadbalancer"
	
	helm repo add kuberay https://ray-project.github.io/kuberay-helm/
	helm repo update
	helm install kuberay-operator kuberay/kuberay-operator --version 1.6.0

	helm dependency build ./archive_entities_helm
	helm install archive-entities archive_entities_helm

standdown:
	k3d cluster delete archive-entities
