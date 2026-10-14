---
id: insufficient-monitoring
name: Insufficient Monitoring
category: operations
aliases: [Ignoring Observability, No Distributed Tracing, Blind Microservices]
severity: high
detects_on: [code, config, docs]
signals:
  - No correlation id or trace id is passed between services.
  - Logs are written to local files per instance with no central collection.
  - No metrics endpoint and no metrics library in the services.
  - Log formats differ per service, so logs cannot be searched together.
  - No alerts on error rate or latency, only on host level CPU and memory.
  - Errors from a downstream call are logged without any context about the caller.
related: [lack-of-communication-standards, chatty-communication, service-chain, bottleneck-service]
solutions: [observability-stack, api-contract-standards]
sources:
  - https://www.designgurus.io/blog/10-common-microservices-anti-patterns
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://www.geeksforgeeks.org/blogs/microservice-anti-patterns/
---

## Summary

Insufficient Monitoring means the system has no reliable way to see what happens
across services: no distributed traces, no central logs, no useful metrics. In a
monolith a stack trace was often enough. In microservices one request touches
many processes, so without tracing nobody can answer which service was slow.

## Why it hurts

Incidents take much longer to resolve, because finding the failing service is
guesswork. Problems that only appear under load, such as a slow dependency or a
retry storm, stay invisible until they cause an outage. It also blocks
improvement work: you cannot fix `chatty-communication` or `service-chain` if
you cannot measure the call paths. This antipattern makes every other one harder
to detect, which is why it should be fixed early.

## How to spot it

- Grep for a correlation or trace header, such as `traceparent`,
  `X-Request-Id`, or `X-Correlation-Id`. If services do not read and forward
  one, there is no end to end view.
- Check for a tracing library or agent, such as OpenTelemetry, Jaeger, or
  Zipkin, in the dependencies.
- Check whether logs are structured, for example JSON, and whether they are
  shipped to a central system.
- Look for a metrics endpoint, such as `/metrics`, or a metrics client in the
  code.
- Read the alert rules. Only infrastructure alerts, with nothing about request
  errors or latency, is the signal.

## Solutions

### 1. Add distributed tracing

- **Do:** Instrument every service with OpenTelemetry, generate a trace id at
  the edge, and pass the context through every call, including messages on a
  broker.
- **Fits when:** Requests cross more than two services, which is almost always.
- **Cost:** Every service needs instrumenting, plus a backend to store traces.
  Sampling must be tuned so the cost stays reasonable.

### 2. Centralise logs and metrics

- **Do:** Use one structured log format with the trace id in every line, ship
  logs to a central store, and export metrics for request rate, errors, and
  latency per endpoint.
- **Fits when:** Logs exist but are scattered and hard to compare.
- **Cost:** Storage and retention cost, and some effort to agree on a shared
  format.

### 3. Define SLOs and alert on symptoms

- **Do:** Set target error rate and latency per user facing flow, and alert on
  those instead of on raw resource use.
- **Fits when:** You already collect metrics but pages are noisy or late.
- **Cost:** SLOs need agreement with the business and regular review to stay
  meaningful.

## Related

Insufficient Monitoring hides `chatty-communication`, `service-chain`, and
`bottleneck-service`. Fixing it first makes the other findings measurable.

## Sources

- 10 Common Microservices Anti-Patterns, Design Gurus.
- 12 Microservices Anti-Patterns, Garnet Grid.
- Microservice Anti-Patterns, GeeksforGeeks.
