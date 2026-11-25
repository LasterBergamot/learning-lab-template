# Containers Track

Containers are the unit of almost every deployment today. Building one from scratch shows they are just Linux processes with namespaces, cgroups and a filesystem image.

**Durability:** High. OCI images and the namespace/cgroup model are standards; engines come and go.

Label: `track:containers`. Lab folders: `labs/containers/<lab>/`.

## Prerequisites

- [Foundations Track](../foundations/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  DOCK["Docker fundamentals"]
  OCI["OCI images and layers"]
  SCR["A container from scratch"]
  POD["Podman: rootless, pods, kube play"]
  COMP["Compose: multi-service apps"]
  ISEC["Image security and slim images"]
  EBPF["eBPF"]
  WASM["WebAssembly and WASI"]
  DOCK --> OCI
  OCI --> SCR
  DOCK --> POD
  DOCK --> COMP
  OCI --> ISEC
  SCR --> EBPF

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class DOCK,OCI,SCR,POD,COMP,ISEC,EBPF,WASM todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `docker-fundamentals`: Docker fundamentals | — | todo |
| `oci-images`: OCI images and layers | — | todo |
| `container-from-scratch`: A container from scratch | — | todo |
| `podman`: Podman: rootless, pods, kube play | — | todo |
| `compose`: Compose: multi-service apps | — | todo |
| `image-security`: Image security and slim images | — | todo |
| `ebpf`: eBPF | — | todo |
| `wasm-wasi`: WebAssembly and WASI | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [Docker docs](https://docs.docker.com/)
- [Podman](https://podman.io/)
- [Open Container Initiative](https://opencontainers.org/)
- [eBPF](https://ebpf.io/)
- [WASI](https://wasi.dev/)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
