---
title: Naming things
date: 2017-11-21
layout: post
---
It's been said that there are only two hard things in computer science; Cache invalidation, naming things and off-by-1 errors.  

Today I'd like to talk about naming things, because it's an issue that is often discussed and regularly comes back biting us. I think both _internal_ naming (variables, functions, packages) and _external_ naming (services, files, paths) are both an issue and closely related. I'll talk about the latter, which I think is less talked about.  

### Names can be fun, but keep them boring

Please, please, please. I've been there. We've all discovered things like Kafka, ZooKeeper, Sidekiq and thought that'd be cool to be the proud owner of such a nicely named service.  
Maybe it is ok to have a cool, original name for an external, open-sourced or SaaS product ([although some would disagree](https://www.expeditedssl.com/aws-in-plain-english)), but for internal stuff, please, _be boring_.  

People feel very strongly about names. They like their pun-intended service names. It's fun and gives excuses to have cute logos.  
Arguments range from supporting that fun names can still make total sense.  
Another argument, which I think is a little more valid, is that descriptive names are too long and end up being reduced to acronymes anyways.  

So "CBFF" wouldn't be better than "Flipr" anuway if we renamed it "Config Based Feature Flags".  

As an example, we have a service that allows for config based feature flags. "Flipr" makes total sense once you know that it allows you to "flip" on and off feature flags on the fly. But if you are searching about _how_ to do so... You'll be more likely searching for "feature flag" and "config" than "flipr".  
Yes, maybe if the service was called "ConfigBasedFeatureFlag" it'd be shorted to "CBFF" - but that's avoidable. Or you can name it "FeatureFlags".  

So keep names explicit, and use those full names. If there is context, then you can use acronyms if it is easier.

### Don't call it by its type

If you are naming a package, don't call it "UserHelperPackage". It is a package, we probably know it, so just call it "UserHelper".  
Same thing if it is a service. "UserStore" is enough. Don't call it "UserStoreService". That would be silly.  

### Keep it consistent

At Uber we use Thrift, and I recently had to migrate to a new service which was named "SomethingStoreService". Its declaration in its thrift file was `service SomethingStoreService`, and the file was located at `.../something-store/something_store.thrift`.  
Now, right there, in one single file, I have 3 names for the same entity. How do I know which to use, when and where? Turns out, because of all those different conventions, I had to use different ones at different places.  
This is what brought me to write this post.  

Keep it consistent and stick to one name. Don't mix dashes and underscores, types and no types.

### No spaces, no underscores, no dashes

And this way, you'll make everyone's life easier.  
Computers are weird and complicated, and those 3 characters make everything an order of magnitude harder.  

Avoiding spaces is kind of obvious - it forces you to use quotes around paths in unix, URLs will have them replaced by their UTF-8 equivalent (%20), etc.  

What about underscores? Well, a lot actually. Did you know that most regex parsers will recognize the underscore as a word character? So Hello_world would be recognized as 1 single word. Google does the same.  

What about dashes? Well, _technically_ they are alright, but that becomes inconsistent when languages _do_ use underscores (for variable/package names).  

So it's just easier to use short, clear names, and when not possible, use multiple words without splitting them. We can all still read "configbasedfeatureflag" and in most places camel case is accepted - "ConfigBasedFeatureFlag" seems pretty damn ok to me.

### Don't rename, version

Lastly, once your perfectly named service gets out of touch and requires a rewrite, do not call is "ImprovedConfigBasedFeatureFlag". Just version it like we do with most softwares. "ConfigBasedFeatureFlagV2". That's it. Easy. Boring.  

So please, _Be boring_.
