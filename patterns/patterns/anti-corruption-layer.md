---
id: anti-corruption-layer
name: Anti-Corruption Layer
type: pattern
solves: [data-driven-migration, distributed-monolith, shared-database]
sources:
  - https://tede.unioeste.br/bitstream/tede/6034/5/Guilherme_Villaca2022.pdf
  - https://assets.ptidej.net/Publications/Documents/EuroPLoP20.doc.pdf
  - https://www.oreilly.com/content/microservices-antipatterns-and-pitfalls/
---

## Summary

An Anti-Corruption Layer is a translation layer between a new service and a
legacy system. The new service works with its own model, and the layer converts
to and from the old one. It keeps legacy naming, structure, and quirks from
spreading into the new design.

## How it works

The new service defines the model it wants. The layer sits at the edge and does
the mapping: renaming fields, converting codes and formats, filling gaps, and
hiding legacy calls behind clean interfaces. All knowledge of the legacy system
stays inside this layer, in one place.

It can be implemented as a module inside the new service, or as a separate
adapter service when several new services need the same translation.

## When to use it

Use it during any migration where new services still read from or write to the
legacy system or its database. Use it also when integrating a third party system
whose model you do not control.

## Cost and risks

It is extra code that provides no direct business value, so it is easy to skip
under pressure, and skipping it is how legacy models end up copied into the new
architecture. The layer can also become a permanent dependency: once the legacy
source is gone, the layer should be deleted, and teams often leave it in place
for years. Set the removal as part of the migration plan.

## Sources

- Villaca, Strategies to mitigate anti-patterns in microservices, UNIOESTE, 2022.
- Richards, Microservices antipatterns and pitfalls, O'Reilly.
