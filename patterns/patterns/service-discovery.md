---
id: service-discovery
name: Service Discovery and External Configuration
type: pattern
solves: [hardcoded-endpoints, distributed-monolith]
sources:
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://www.politesi.polimi.it/retrieve/04fb6ce8-cc33-4207-a932-6e0701e8f932/2022_04_ESAS.pdf
---

## Summary

Service Discovery lets a service find another one by logical name at runtime,
instead of by a fixed address in the code. External Configuration keeps every
environment specific value outside the build. Together they remove hardcoded
endpoints.

## How it works

Service instances register themselves with a registry, or the platform registers
them. A caller asks for a name, such as `orders`, and gets a healthy instance
back. Common options are Consul, Eureka, and Kubernetes DNS with services, where
the cluster does the work and the caller just uses the service name.

External configuration completes the picture: addresses, credentials, timeouts,
and feature flags come from environment variables or a config service. The same
build artifact then runs in every environment. Secrets belong in a secret store,
not in config files in the repository.

## When to use it

Use discovery when instances scale up and down, when addresses change, or when
you run more than one replica per service. Use external configuration always,
even in small systems, because it costs almost nothing and removes a whole class
of deploy problems.

## Cost and risks

The registry is infrastructure that must be run, monitored, and made highly
available, and callers need sensible behaviour when a lookup fails: cache the
last known good result and fail fast rather than hang. Wrong config now fails at
runtime instead of at compile time, so validate config at startup and refuse to
start when a required value is missing.

## Sources

- 12 Microservices Anti-Patterns, Garnet Grid.
- Design Patterns and Anti-Patterns in Microservices Architecture, Politecnico di Milano, 2022.
