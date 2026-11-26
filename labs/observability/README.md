# Observability Track

You can't fix what you can't see. Logs, metrics and traces are how every production system is understood, and OpenTelemetry is the common layer that feeds every backend.

**Durability:** Very high for the concepts and OpenTelemetry; medium for each commercial suite.

Label: `track:observability`. Lab folders: `labs/observability/<lab>/`.

## Prerequisites

- [Containers Track](../containers/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  three_pillars["Logs, metrics, traces"]
  prometheus_grafana["Prometheus and Grafana"]
  opentelemetry["OpenTelemetry"]
  jaeger["Jaeger"]
  splunk_enterprise["Splunk Enterprise and SPL"]
  datadog["Datadog (trial)"]
  splunk_observability_cloud["Splunk Observability Cloud (trial)"]
  slo_alerting["SLOs and alerting"]
  three_pillars --> prometheus_grafana
  three_pillars --> opentelemetry
  opentelemetry --> jaeger
  three_pillars --> splunk_enterprise
  jaeger --> datadog
  jaeger --> splunk_observability_cloud
  prometheus_grafana --> slo_alerting

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class three_pillars,prometheus_grafana,opentelemetry,jaeger,splunk_enterprise,datadog,splunk_observability_cloud,slo_alerting todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `three-pillars`: Logs, metrics, traces | — | todo |
| `prometheus-grafana`: Prometheus and Grafana | — | todo |
| `opentelemetry`: OpenTelemetry | — | todo |
| `jaeger`: Jaeger | — | todo |
| `splunk-enterprise`: Splunk Enterprise and SPL | — | todo |
| `datadog`: Datadog (trial) | — | todo |
| `splunk-observability-cloud`: Splunk Observability Cloud (trial) | — | todo |
| `slo-alerting`: SLOs and alerting | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## Notes

Datadog and Splunk Observability Cloud are time-limited trials: finish the local labs first ([Tool Landscape](../../docs/Tool-Landscape.md)).

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [OpenTelemetry](https://opentelemetry.io/docs/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [Jaeger](https://www.jaegertracing.io/docs/)
- [Datadog](https://docs.datadoghq.com/)
- [Splunk docs](https://docs.splunk.com/)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
