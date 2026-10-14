---
id: resilience-patterns
name: Resilience Patterns
type: pattern
solves: [bottleneck-service, lack-of-communication-standards, chatty-communication, service-chain]
sources:
  - https://www.politesi.polimi.it/retrieve/04fb6ce8-cc33-4207-a932-6e0701e8f932/2022_04_ESAS.pdf
  - https://garnetgrid.com/insights/microservices-anti-patterns
  - https://www.designgurus.io/blog/10-common-microservices-anti-patterns
---

## Summary

Resilience Patterns are the rules that stop one failing service from taking down
the rest: timeouts, retries with backoff, circuit breakers, bulkheads, and
fallbacks. They do not fix a bad topology, but they limit the damage while the
topology is fixed.

## How it works

- **Timeouts.** Every remote call has one. A call with no timeout holds a thread
  until something else breaks. Set the caller's timeout shorter than its own
  deadline, so a chain of calls has a coherent budget.
- **Retries with backoff and jitter.** Retry only calls that are safe to repeat,
  cap the attempts, and spread them out. Retries without a cap turn a slow
  service into a dead one.
- **Circuit breaker.** After a number of failures, stop calling for a while and
  fail fast. This gives the failing service room to recover.
- **Bulkhead.** Separate connection or thread pools per dependency, so one slow
  dependency cannot consume all the capacity of the caller.
- **Fallback.** Define what the caller does when the dependency is unavailable:
  cached data, a reduced feature, or a clear error.
- **Load balancing and autoscaling.** For services that must stay central, run
  several replicas and scale on a signal that matches the load.

Write these values into a shared policy, so every service uses the same defaults
instead of inventing its own.

## When to use it

Use them for every synchronous call between services. They are required, not
optional, once a request crosses a process boundary.

## Cost and risks

Fallback behaviour is a product decision, not just config, and it takes real
work per caller. Badly tuned values cause their own incidents: a timeout that is
too short fails healthy requests, and a circuit breaker that is too sensitive
opens under normal load. These patterns can also hide a design problem, so track
how often a breaker opens and treat it as a finding, not as normal.

## Sources

- Design Patterns and Anti-Patterns in Microservices Architecture, Politecnico di Milano, 2022.
- 10 Common Microservices Anti-Patterns, Design Gurus.
