# Distributed Systems Track

The most durable track. Every system with more than one machine meets the same problems: partial failure, unreliable clocks, consistency trade-offs, and agreement.

**Durability:** Very high. Lamport clocks are from 1978 and Raft from 2014; the problems don't change.

Label: `track:distributed`. Lab folders: `labs/distributed/<lab>/`.

## Prerequisites

- [Eventing and Streaming Track](../eventing/README.md)
- [Data Track](../data/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  failure_models["Fallacies and failure models"]
  clocks["Clocks and ordering"]
  consistency_models["Consistency models"]
  cap_pacelc["CAP and PACELC"]
  replication["Replication"]
  raft["Consensus: a toy Raft"]
  idempotency_retries["Idempotency and retries"]
  sagas["Sagas"]
  crdts["CRDTs and local-first"]
  failure_models --> clocks
  clocks --> consistency_models
  consistency_models --> cap_pacelc
  consistency_models --> replication
  replication --> raft
  failure_models --> idempotency_retries
  idempotency_retries --> sagas
  consistency_models --> crdts

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class failure_models,clocks,consistency_models,cap_pacelc,replication,raft,idempotency_retries,sagas,crdts todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `failure-models`: Fallacies and failure models | — | todo |
| `clocks`: Clocks and ordering | — | todo |
| `consistency-models`: Consistency models | — | todo |
| `cap-pacelc`: CAP and PACELC | — | todo |
| `replication`: Replication | — | todo |
| `raft`: Consensus: a toy Raft | — | todo |
| `idempotency-retries`: Idempotency and retries | — | todo |
| `sagas`: Sagas | — | todo |
| `crdts`: CRDTs and local-first | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [Raft](https://raft.github.io/)
- [Jepsen: consistency models](https://jepsen.io/consistency)
- [CRDT resources](https://crdt.tech/)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
