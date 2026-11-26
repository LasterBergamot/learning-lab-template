# Virtualization Track

VMs sit under every cloud, and under the Omarchy VM this repo runs in. Knowing what a hypervisor does explains cloud instance types, nested virtualization and microVMs.

**Durability:** High. Hardware virtualization has been the base of the cloud for twenty years; microVMs are its current direction.

Label: `track:virtualization`. Lab folders: `labs/virtualization/<lab>/`.

## Prerequisites

- [Foundations Track](../foundations/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  hypervisors["Hypervisor concepts"]
  kvm_qemu["KVM and QEMU (Linux)"]
  libvirt["libvirt"]
  cloud_init["cloud-init images"]
  firecracker["Firecracker microVMs"]
  vagrant_libvirt["Vagrant on libvirt"]
  hypervisors --> kvm_qemu
  kvm_qemu --> libvirt
  libvirt --> cloud_init
  kvm_qemu --> firecracker
  hypervisors --> vagrant_libvirt

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class hypervisors,kvm_qemu,libvirt,cloud_init,firecracker,vagrant_libvirt todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `hypervisors`: Hypervisor concepts | — | todo |
| `kvm-qemu`: KVM and QEMU (Linux) | — | todo |
| `libvirt`: libvirt | — | todo |
| `cloud-init`: cloud-init images | — | todo |
| `firecracker`: Firecracker microVMs | — | todo |
| `vagrant-libvirt`: Vagrant on libvirt | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [QEMU docs](https://www.qemu.org/docs/master/)
- [libvirt](https://libvirt.org/)
- [cloud-init](https://cloud-init.io/)
- [Firecracker](https://firecracker-microvm.github.io/)
- [Vagrant](https://developer.hashicorp.com/vagrant)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
