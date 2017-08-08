---
title: Analysis Paralysis
layout: post
date: 2017-07-13
---
When building software, one of the important thing is having a great vision and build a system that will survive and stay relevent as long as possible.  
Because of that, before actually starting to write software, there is a long, important and necessary process of preparation that has to happen.  
Design, architecture, user research, RFC amongst other are all part of this process. It is important, because you want to make sure you are heading towards the right direction and know exactly why and how you will build what.  
Once this is done (read multiple people gave their opinion and agreed on something), you can start scoping your work by prioritizing all the features you want to build and go ahead with your MVP, v1, etc. This is all pretty basic Agile or Lean software methodology.

But today I want to talk about what comes before that: You know what problem you need to solve. It is a pretty big problem, and you'll need to build a pretty major architecture. Chances are it will end up split into multiple services and the whole (distributed) system will have multiple consumers, has to work across data centers (be all active), ensure a certain SLA, scale to a certain amount of data, etc.  

This is what we are currently facing on a team at Uber; Since we added the first system to allow riders to add a payment method, 8 years ago, our needs have changed a lot.  

- We've added additional payment methods
- We've added multiple ways to pay (credit, split fare)
- We've changed the rider-partner relationship (Uber pool)
- We've added more relationships (u4b, uberFreight, uberRush, uberEats)
- We're facing additional and more complex regulations (we've grown, we've expended to more countries, etc)
- We've moved from a monolith into a single dc to a service oriented architecture across multiple dc

So we've got to a point where our payment systems are hard and expensive to maintain and decided to rebuild everything from scratch. This means that we are working on a very complex architecture challenge where we need to answer all needs previously stated, and more. And since it's going to be a very long process, we want to build something that will survive years. This means we are faced with taking decision that have to be the right ones. Or do we?  

When faced with such basic, but crucial and long term decisions such as "which language should we use between java and go?", "which database should we use between cassandra and schemaless?", "which architecture principles should we use between sync and events based?", we tend to have a lot of trouble moving forward, because those are extremely hard to make decisions.  
As engineers, we want to gather all information we can to make an educated and confident decision on what to use, because we know it will possible affect how long our system will survive and don't want to face another situation where we need to migrate towards another technology.  
The problem with this approach is that when making such decisions, no silver bullet exists. We are finding great arguments for both Go and Java, both schemaless and cassandra and both sync and events. We keep getting more information, talking to convincing people defending one way or another and will never reach a comfort level allowing us to take a decision with 100% confidence that this is the right choice.  
One reason is because the environment in a big company like Uber makes it very hard to get 100% of real, updated information on all technologies available. The second is that, we can't (and will never be able to) see the future. And nobody can. So what is true today might change.  

Being incapable of getting enough confidence to take a decision puts the team in Analysis Paralysis. We keep talking to more people, we keep discussing the different solutions, update docs, etc., hoping to get to convidence at some point. But we never reach confidence and will never do, and this prevents us from taking a deicsion since everyone wants to make the right decision.  
As Jeff Besos explains it with his concept of Day 0, you need to learn to be ok with taking decisions without confidence. You'll never reach nore than 70% of the information you need for a confident decision, so at some point, you need to make a decision knowing it might not be the perfect one.  

A bad decision is better than no decision at all. A bad decision will give you information at some point. No decision makes you stagnate and not move forward. Analysis Paralysis is the worst that can happen to a team.

So to avoid that, you need to timebound your decision taking, and once the bound is reached, if no decision was taken, you need to make a decision with the information you have. No matter how much more information you think you can get with more time doesn't matter. You need to take a decision, period. If the current information gives a perfect tie between the different solutions, pick one randomly and go for it.  

What you need, is be comfortable with your decision, not with your solution. If you have invested enough energy and your best intentions to pick the best solution, then you'll have enough arguments and data to justify your choice by comparing the available information. In case of a mistake, embrase it, and see the failure as additional, extremely valuable new information that allows you then to make a new, more informed and more confident solution that wasn't previously possible.  

No matter how hard or scary it is, fight against Analysis Paralysis. A bad decisions is always better than no decision.  
