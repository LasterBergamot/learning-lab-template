# Glossary

Short definitions of the terms these pages use. Add a term when a page first uses it.

| Term | Meaning |
|---|---|
| **Lab** | One self-contained learning project under `labs/<track>/<lab>/`, with its own brief, notes and teardown |
| **Track** | A group of related labs, such as Security or Orchestration, with its own `labs/<track>/README.md` page and `track:*` label |
| **Socratic method** | Teaching by asking questions that lead you to the answer, instead of telling you the answer |
| **Hint ladder** | The four steps the tutor climbs when you're stuck: question, pointer, concept, doc link ([How I Learn](How-I-Learn.md)) |
| **Milestones** | Understand → build → break → fix → explain; the five stages every lab goes through |
| **Explain it back** | Explaining a topic in your own words, without notes, to check you really understand it |
| **Spaced repetition** | Reviewing a fact at growing intervals, so it moves into long-term memory ([Review Queue](Review-Queue.md)) |
| **Isolation tier** | T0–T5: how strongly a lab is separated from the rest of the machine ([Isolation](Isolation.md)) |
| **Teardown** | The steps that remove everything a lab created: containers, volumes, clusters, VMs, cloud resources |
| **Compose project** | The group of containers, networks and volumes that one `compose.yml` creates; its `name:` keeps it separate from other labs |
| **Dev container** | A container that holds a whole development toolchain, described by `.devcontainer/` |
| **kind** | "Kubernetes in Docker": runs a Kubernetes cluster inside containers (Docker or Podman) |
| **Rootless containers** | Containers run without root on the host; safer, but they can't bind ports below 1024 |
| **Emulator (cloud)** | A local imitation of a cloud service, such as LocalStack for AWS, so you can learn without a bill |
| **IaC** | Infrastructure as Code: describing servers, networks and services in files that a tool applies |
| **Competency matrix** | A table of skills by level (Novice, Intermediate, Advanced) used for skill evaluations ([Assessments](Assessments.md)) |
| **Readiness** | Per competency: not started, learning, can explain, ready |
| **APM** | Agent Package Manager: installs the AI skills and agents from ai-common into this repo |
| **Skill (AI)** | A packaged instruction set for Claude Code, such as `socratic-tutor`; not to be confused with your own skills in [Assessments](Assessments.md) |
| **Output style** | A Claude Code setting that changes how every session behaves; here it puts every session in tutor mode |
| **Status line** | The `**Status:**` line under a lab README's title (`todo`, `learning`, `building`, `done`); the graphs follow it |
| **JWT** | JSON Web Token: a compact, signed (and optionally encrypted) set of claims, `header.payload.signature` |
| **JWS / JWE** | JSON Web Signature (signed, readable) and JSON Web Encryption (encrypted) — the two forms a JWT can take |
| **JWK / JWKS** | JSON Web Key: a public key as JSON. A JWKS is the set an issuer publishes so others can verify its tokens |
| **Claims** | The statements in a token: `iss` (issuer), `sub` (subject), `aud` (audience), `exp` (expiry), scopes |
| **OAuth 2** | A framework for delegated authorization: a client gets an access token to call an API |
| **OIDC** | OpenID Connect: an identity layer on OAuth 2 that adds the ID token (who logged in) |
| **Authorization code + PKCE** | The OAuth grant for apps with a user; PKCE ties the code to the client that asked for it |
| **Client credentials** | The OAuth grant for service-to-service calls, with no user involved |
| **Refresh token** | A long-lived token used to get new access tokens without a new login |
| **Token exchange** | RFC 8693: trading one token for another (different audience or scope), for delegation or impersonation |
| **Introspection** | Asking the identity provider whether a token is still active and what it contains (RFC 7662) |
| **DPoP** | Demonstrating Proof of Possession: binds a token to a client key, so a stolen token is useless alone |
| **IdP** | Identity provider: the service that logs users in and issues tokens, such as Keycloak |
| **Test pyramid** | Many fast unit tests at the bottom, fewer integration and API tests, very few end-to-end tests at the top |
| **Test double** | Anything standing in for a real collaborator in a test: dummy, stub, spy, mock or fake |
| **TDD** | Test-driven development: write a failing test, make it pass, refactor (red, green, refactor) |
| **BDD** | Behaviour-driven development: describe behaviour as examples agreed with the business, then automate them |
| **Gherkin** | The `Given / When / Then` language BDD scenarios are written in, run by Cucumber |
| **Contract test** | A test that checks two services agree on their API, without running both together |
| **Mutation testing** | Changing the code on purpose (mutants) to see whether the tests notice; measures test strength |
