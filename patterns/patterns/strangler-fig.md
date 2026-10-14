---
id: strangler-fig
name: Strangler Fig
type: pattern
solves: [distributed-monolith, mega-service, data-driven-migration]
sources:
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://www.politesi.polimi.it/retrieve/04fb6ce8-cc33-4207-a932-6e0701e8f932/2022_04_ESAS.pdf
---

## Summary

Strangler Fig is a way to replace a system in small steps instead of all at
once. You put a routing layer in front of the old system, move one capability at
a time to a new service, and switch traffic for that capability. The old system
shrinks until it can be turned off.

## How it works

1. Put a facade in front, usually a gateway or a reverse proxy, so clients stop
   calling the old system directly.
2. Pick one capability. Prefer one that changes often and has few incoming
   dependencies.
3. Build it as a new service with its own data.
4. Route a small share of traffic to it, compare results, then move the rest.
5. Delete the old code for that capability. This step is often skipped, and the
   migration then never ends.
6. Repeat.

During the move, the new service may still need legacy data. Use an
`anti-corruption-layer` so the old model does not leak into the new design, and
decide clearly which side owns the data while both are live.

## When to use it

Use it when the system is in production, a rewrite is too risky, and the business
cannot wait for a long migration with no delivery. It is the default approach for
monolith to microservices work.

## Cost and risks

Two systems run at once for a long time, which costs money and attention. Data
must be kept in sync during each cutover, and that sync code is temporary but
easy to forget. The biggest risk is stopping halfway: the old system stays, the
new services depend on it, and you end up with a `distributed-monolith`. Track
the retirement of old code as part of the plan, not as cleanup.

## Sources

- Richards, Microservices antipatterns and pitfalls, O'Reilly.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
