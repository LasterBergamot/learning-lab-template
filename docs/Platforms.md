# Platforms

Every lab should run on both supported platforms. Having two platforms means a lab can move to
the bigger machine when the other runs out of disk or RAM, and it forces each lab to rely on open
standards (the Compose spec, OCI images) instead of one engine's quirks.

## The two platforms

| Concern | Linux: the Omarchy VM | Windows 11 host |
|---|---|---|
| Container engine | Docker (`docker compose`) | Podman Desktop, with the `podman` CLI used from **Git Bash** (`podman compose`) |
| Podman machine (the Linux VM that runs the containers) | n/a | **Hyper-V provider** (`CONTAINERS_MACHINE_PROVIDER=hyperv`, Windows 11 Pro/Enterprise). On Windows Home only WSL2 works; it stays an invisible backend |
| Shell and tooling | bash, mise, uv | **Git Bash only**, no WSL2 distro. mise and uv run natively |
| Machine setup (optional) | dev-config `install.sh` | dev-config `install.ps1` (launches Git Bash) |
| Guard hooks (optional) | ai-common guards | ai-common guards (tested in Git Bash) |
| Kubernetes | kind | kind with `KIND_EXPERIMENTAL_PROVIDER=podman` |
| VMs (tier T3) | QEMU/libvirt through nested KVM | Hyper-V VMs, optionally through Vagrant's Hyper-V provider |
| Heavy labs (OpenShift Local, Spinnaker, Db2, Android emulator) | Only with enough RAM and disk (see [Isolation](Isolation.md)) | Usually the bigger machine |

Why kind and not k3d: kind supports both Docker and Podman. k3d targets Docker (Podman support
is partial; verify).

## Portability rules for labs

These rules are also in `.claude/rules/labs.md` and in the lab template.

- **Compose spec only.** No Docker-only extensions. If a lab really needs the Docker socket
  (`/var/run/docker.sock`), its README says how to point it at the Podman socket.
- **No `network_mode: host`.** It behaves differently on Podman and on Windows. Publish ports instead.
- **Host ports above 1024.** Rootless Podman cannot bind lower ports. Use `8443:443`, not `443:443`.
- **Relative bind mounts** (`./certs:/etc/nginx/certs`), never absolute host paths.
- **LF line endings.** The repo's `.gitattributes` forces `eol=lf`, so scripts mounted into
  Linux containers never break on CRLF.
- **Testcontainers on Podman** needs `DOCKER_HOST` pointing at the Podman socket, and possibly
  Ryuk disabled (verify per Testcontainers version). Labs that use it say so.
- **Name the compose project.** A unique top-level `name:` in every `compose.yml` keeps
  networks and volumes per lab ([Isolation](Isolation.md)).

## What each lab README states

```
Tested on: Linux/Docker ☐  Windows/Podman ☐
Resources: ~RAM, ~disk, isolation tier
```

Tick a box only after the lab has run end to end on that platform, teardown included.
