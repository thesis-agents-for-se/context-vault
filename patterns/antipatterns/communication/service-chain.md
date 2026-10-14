---
id: service-chain
name: Service Chain
category: communication
aliases: [Long Chain of Responsibility, Deep Call Chain, Service Fan-Out Chain]
severity: high
detects_on: [code, traces]
signals:
  - One request passes through four or more services in a straight line.
  - Each service in the path adds a small step and calls the next one.
  - Total latency for a request is close to the sum of many small calls.
  - A failure in the last service in the path breaks the whole request.
  - Timeouts are set so the outer timeout is shorter than the sum of inner ones.
related: [chatty-communication, nano-service, bottleneck-service]
solutions: [service-granularity-refactoring, saga, event-driven-integration]
sources:
  - https://arxiv.org/abs/1908.04101
  - https://algomaster.io/learn/microservices/anti-patterns-reference
  - https://stackandsystem.com/series/microservices/microservices-antipatterns
---

## Summary

A Service Chain is a long line of services that must each call the next one to
answer a single request. Service A calls B, B calls C, C calls D, and only then
does the answer travel back. Each link adds latency and one more point of
failure.

## Why it hurts

Latency and failure both add up along the chain. The caller at the front has no
way to know which link is slow without a trace. Timeouts are hard to set,
because each service must allow less time than the one before it, and teams
rarely coordinate this. A chain also hides ownership: no one service knows the
full business flow, so the rules end up scattered.

## How to spot it

- Read distributed traces and measure the depth of the span tree, not just the
  number of spans. Depth of four or more is the signal for Service Chain.
- Follow the code from the entry point. If each handler's main job is to call
  the next service and pass the result along, the chain is in the code.
- Compare the timeout configured at the edge with the sum of inner timeouts. A
  mismatch means nobody designed the chain as a whole.
- Look for services that only transform a payload before forwarding it.

## Solutions

### 1. Merge the steps that belong together

- **Do:** Collapse neighbouring steps that always run in the same order and have
  no separate scaling or ownership needs into one service.
- **Fits when:** The chain came from splitting one business process into too
  many parts.
- **Cost:** The merged service is bigger and takes on more responsibility. Keep
  its modules clean.

### 2. Replace the chain with orchestration

- **Do:** Put one orchestrator or workflow engine in charge of the flow. It
  calls each step directly, so the depth stays at one level instead of many.
- **Fits when:** The flow has real steps with business meaning, and you need to
  see and retry each one.
- **Cost:** The orchestrator holds business knowledge and can become a
  `bottleneck-service` if it grows without limits.

### 3. Break the chain with a queue

- **Do:** For the part of the flow that does not need an answer right away,
  publish a message and return to the caller. The rest of the chain runs in the
  background.
- **Fits when:** The client only needs an acknowledgement, such as "order
  accepted".
- **Cost:** The client needs a way to check the final result, and failures now
  need retries and a dead letter queue.

## Related

Service Chain and `chatty-communication` often appear together: one is deep, the
other is wide. Both are common when the system has `nano-service` problems.

## Sources

- Taibi and Lenarduzzi, Microservices Anti-Patterns: A Taxonomy, 2019.
- Microservices Anti-Patterns: Complete Reference, AlgoMaster.
- Microservices Anti-Patterns series, Stack and System.
