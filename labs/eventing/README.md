# Eventing and Streaming Track

Queues and logs decouple services in time. Comparing a transactional queue (IBM MQ) with a replayable log (Kafka) shows what each guarantee costs.

**Durability:** High. Messaging patterns (pub/sub, queues, logs, outbox) are decades old; Kafka has been the default log for over ten years.

Label: `track:eventing`. Lab folders: `labs/eventing/<lab>/`.

## Prerequisites

- [Containers Track](../containers/README.md)
- [JVM Track](../jvm/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  MSG["Queues vs. logs, delivery guarantees"]
  JMS["JMS basics"]
  MQ["IBM MQ"]
  RMQ["RabbitMQ"]
  NATS["NATS and JetStream"]
  KAF["Kafka core"]
  KCON["Kafka Connect"]
  CDC["CDC with Debezium"]
  OUT["The outbox pattern"]
  FLINK["Stream processing with Flink"]
  MSG --> JMS
  JMS --> MQ
  MSG --> RMQ
  MSG --> NATS
  MSG --> KAF
  KAF --> KCON
  KCON --> CDC
  CDC --> OUT
  KAF --> FLINK

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class MSG,JMS,MQ,RMQ,NATS,KAF,KCON,CDC,OUT,FLINK todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `messaging-concepts`: Queues vs. logs, delivery guarantees | — | todo |
| `jms`: JMS basics | — | todo |
| `ibm-mq`: IBM MQ | — | todo |
| `rabbitmq`: RabbitMQ | — | todo |
| `nats`: NATS and JetStream | — | todo |
| `kafka-core`: Kafka core | — | todo |
| `kafka-connect`: Kafka Connect | — | todo |
| `cdc-debezium`: CDC with Debezium | — | todo |
| `outbox`: The outbox pattern | — | todo |
| `flink`: Stream processing with Flink | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [Apache Kafka](https://kafka.apache.org/documentation/)
- [RabbitMQ](https://www.rabbitmq.com/docs)
- [NATS](https://docs.nats.io/)
- [IBM MQ](https://www.ibm.com/docs/en/ibm-mq)
- [Debezium](https://debezium.io/documentation/)
- [Apache Flink](https://flink.apache.org/)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
