# Platforms

learning-lab runs on **Linux with Docker**. The reference machine is Omarchy running as a Linux
VM through Try Omarchy for Windows. Any other Arch-based distro works the same way, and any other
Linux distro works too: `scripts/prereqs.sh` installs through mise there and names the system
packages for you to install with your package manager.

## The platform

| Concern | Linux (Omarchy VM, or any distro) |
|---|---|
| Container engine | Docker with the compose plugin (`docker compose`) |
| Shell and tooling | bash, mise, uv; system packages from pacman (yay for AUR) on Arch-based distros |
| Machine setup (optional) | dev-config `install.sh` |
| Guard hooks (optional) | ai-common guards |
| Kubernetes | kind |
| VMs (tier T3) | QEMU/libvirt. Inside the Omarchy VM this needs nested virtualization enabled on the host |
| Heavy labs (OpenShift Local, Spinnaker, Db2, Android emulator) | Only with enough RAM and disk in the VM (see [Isolation](Isolation.md)) |

## Portability rules for labs

These rules are also in `.claude/rules/labs.md` and in the lab template. They keep each lab on
open standards (the Compose spec, OCI images), so it runs on any Linux machine with Docker.

- **Compose spec only.** No Docker-only extensions that other Compose implementations reject.
- **No `network_mode: host`.** Publish ports instead, so labs don't clash with each other or the
  host.
- **Host ports above 1024.** Use `8443:443`, not `443:443`: no root needed, fewer clashes.
- **Relative bind mounts** (`./certs:/etc/nginx/certs`), never absolute host paths.
- **LF line endings.** The repo's `.gitattributes` forces `eol=lf`.
- **Name the compose project.** A unique top-level `name:` in every `compose.yml` keeps
  networks and volumes per lab ([Isolation](Isolation.md)).

## What each lab README states

```
Tested on: Linux/Docker ☐
Resources: ~RAM, ~disk, isolation tier
```

Tick the box only after the lab has run end to end, teardown included.
