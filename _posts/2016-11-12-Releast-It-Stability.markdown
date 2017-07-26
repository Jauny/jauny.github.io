---
title: Building Stable Systems
date: 2016-11-12
layout: post
---

It is impossible to build a system that is 100% stable, available and bug free.
Humans will make mistakes. Machines will break. The internet will go offline.
Sometimes you will break things that are under your control, and some other times, things outside of your control will break.

The point is, things will break, you can't avoid it, so instead of denying it you should build your systems taking this into account, and make sure that you buid stability.

When getting a failure, some components of the system will start failing before everything else does. The original trigger and its spread to the rest of the system is called a "failure mode".
You can build crack-stoppers to protect your system and avoid propagation of those failures.

You need to decouple as much as possible the different parts of the system to reduce dependencies and triggers to spread across the systems.

So the first question is, what can happen anyway? A lot, but here is an overview of the main things that you should keep in mind when designing and building software, from MVP to large scale systems.

### Definitions
**Impulses** A rapid shock to the system  
**Stress** A long strain on the system  
**Stability** Being able to keep processing requests despite impulses and stress  
**Failure Mode** The way (or 'mode') in which something might fail  

## Stability anti-patterns, or WTF can happen?
Today, systems are bigger than what they used to be, which means new and bigger challenges. Tightly coupled systems are the rule.  
Their size and complexity push us toward the "technology frontier" where moving cracks rapidly turn into full-blown failures.  

### Integration points
Softwares are a set of systems integrated together. From the web frontend, to the web server and the CMS, connecting to the database, etc.  
Integration points are the number one killer of systems. Every socket, process pipe or remote procedure call will refuse connections, hang, disconnect, etc.  
This is especiall true in services oriented architecture when you have exponentially more services talking to each others.  

- Every connection will fail
- Many forms of failures and errors
- Failures in remote systems quickly become your problem

### Chain reactions
As you scale horizontally, you end up with multiple servers, doing the same thing and sharing the load, behind a load balancer.  
If the connection between the load balancer and a server breaks, or if a server fails because of some load related failure, the remaining servers need to handle the additional load.  
With each server that breaks, the remaining servers are more likely to also go down.  

- One server down jeopardizes the others
- Resource leaks are often a cause and risk increases as servers go down
- Same for race conditions

### Cascading failures
Service oriented architectures comprise of a collection of services that are interconnected to each others and form layers. Or nodes in a directed graph.  
Failures start with a crack. A crack comes from a fundamental problem in one of the layers. A cascading failure happens when a crack in one layer propagates to another layer, and eventually bring the whole system down.  
Just as Integration Points are the number one source of cracks, cascading failures are the number one crack accelerator.  

- Main accelerator of cracks propagation
- Result in drained resource pools
- Defend with timeouts and circuit breakers

### Blocked Threads
The majority of system failurs do not involve outright crashes. Those are pretty easy to debug and fix.  
Usually you see a process run and do nothing, because every thread is blocked waiting on some process that never ends or response that never comes.  
Blocked threads can happen anytime you check resources out of a connection pool, deal with cache or make calls to external systems.  

- Leads to chain reaction and cascading failures
- Usually happens around resource pools (db etc)
- Defend with timeouts

### Attack of self denial
Those happen when the system self-conspire against itself.  
For example, the stress happening during a big marketing campaign bringing a lot of traffic to an e-commerce website.  

- Keep good communication across the company, so you can prepare for such surge in traffic.
- Protect shared resources  
Don't let high loads on the front-end affect the back-end.


### Unbounded result sets
Those happen when you play with sets of data that are bigger than you expect. Querying all rows from a database could eventually return an infinite amount of items that would slow your processing quite a bit. Sometimes, the amount of data can become so big that it won't even hold in memory, and break your system. Always keep that in mind and make sure that you set limits when querying data.

- Use realistic data volumes
- Don't rely on data producers
- Put limits into other app-level protocols

### Slow responses
Slow responses generate cascading failures because each process left handing is blocking a thread. For client-facing assets, such as a website, it causes a surge in traffic because visitors will likely spam the refresh button if the request is too slow.

- Fail fast
- Hunt for memory leaks

### SLA Inversion
Every single dependency of your system is an integration point that can break. This means that your SLA can only be as good as the total SLA of your dependencies. If you have 2 dependencies that have each a SLA 99.99% of availability, that means that you can't offer more than 99.98% of availability.

- Don't make empty promises
- Examine your dependencies
- Decouple your SLAs
Ensure resiliency when a dependency fails

## Stability Patterns, or How to ensure resiliency?

### Timeouts
It is essential to have a timeout on any resource-blocking thread. TCP, Database connections, etc.  
Timeouts can often be coupled with retries, but it's not always a good decision. Make sure to add retries only when it makes sense. Too many retries will also make threads hang longer and clients wait more.

