# Package development best practices

As our web apps (both internal and external) are becoming larger and more complex, we've been taking a more 'service oriented architecture' to allow us to break down complexities and keep our different code bases smaller.  

Keeping code bases smaller has allowed us to move faster (builds, test, deploys, lower cognitive load, faster onboarding) and more safely (less things to break, easier to test, easier to monitor and debug).  

But this doesn't come for free - Splitting an app in two will require you to re-implement a lot of things twice. Auth systems, session management, RPC, databases, tracking/logging/monitoring, etc.  

At Uber, we have a Web Platform team building an in-house nodejs framework called Bedrock. It's an Expressjs wrapper that includes most of the things I just mentionned. It makes product engineers' lives way easier when it comes to bootstrapping a new service. Almost as easy as pressing a button, nowadays.  
They are also building and maintaining Superfine, our frontend framework. It uses React and offers a suite of styles components. Again, this makes product engineers faster by giving them most things already built. You can see this as an internal Bootstrap on steroids. If I need a modal, I can somply `npm install --save @uber/superfine-modal` and use it. It will already be styled and will be plug and play in my app.  

But what happens if I need to use a date picker, and none exists? Well, I face the choice to go see the Web Platform team and ask them to make one for me. They'll eventually do it, but unlikely that it'll be done in time for my needs, because they have their own roadmap.  
I can decide to just build one in my project. Easy and fast. But then if another app needs a date picker, the same problem will be faced again and again.  
The last solution is for me to build a date picker, package it and integrate it into superfine, so other teams can use it and contribute back.  

This sounds great, but has challenges.  
First, I'm a product engineer, I'm used to work on my main app, I have a deadline and 

