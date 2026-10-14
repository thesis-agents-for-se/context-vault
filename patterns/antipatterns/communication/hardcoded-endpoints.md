---
id: hardcoded-endpoints
name: Hardcoded Endpoints
category: communication
aliases: [Hard-Coded IPs, Static Endpoints, Hardcoded Service Addresses]
severity: medium
detects_on: [code, config]
signals:
  - IP addresses or host names written inside source files.
  - Port numbers fixed in code instead of read from config.
  - Environment specific URLs, such as a staging host, committed to the repository.
  - Base URLs built by string concatenation in several places.
  - No service discovery client and no DNS based service names.
related: [no-api-gateway, lack-of-communication-standards, distributed-monolith]
solutions: [service-discovery, api-gateway]
sources:
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://arxiv.org/abs/1908.04101
  - https://garnetgrid.com/insights/microservices-anti-patterns
---

## Summary

Hardcoded Endpoints means service addresses, IPs, or ports are written into the
source code instead of resolved at runtime. The code then only works in the
environment it was written for. Scaling, moving, or replacing an instance needs
a code change and a new release.

## Why it hurts

Hardcoded Endpoints block dynamic scaling, because new instances get new
addresses that nobody is calling. They make environments differ in code rather
than in config, which is a common cause of "works in staging, fails in
production". They also make failover slow: when a host dies, the fix is a
deploy. Finally, they hide the real dependency graph, since addresses are spread
through the code instead of declared in one place.

## How to spot it

- Grep for IPv4 patterns, `localhost`, `http://`, and `https://` in source
  files, excluding tests and documentation.
- Grep for port numbers next to host names, such as `:8080` or `:5432`.
- Look for environment names inside strings, such as `-dev`, `-qa`, `-prod`.
- Check whether the project has a discovery client, such as Consul, Eureka, or
  Kubernetes service names. If not, addresses come from somewhere fixed.
- Look for the same base URL repeated in several files instead of one client
  configuration.

## Solutions

### 1. Use service discovery

- **Do:** Register services and resolve them by logical name at call time, using
  Consul, Eureka, or Kubernetes DNS.
- **Fits when:** Instances come and go, or you run more than one replica per
  service.
- **Cost:** The registry becomes infrastructure you must run and monitor.
  Clients need a fallback when lookup fails.

### 2. Move addresses to external configuration

- **Do:** Read every address from environment variables or a config service, and
  keep one typed client configuration per dependency.
- **Fits when:** The platform is stable and discovery would be too much for the
  current size.
- **Cost:** Config must be managed per environment, and a wrong value now fails
  at runtime instead of at compile time.

### 3. Call through a gateway or a stable logical name

- **Do:** Point clients at one stable name, such as a gateway route or an
  internal load balancer, and let that layer decide the real instance.
- **Fits when:** A gateway or load balancer already exists.
- **Cost:** One more hop per call, and the gateway must be highly available.

## Related

Hardcoded Endpoints often appear together with `no-api-gateway`. When addresses
are hardcoded across many services, deployments become coordinated, which feeds
`distributed-monolith`.

## Sources

- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- 12 Microservices Anti-Patterns, Garnet Grid.
