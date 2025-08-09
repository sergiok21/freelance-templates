resource "proxmox_vm_qemu" "test01" {
  name = "..."
  target_node = var.proxmox_node
  vmid = 0
  clone = var.vm_template_name
  full_clone = true

  ciuser = var.cloud_init_user
  cipassword = var.cloud_init_password
}
