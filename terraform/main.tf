resource "azurerm_resource_group" "rg" {
  name     = "terraform-azure"
  location = "West Europe"
}
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "terraform-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "exampleaks1"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "test"
  }
}

output "client_certificate" {
  value     = azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate
  sensitive = true
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

#to set kubectl default cluster as the cluster created by terraform:
#export KUBECONFIG=$(terraform output -raw kube_config)
