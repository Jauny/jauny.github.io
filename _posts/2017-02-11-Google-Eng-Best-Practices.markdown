---
layout: post
title: "Google's Software Development Best Practices"
---

### The famous monorepo
Most of Google's source code is hosted into a single repository, accessible to all software engineers. Only 3 main exceptions: Chrome and Android have their own open sourced repo, and a few high-value or security-critical pieces that have more strict access rules.  
Automated tests are frequently ran, and automatically notify engineers when their code breaks the build. Build status is prominently shown for each teams to put a focus on keeping the build successful. Bigger teams have a "build cop" rotation, similar to oncall, but to help and ensure that build stays green.  
Code ownership is set by a file at the root of each subtree listing the owners. Any engineer can modify any code, but changes have to be approved by an owner.  

In numbers (as of January 2015):  
- 86 terabytes
- 1 billion files
- 2 billion lines
- 35 million commits
- 40 thousand commits/day

### The build system
Google uses a distributed build system called BLAZE, which compiles, builds and runs tests, using a BUILD file for each project.  
Makes it very simple and quick for any engineer to build and test any software in the monorepo.  
It is distributed across thousands of machines, allowing to build and test very quickly.  
Individual build steps are hermetic (they don't have other dependencies that what is declared) allowing the distribution of the build, and deterministic, allowing caching.  This way, incremental builds are fast and can reuse intermediate builds.  
Presubmit checks run test suites when code is submitted for review.  

### Code reviews
Excellent web-based code review tools.  
All changes to the source code has to be reviewed by at least one owner.  
In exceptional case an owner can check in an urgent change before it gets reviewed, but still requires a review.  
There are tools to automatically suggest reviewers.  
Discussions on code reviews are automatically copied and sent over to an email list designated by the project maintainers.  
Engineers are encouraged to keep code reviews as small as possible  

### Testing
Unit testing is strongly encouraged and widely practiced.  
All production code is expected to have unit tests and the code review tool will highlight untested code.  
Integration and regression testing is also widely practiced. Load testing prior to deployment is de rigueur. Teams are expected to provide graphs of how key metrics vary with different rates of requests.

### Programming languages
Google uses four official languages: C++, Java, Python and Go. Each have strong guidelines.  
Commonality of process is key to making development easy. The same commands for checkout, build, tests, etc. are offered no matter what language is used.  
Interoperation between different languages is done mainly using Protocol Buffers.  

### Release engineering
For most teams, the release engineering work is done by regular software engineers. They are done frequently (from daily to weekly), permitted by automating most of the release tasks.  
A release starts with a fresh workspace on a release branch where the software gets built and tests ran. When all tests pass, a first deploy in done on staging servers for more integration testing. Then rollout to canary servers and finally a gradual rollout to the remaining production servers.

### Frequent rewrite
Most software at Google get rewritten every few years. Costly, but also crucial to Google's agility and long-term success, by regularly refreshing the requirements around the software and cutting out complexity that was built over time.


-----------------
_notes taken from [Software Engineering at Google](https://arxiv.org/abs/1702.01715)_
