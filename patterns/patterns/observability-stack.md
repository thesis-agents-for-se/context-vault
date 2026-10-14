---
id: observability-stack
name: Observability Stack
type: pattern
solves: [insufficient-monitoring, chatty-communication, service-chain, bottleneck-service, no-api-gateway]
sources:
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://www.designgurus.io/blog/10-common-microservices-anti-patterns
  - https://www.geeksforgeeks.org/blogs/microservice-anti-patterns/
---

## Summary

An Observability Stack is the combination of distributed tracing, central
structured logging, metrics, and alerts on user facing symptoms. It is what
makes a distributed system debuggable. It is also the tool that proves the other
antipatterns exist.

## How it works

- **Tracing.** Instrument services with OpenTelemetry. Create a trace at the
  edge and pass the context through every call, including messages on a broker.
  Backends such as Jaeger, Zipkin, or a hosted service store the traces.
- **Logging.** One structured format, usually JSON, with the trace id, service
  name, and version in every line. Ship logs to a central store such as an ELK
  stack so they can be searched together.
- **Metrics.** Export request rate, error rate, and latency percentiles per
  endpoint, plus saturation signals like pool usage. Prometheus and Grafana are
  the common choice.
- **Alerts.** Alert on error rate and latency against an agreed SLO, not on CPU.
  CPU tells you a machine is busy; the SLO tells you users are affected.

Traces are also the main input for architecture analysis: span depth exposes
`service-chain`, span count per request exposes `chatty-communication`, and the
service that appears in every trace is the `bottleneck-service`.

## When to use it

Set it up before or during the first extractions from the monolith. Without it,
you cannot measure whether the migration improved anything.

## Cost and risks

Storage and retention cost money, so sampling has to be tuned: keep all errors
and slow requests, sample the rest. Instrumenting every service takes effort and
is often left half done, which is worse than nothing because the gaps are
invisible. Dashboards with no owner go stale, and alerts that fire too often get
ignored.

## Sources

- 12 Microservices Anti-Patterns, Garnet Grid.
- 10 Common Microservices Anti-Patterns, Design Gurus.
- Microservice Anti-Patterns, GeeksforGeeks.
