variable "proxmox_api_url" {
  description = "URL API Proxmox"
}

variable "proxmox_api_token_id" {
  description = "API Token ID у форматі ..."
}

variable "proxmox_api_token_secret" {
  description = "Секрет API токена"
  sensitive   = true
}

variable "proxmox_node" {
  description = "Ім'я Proxmox-ноди, куди розгортати ВМ"
}

variable "vm_template_name" {
  description = "Назва QEMU VM-шаблону"
}

variable "vm_template_vmid" {
  description = "VM ID"
}

variable "cloud_init_user" {
  description = "Ім'я користувача для cloud-init"
}

variable "cloud_init_password" {
  description = "Пароль для cloud-init"
  sensitive   = true
}