- Apply timeouts to integration points, blocked threads and slow responses
- Apply to recover from unexpected failures
- Consider delaying retries
Most timeouts involve a problem with the network or remote system that won't be resolved right away, in which case immediate retries are liable to hit the same problem.

### Circuit breaker
A circuit breaker is a wrapper that circumvents calls when a system is not healthy. It's the opposite of a retry since it prevents additional calls rather than execute them.  
Once the number (or frequency) of failures reaches a threshold, the circuit breaker "opens" and fail all consequent calls.  

It's a very efficient way to automatically degrade functionality when a system is under stress.

- "Don't do it if it hurts" principle
- Use it coupled with time outs
- Expose, track and report the state change
Opening a circuit breaking always indicates a serious problem, so make sure to always be alerted when this happens.

### Bulkheads
A bulkhead is an upright wall within the hull of a ship that partitions it into water resistant compartment preventing the ship to sink or be waterboarded in case part of the hull is broken open.  
The same technique can be employed with your software, so when part of it is under stress and breaks, the rest of your systems continue to function.  

- Pick a useful granularity (threads, CPUs on a server or servers in a cluster)
- Bulkheads are very important in a service oriented architecture
- You have to accept a less efficient use of resources (harder to dynamically allocate needed resources if they are not shared)

### Steady state
Every time a human touches a server is an opportunity for unforced errors.  
Keep people off the production servers as much as possible by automating regular maintenance tasks.  

Any mechanism that accumulates resources must be drained at some point, and at a faster pace than it accumulates those resources, or it will eventually overflow.

Steady State patterns say that for every mechanism that accumulates resources, some other mechanism must recycle those resources.

**Data purging**  
Sounds like a high-class problem, but at some point your database will start having issues, such as increased I/O rates, latencies, etc.  
Being able to purge data from it while keeping your systems running is hard and you need to be prepared for it.

**Log Files**  
Logs accumulate very quickly and take up disk space. Last week's log files are already not very interesting, so anything older than this is pure garbage.  
At some point they'll fill up their containing file system and jeopardize the whole app with ENOSPC errors.

If you need to save logs (to stay compliant with financial information for example), then back up your logs in a separate machine meant for this.

**In-memory caching**  
Same as logs and databases, caching takes up valuable memory from the server. Make sure to set up correct TTL on your cache so it gets regularly purged and useless cache is not blocking any crucial memory for anything else.

### Fail fast
Just like slow responses, slow failures are very bad, because you end up using resources for nothing.

- Inform the caller of a failure as early as possible
- Verify integrity points early  
If a dependency is down, a circuit breaker is open, etc., then you should not even try to operation.  
- Validate input early  
Don't build models, load data from your database, etc., to finally fail because the user input is invalid. Validate first.  

### Handshaking
Handshaking is all about letting two devices that communicate know about each other's state and readiness. It create cooperative demande control.  
It may add an additional call to check a dependency's health, which is additional time and resources needed, but is usually less costly than a failing call.  

### Integration testing
Unit tests are good and you should strive for 100% coverage, but even then, you won't be testing everything, because unit tests are meant to test what is expected from your services. They do "in spec" testing.

An integration testing environment is meant to replicate the production environment, and break it in unexpected ways that unit testing are not covering. It helps testing failures such as network transport and protocol, application protocol and application logic.

- Emulate "out of spec" failures
- Stress the caller with slow responses, no responses, garbage responses, etc.
- Supplement, don't replace
Integration testing is meant to augment your other testing methods, not replace them.

### Middleware
Middleware occupies the essential interstices between systems that were not meant to work together.  
Done well, it simultaneously integrates and decouples systems.

- Integrates them by passing data and events between the systems
- Decouples by letting systems remove specific knowledge of the other systems

There are synchronous middlewares that force the systems to hang and wait. They can amplify shocks to the systems, but sometimes are necessary (such as authorizing a credit card during a transaction).

Some, less tightly coupled middlewares allow calling/receiving to happen at a different time and place, such as a pub/sub messaging system.  
But those are sometimes less useful or harder to deal with.

- Decide early  
Those are big architectural decisions that are harder to change  
- Avoid failures through decoupling  
Decoupled apps are more adaptable and less prone to cascading failures  
- Learn many, choose one  
There are no silver bullets, so you need to know multiple architures and choose which fits best your case.


## Summary
No matter what you do, shit will happen in the most unexpected ways.

Avoiding stability anti-patterns will help minimize bad things happening, but never fully prevent them.  
Apply stability patterns as you need to protect your systems from going completely down when bad things happen.  

Be cynical, be paranoid; In software development, this is a good thing.

_Those were my notes for Part I: Stability, of "Release It!"._
