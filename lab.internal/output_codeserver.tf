

resource "proxmox_vm_qemu" "glusterfs_cluster" {

  count = 1 # node counts

  name        = "codeserver-${count.index + 1}"
  target_node = "pve-node-0"
#  target_node = "pve-nuc-0${count.index + 1}"
  clone       = "debian-12-genericcloud-01"
  agent       = 1

  os_type     = "cloud-init"
  cores       = 4
  sockets     = 1
  cpu         = "host"
  memory      = 4192
  scsihw      = "virtio-scsi-pci"
  bootdisk    = "scsi0"

  disks {
    ide {
        ide2 {
            cloudinit {
                storage = "zfs"
            }
        }
    }     
    scsi {
      
      scsi0 {
        disk {
          size        = "32G"
          storage     = "zfs"
          discard     = true  
          iothread    = false       
          emulatessd  = true
        }
      }
      
      scsi1 {
        disk {
          size        = "64G"
          storage     = "zfs"
          discard     = true  
          iothread    = false       
          emulatessd  = true
        }
      }
      
    }
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
    tag    = "1010"
  }

  # Cloud Init Settings
  ipconfig0 = "ip=${cidrhost("10.10.10.17/24", 40 + count.index)}/24,gw=${cidrhost("10.10.10.17/24", 1)}"

  skip_ipv6 = true

  cicustom = "user=local:snippets/cloud-init-config.yaml"

  lifecycle {
    ignore_changes = [
      
      ciuser,
      
      sshkeys,
      
      network,
      
    ]
  }

}
