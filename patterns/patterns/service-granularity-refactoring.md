---
id: service-granularity-refactoring
name: Service Granularity Refactoring
type: pattern
solves: [nano-service, mega-service, wrong-cuts, service-chain, shared-libraries, bottleneck-service, cyclic-dependency, esb-misuse]
sources:
  - https://stackandsystem.com/series/microservices/microservices-antipatterns
  - https://algomaster.io/learn/microservices/anti-patterns-reference
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
---

## Summary

Service Granularity Refactoring means changing the size and number of services
after they exist: merging ones that are too small, splitting ones that are too
big, and moving responsibilities so each service owns a whole job. The first
split is rarely right, so this is normal work, not a failure.

## How it works

Use evidence to decide:

- **Change coupling.** Services that appear in the same commit or release again
  and again should probably be one service.
- **Call frequency.** Services that always call each other for a single use case
  are candidates for merging.
- **Ownership.** Two teams sharing one service is a reason to split. One team
  owning twenty services is a reason to merge.
- **Scaling profile.** Parts with very different load or cost profiles are worth
  keeping apart.

The moves available:

- **Merge** small services that ship together into one, keeping clear internal
  modules so the result does not become a `mega-service`.
- **Split** a large service along its internal packages or table groups, one
  capability at a time.
- **Move a responsibility** from a central service to the service that owns the
  outcome, which is the main fix for a `bottleneck-service`.
- **Extract to a library** when the logic is stateless and does not need its own
  deployment. Version it properly.
- **Extract to a service** when shared logic must change in one place for
  everyone, such as pricing rules.

## When to use it

Use it when metrics or incidents show the boundaries are wrong, and after a
migration has run long enough for real usage patterns to appear.

## Cost and risks

Merging and splitting both touch data, which is the expensive part. Each move
needs a migration plan and a rollback path. Doing this without domain input just
rearranges the same wrong boundaries, so pair it with
`domain-driven-decomposition`.

## Sources

- Microservices Anti-Patterns series, Stack and System.
- Microservices Anti-Patterns: Complete Reference, AlgoMaster.
- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
