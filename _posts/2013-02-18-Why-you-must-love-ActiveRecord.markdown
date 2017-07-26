---
id: 7
title: Why you must love ActiveRecord
date: 2013-02-18
layout: post
---

ActiveRecord is the database "management" tool used by Rails. To use a smart term, it's what we call "ORM", or Object-Relational Mapping. What does that mean?

When you start a project, you could decide to do it in Ruby, Python, Javascript, Go, or any other language you want. 
And you could decide to couple this language with a lot of different database; SQL, SQLite, Postgres, MongoDB, etc...

That means that you have to make a lot of different languages work with a lot of different databases, which might have their own languages... pretty messy.
That's when ORM comes in the battle. It's literally a __bridge__ between the two systems, allowing an easy communication. It stands on the language side and deal with the database, but translating everything for you, in the language you are using.

Here is a schema about that, stolen from Jesse, God of DevBootcamp!
![ORM Schema](https://a248.e.akamai.net/camo.github.com/8617e551231b7df753a5e911c52b4e07b22c85d8/687474703a2f2f662e636c2e6c792f6974656d732f32683158343131313277323934353164333930572f5468652532304e61747572652532306f662532304f524d2e706e67)

So... back to ActiveRecord. It's a rails library that does exactly that. ActiveRecord is a Rails library, full of Ruby methods, which, when called, return the correct SQL query, and then, when the database responds, ActiveRecord takes the answer and translates it back to Ruby.

```ruby
client = Client.find(10)
vs
SELECT * FROM clients WHERE (clients.id = 10) LIMIT 1
###
client = Client.last
vs
SELECT * FROM clients ORDER BY clients.id DESC LIMIT 1
```
You can see that even on really simple queries the difference is huge, so I'll let you imagine what it can do for you for bigger queries...
Well, I won't let you imagine long, since I'm gonna talk to you about __SCOPES__

First, a little reminder about ActiveRecord::Relations.  Having an AR::Relation returned when you do a query allow us to chain those queries. 

```ruby
blond_workers = Worker.where(:hair => "blond").class
=> ActiveRecord::Relation
blond_and_blue_eyed_workers = blond_workers.where(:eyes => "blue").class
=> ActiveRecord::Relation
blond_and_blue_eyed_workers.all.class
=> Array
```
So wtf?! When you make a query with ActiveRecord, the query is stored as a relation, and ActiveRecord doesn't actually make the query right away. It waits until the last moment, when it really needs the answer, to call the database. So in the previous example, when we just get the blond workers, we don't do anything with them yet, so ActiveRecord store that relation in the blond_worker variable, but since nothing more is asked, doesn't call the database right away. Allowing us to call more queries on this later. 
Same with blond_and_blue_eyed_workers.
BUT, when we call .all on our Relation, what we do is actually ask to get information on all of those workers, so ActiveRecord need now to query the database to ask for that information and return us all the _workers objects_ with bond hair and blue eyes.

Ok so now, let's get back to scopes. Scope allow us to create _filters_ for queries we would often do. Think of it like methods which return AC::Relations.

```ruby
class Worker < ActiveRecord::Base
  :scope :blond, where(:hair => "blond")
  :scope, :blue_eyed, where(:eyes => "blue")
end
```
Here we created 2 scoped for the Worker model, _blond_ and _blue_eyed_. So next time we want to get our blond and blue eyed workers, we can call it way more easily using those scopes;

```ruby
blond_and_blue_eyed_workers = Worker.blond.blue_eyed.class
=> ActiveRecord::Relation
```
And as you can see, even after chaining scoped, we still get an AC::Relation. Which means we can add scoped after that, of queries, or pure SQL, whatever you want, until you actually use the information inside the relation. Like .all, .first, .each, etc...

There you go, I love ActiveRecord, and anytime I find a query a little too long in my controller, I just make it a scope in my Model, so it keeps my controller cleaner and more understandable :)

I recommend also to check Squeel, an amazing gem allowing even easier syntax than Rails 3 for queries!
  