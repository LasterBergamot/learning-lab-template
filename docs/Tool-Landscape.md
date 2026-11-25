# Tool Landscape

Many of the tools in this repo overlap. None of them rule each other out, but learning two
competing tools before you understand what they compete *about* wastes time. This page groups
them, and for each group gives a recommendation and the catch.

Facts marked "(verify)" were true when this page was written but change often (prices, trial
lengths, licences). Check them before you rely on them.

## Container platforms: Kubernetes, OpenShift, Dokku

- **What they are:** OpenShift *is* Kubernetes, with Red Hat's opinions added: Routes,
  Security Context Constraints, built-in builds and CI. Dokku is a single-host, Heroku-style
  PaaS: `git push` and your app runs.
- **Recommendation:** Kubernetes first, then OpenShift, to see what a distribution adds. Dokku
  fits any time; it is small.
- **Catch:** OpenShift Local needs about 9 GB RAM and 35 GB disk (verify). Run it on your
  bigger machine, or use the free Red Hat Developer Sandbox (verify the current terms).

## Infrastructure as Code: Terraform/OpenTofu, Pulumi, SST, Ansible

- **What they are:** Terraform and Pulumi both *provision* infrastructure. Terraform uses HCL;
  Pulumi uses a general-purpose language. Both use the same state model. SST is an application
  framework on top of that kind of engine, focused on AWS. Ansible *configures* existing
  machines (packages, files, services); it doesn't provision them, so it **complements** the
  other three.
- **Recommendation:** Terraform first, because it is the most common in jobs. Learn OpenTofu
  alongside it: it is the open-source fork, created after Terraform moved to the BSL licence.
  Then Pulumi, to compare, then SST.
- **Catch:** SST mostly needs real AWS; LocalStack covers only part of it (verify).

## Observability: OpenTelemetry, Jaeger, Datadog, Splunk Observability Cloud, Splunk Enterprise

- **What they are:** OpenTelemetry is the vendor-neutral standard for producing and shipping
  traces, metrics and logs. Jaeger is an open-source tracing backend. Datadog and Splunk
  Observability Cloud are **competing** commercial suites (APM, metrics, logs). Splunk
  Enterprise is a different product: log search and SIEM with the SPL query language.
- **Recommendation:** learn OpenTelemetry once. Send the same telemetry to Jaeger locally, then
  compare Datadog and Splunk Observability Cloud side by side with the same app.
- **Catch:** the commercial suites are time-limited trials, about 14 days (verify). Finish the
  local prep first, then start the trial clock. Splunk Enterprise has a free licence with a
  daily ingest limit, about 500 MB/day (verify), and a container image.

## Continuous delivery: Spinnaker vs. Argo CD

- **What they are:** both deploy software continuously. Spinnaker comes from Netflix and is
  made of about ten microservices. Argo CD is GitOps (the cluster follows a Git repo) and has
  largely taken over in Kubernetes shops.
- **Recommendation:** Argo CD first. Spinnaker is optional and low priority.
- **Catch:** Spinnaker is very heavy. Run it on Windows only.

## Chaos engineering: Chaos Monkey vs. Chaos Mesh / Litmus

- **What they are:** tools that inject failures on purpose, to prove a system survives them.
  Chaos Monkey (Netflix) needs Spinnaker and is legacy. Chaos Mesh and Litmus are
  Kubernetes-native.
- **Recommendation:** learn the principles with Chaos Mesh. Run Chaos Monkey only if you do
  Spinnaker, as history.
- **Catch:** chaos needs observability first. Without metrics and traces you can't see what
  the failure did.

## Messaging: IBM MQ vs. Kafka / RabbitMQ / NATS

- **What they are:** IBM MQ is a transactional message queue (JMS, messages consumed and
  removed). Kafka is a replayable, partitioned log. RabbitMQ is a broker with flexible routing.
  NATS is a lightweight messaging system with an optional persistence layer (JetStream).
  Different models, not contradictions.
- **Recommendation:** do both a queue and a log, and compare what each guarantees: ordering,
  delivery, replay.
- **Catch:** the free IBM MQ developer image is fine for learning. MQ matters mostly in
  enterprise settings such as banks.

## Databases: IBM Db2 vs. Postgres

- **What they are:** both relational SQL databases. Db2 is common in enterprise and mainframe
  shops; Postgres is the open-source default.
- **Recommendation:** Postgres internals first, then Db2 as a contrast.
- **Catch:** the Db2 Community image is several GB and needs a privileged container (verify).
  Prefer Windows.

## Backend-in-a-box: PocketBase

- **What it is:** a single Go binary with SQLite: auth, a REST API, realtime subscriptions and
  an admin UI.
