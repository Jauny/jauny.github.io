---
id: 1
title: Sandi Metz at Parisoma
date: 2012-12-25
layout: post
---

If you're a Ruby developer and you havn't read Sandi Metz's book POOTR, shame on you. 
If you havn't heard of her... well shame on you, but trust me, now you know her, you're life is already happier!

Whomever you are, you definitely should read her book. I even told my grand mother to read it, and she said, I quote:
> This shit's crazy, totally changed my life!

So yesterday, Sandi Metz gave a talk about her book at Parisoma. We went with a good chunk of DevBootcamp, and it was nice.
First, well, like every meetups in San Francisco, free beer and pizza. I mean, who doesn't like it?
_I sincerely think that you literally can eat for free every-single-night in San Francisco._

Then, I love that kind of ambiance where you get to a meetup and there is no private room or whatever. Sandi was simply drinking beer and eating pizza with us, and she came to me to talk about DevBootcamp. She stopped the conversation after a few minutes saying she was trying to talk to everyone. That's awesome.

After an hour of meeting new people, eating 9, _yes 9_ slices of pizza and _a few_ beers, we finally sat and Sandi started her presentation.

Here it is; Or at least, what I was able to note down;
_If you read the book, it will sound familiar; It's never bad to refresh your mind about those principles_

### Design
Everyone has his own definition of Design. So let's agree on the definition that will support the coming statements;
One important thing about code is that

1. it needs to work _now_
2. it needs to be easy to change.

Why those 2 assumptions? Because
> The purpose of Design is to reduce the cost of change.

Nothing else. Design is here to reduce costs. And this is a whole hypothesis OO is based on. Easy to reuse, easy to change, so as opposed to procedural code, you end up reusing a lot of the code you already wrote, instead writing the same things over and over again.

### Diagnostic - TRUE code
* __Transparent__ Consequences of change are visible and predictable
* __Reasonable__ Cost of a new feature should be proportionate to its value
* __Usable__ If it's already written, it can be easily reused anywhere else
* __Exemplary__ Is your code good the app or does it make your coworkers hate you?

Why following this TRUE principles?

Because as Antoine de Saint-Exupery said, 
> Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away.

And he is french, so he must be right!

So following the TRUE principles might not help you know when it's perfect, but it will certainly help you know _when to stop_. And it's __when it's good enough__. 

### Balance between abstraction and function
+ __abstraction__ in the code makes it really easy to change, but harder to understand.
+ __functional__ code, in the opposite, is really easy to read and understand, like a story, but is almost impossible to change.

Someone in the audience asked the question, _so how to make the balance between both, and how to do you it's good enough?_

Programming is an art. Some people don't agree with that statement, but it is.
And programmers are artists.
__So don't be scared of your feelings__. The brain is really smart, and most of it is unconsciously working. Which makes it even smarter. You don't have to be aware that it's doing something for it to do so. The problem is, that unconscious part of the brain can't talk. To communicate, it send you feelings. __Good feelings or bad feelings__.
Listen to those feelings. And the more you practice, the more you'll be able to __feel that your code is good enough__.

It's not about what's going in each objects, it's about the space between objects. __Objects need space to function correctly__. The less information each object has about others, the easier it will be to reuse those object outside of the scope in which they were written.

So when you refactor your code, to add abstractions, __just do one refactor less that you want to__. And there will be the perfect balance between abstraction for easy change and functional for easy understanding.

__Sandi Metz's book, [Practical Object-Oriented Design in Ruby](http://www.amazon.com/dp/0321721330), is a must read. Go buy it now, and read it.__
  