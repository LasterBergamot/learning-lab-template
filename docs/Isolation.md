# Isolation

Each lab must be startable, breakable and deletable without affecting any other lab or the
machine. This is what lets you experiment freely: break the TLS lab on purpose, and Kafka
doesn't notice.

## Tiers

Every lab names the lowest tier that gives it enough isolation. Lower tiers are cheaper and
faster.

| Tier | Mechanism | What it isolates | Examples |
|---|---|---|---|
| **T0 Toolchain** | a `mise.toml` per lab (Java, Node, Go, Flutter versions); a `uv` virtual env per Python lab | Language and tool versions | Java concurrency, Flask |
| **T1 Container** | a per-lab `compose.yml` with a unique top-level `name:` | Processes, networks, volumes; the compose project name scopes all of them | Kafka, IBM MQ, Db2, PocketBase, Jaeger, nginx with TLS |
| **T2 Dev container** | `.devcontainer/` per lab (Docker) | The whole dev toolchain, when installing it on the host would be messy | Flutter, Django with system dependencies |
| **T3 VM** | throwaway VMs: QEMU/libvirt (nested virtualization inside the Omarchy VM) | A whole OS, for tools that want to own a host | Dokku, Ansible targets, KVM basics |
| **T4 Cluster** | one kind cluster per lab, deleted afterwards | A whole Kubernetes control plane | Kubernetes, Istio, Argo CD, Chaos Mesh |
| **T5 Cloud** | emulators first (LocalStack, Azurite, GCP emulators), then free tiers or trials | Real cloud resources and bills | AWS, Datadog, Splunk, OpenShift Developer Sandbox |

## Rules

- **No shared running state.** A lab never depends on another lab's containers, clusters or
  data. Starting a lab never needs another one to be up.
- **Copy shared infrastructure, don't link it.** If two labs need Postgres, each has its own in
  its own compose file. Duplication is the price of independence.
- **One heavy lab at a time.** See the budget below.
- **Cloud labs (T5)** set a budget alert before creating anything, use a separate project or
  account per lab where the provider allows it, never commit credentials, and end with
  `destroy` in the teardown.
- **Time-boxed trials** (Datadog, Splunk Observability Cloud): finish all local preparation
  first, then start the trial, so the clock isn't wasted on setup.

## Resource budget

Record your machines here, with the date you measured free disk: for example "Linux VM: 8 cores,
**16 GB RAM**, **40 GB free disk** on YYYY-MM-DD". The tiers below assume roughly that.

- Light (fits easily): T0 labs, single-container T1 labs, PocketBase, Jaeger.
- Medium (one at a time): Kafka, Postgres + app, a small kind cluster.
- Heavy (only with enough RAM and disk in the VM): OpenShift Local (about 9 GB RAM, 35 GB disk; verify), Spinnaker,
  Db2 Community, the Android emulator, local LLMs larger than a few GB.

Before starting a medium or heavy lab:

```bash
docker system df
```

## Teardown discipline

Every lab has a `TEARDOWN.md`. Run it when you finish a session, not just at the end of the
lab. Typical steps:

- `docker compose down -v`: stops containers and
  removes the lab's volumes.
- `kind delete cluster --name <lab>`.
- Remove the lab's VMs and their disk images.
- Cloud: `terraform destroy` / `pulumi destroy`, then check the billing console.
- Occasionally: `docker image prune` for images no lab uses any more.

A lab is only "done" when its teardown leaves `docker ps -a` and `docker system df` as they were before the lab started.