- **Recommendation:** a great early lab, and later a deploy target for Dokku.

## Diagrams: Cloudcraft

- **What it is:** an AWS architecture diagramming tool (owned by Datadog), not a runtime.
- **Recommendation:** use it while learning AWS and Terraform, to draw what you built.
- **Catch:** the free plan is limited (verify), and there is little depth to learn.

## Identity providers: Keycloak vs. others

- **What they are:** an identity provider (IdP) issues the tokens: Keycloak (open source,
  self-hosted, runs in a container), managed ones (Auth0/Okta, Microsoft Entra ID, AWS Cognito),
  and lighter self-hosted ones (Authentik, Zitadel, Ory).
- **Recommendation:** Keycloak for the labs. It runs locally on both platforms, implements the
  grants this repo covers (authorization code + PKCE, client credentials, device flow,
  introspection, token exchange) and is common in enterprise Java shops.
- **Catch:** Keycloak is heavy (a JVM, ~1 GB RAM) and its admin UI hides the protocol. Read the
  raw HTTP exchanges, not just the console. Token exchange support differs between versions (verify).

## JWT libraries and validation: do it by hand first

- **What they are:** libraries such as Nimbus JOSE + JWT (used by Spring Security) or jjwt
  parse and validate tokens. Online decoders show what's inside.
- **Recommendation:** decode and validate one token by hand first (base64url, signature check
  against the JWKS, `exp`/`aud`/`iss`), then let the library do it.
- **Catch:** never paste real tokens into online decoders. Most JWT vulnerabilities are
  validation mistakes (`alg: none`, algorithm confusion, missing `aud` check), not library bugs.

## Java testing: overlapping tools

- **Contract testing: Pact vs. Spring Cloud Contract.** Pact is consumer-driven and works
  across languages, with a broker to share contracts. Spring Cloud Contract is producer-side
  and Spring-only, and generates stubs and tests from contracts.
  **Recommendation:** Pact first, for the consumer-driven idea; Spring Cloud Contract as the
  contrast. **Catch:** contract tests replace some end-to-end tests, not unit tests.
- **BDD: Cucumber-JVM vs. JBehave / Serenity BDD.** All three run Gherkin-style scenarios.
  Cucumber is the most widely used; Serenity adds reporting on top.
  **Recommendation:** Cucumber-JVM. **Catch:** BDD is a conversation technique first. Gherkin
  written by developers alone is just slower tests.
- **Integration: Testcontainers vs. embedded fakes (H2, embedded Kafka).** Fakes are fast but
  differ from the real thing; Testcontainers runs the real service in a container.
  **Recommendation:** Testcontainers for anything with its own behaviour (databases, brokers).
  **Catch:** needs a container engine; on Windows/Podman set `DOCKER_HOST` (verify Ryuk).
- **Mocks: Mockito vs. hand-written fakes.** Mockito is quick; fakes are clearer for complex
  collaborators. **Recommendation:** learn the test-double taxonomy, then use both on purpose.
  **Catch:** heavy mocking tests the implementation, not the behaviour.
- **UI end-to-end: Playwright vs. Selenium.** Both drive real browsers. Playwright has
  auto-waiting and better tooling; Selenium is older and very widespread.
  **Recommendation:** Playwright for Java. **Catch:** keep end-to-end tests few: they are the
  top of the pyramid.

## Other durable topics

Topics that have mattered for 10–15 years and should keep mattering:

- Distributed systems theory and consensus (Raft): [Distributed Systems Track](../labs/distributed/README.md)
- Database internals (B-tree vs. LSM, MVCC, isolation levels): [Data Track](../labs/data/README.md)
- Security: TLS/PKI, supply chain (SBOM, Sigstore), post-quantum TLS: [Security Track](../labs/security/README.md)
- Identity: JWT, OAuth 2 grants, token exchange, OIDC, passkeys: [Identity and Access Track](../labs/identity/README.md)
- eBPF and WebAssembly/WASI: [Containers Track](../labs/containers/README.md), [Virtualization Track](../labs/virtualization/README.md)
- Concurrency models across languages: [Concurrency Models Track](../labs/concurrency/README.md)
- API design, DDD, event sourcing: [Architecture and Craft Track](../labs/architecture/README.md)
- The test pyramid, TDD, BDD, contract tests: [Testing Track](../labs/testing/README.md)
- Evals for AI systems: [AI Track](../labs/ai/README.md)
- Build-from-scratch classics (an interpreter, a KV store, an HTTP server): [Classics Track](../labs/classics/README.md)
- Podman itself: pods, rootless containers, `podman kube play`: [Containers Track](../labs/containers/README.md)
