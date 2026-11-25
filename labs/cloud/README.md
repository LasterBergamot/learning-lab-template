# Cloud Track

The three big clouds share the same building blocks (compute, IAM, storage, queues, serverless). Learning one deeply and the others by comparison is cheaper than learning three separately.

**Durability:** High. IAM and the shared-responsibility model are stable; service names change.

Label: `track:cloud`. Lab folders: `labs/cloud/<lab>/`.

## Prerequisites

- [Foundations Track](../foundations/README.md)

## Planned labs

An arrow means "do this lab first". The colours follow the [legend in the root README](../../README.md#legend).

<!-- roadmap-sync:start -->
```mermaid
flowchart LR
  cloud_fundamentals["Cloud fundamentals and pricing"]
  iam["IAM"]
  aws_core["AWS core: compute, storage, VPC"]
  localstack["LocalStack"]
  aws_serverless["Serverless: Lambda, queues"]
  gcp_core["GCP core and emulators"]
  azure_core["Azure core and Azurite"]
  cross_cloud["Cross-cloud comparison"]
  cloudcraft["Diagrams with Cloudcraft"]
  cloud_fundamentals --> iam
  iam --> aws_core
  aws_core --> localstack
  localstack --> aws_serverless
  cloud_fundamentals --> gcp_core
  cloud_fundamentals --> azure_core
  aws_core --> cross_cloud
  gcp_core --> cross_cloud
  azure_core --> cross_cloud
  aws_core --> cloudcraft

  classDef todo fill:#e5e7eb,color:#111827,stroke:#6b7280
  classDef learning fill:#fde68a,color:#111827,stroke:#b45309
  classDef building fill:#bfdbfe,color:#111827,stroke:#1d4ed8
  classDef done fill:#bbf7d0,color:#111827,stroke:#15803d
  class cloud_fundamentals,iam,aws_core,localstack,aws_serverless,gcp_core,azure_core,cross_cloud,cloudcraft todo
```
<!-- roadmap-sync:end -->

| Lab | Folder | Status |
|---|---|---|
| `cloud-fundamentals`: Cloud fundamentals and pricing | — | todo |
| `iam`: IAM | — | todo |
| `aws-core`: AWS core: compute, storage, VPC | — | todo |
| `localstack`: LocalStack | — | todo |
| `aws-serverless`: Serverless: Lambda, queues | — | todo |
| `gcp-core`: GCP core and emulators | — | todo |
| `azure-core`: Azure core and Azurite | — | todo |
| `cross-cloud`: Cross-cloud comparison | — | todo |
| `cloudcraft`: Diagrams with Cloudcraft | — | todo |

`plan-lab` creates a lab's folder from [`labs/_template/`](../_template/README.md) when you start it, and fills in the Folder column. Until then the plan above is a proposal you can change. Each lab's own README carries its `**Status:**` line; `roadmap-sync` reads those lines to colour the graph and this table.

## Notes

Set a budget alert before creating any real cloud resource ([Isolation](../../docs/Isolation.md)).

## References

Every online source used for this track or its labs goes here (or in the lab's own README), with a one-line note when it isn't obvious.

- [AWS docs](https://docs.aws.amazon.com/)
- [Google Cloud docs](https://cloud.google.com/docs)
- [Azure docs](https://learn.microsoft.com/azure/)
- [LocalStack](https://docs.localstack.cloud/)
- [Cloudcraft](https://www.cloudcraft.co/)

See also [Tool Landscape](../../docs/Tool-Landscape.md) and [Isolation](../../docs/Isolation.md).
