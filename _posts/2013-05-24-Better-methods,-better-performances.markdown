---
id: 16
title: Better methods, better performances
date: 2013-05-24
layout: post
---

This is just a quick post to talk about how small changes can make a big difference.

Sometimes, a simple change of built-in method can make a big difference in your application's performance, just because of the way it works, it's ran or the underlying SQL is written.

Let's take a quick example in ActiveRecord.

__.present?__ vs __.exists?__

```ruby
$ User.where(first_name: "Jonathan").present?
  (3.7ms)  SELECT COUNT(*) FROM "users" WHERE "users"."first_name" = 'Jonathan'
  
$ User.where(first_name: "Jonathan").exists?
  User Exists (42.9ms)  SELECT 1 AS one FROM "users" WHERE "users"."first_name" = 'Jonathan' LIMIT 1
```

So as you can see, using __.present?__ queries the database for a COUNT, which means it first gets ALL users with first_name: "Jonathan", then counts them, then checks if COUNT > 0.

Versus __.exists?__ which, instead, SELECT the first row where first_name is Jonathan. As soon as it gets one, it stops, and returns true.

BUT JO, OPEN YOUR EYES, ```.present?``` TAKES 3.7ms and ```.exists?``` TAKES 42.9ms. FOURTY-TWO! STUPID FRENCH!

I though so, but then look at HOW IM RIGHT AGAIN!

```ruby
EXPLAIN ANALYZE SELECT COUNT(*) FROM users WHERE "users"."first_name" = 'Jonathan';
ggregate  (cost=8.80..8.81 rows=1 width=0) (actual time=3.105..3.105 rows=1 loops=1)
   ->  Seq Scan on users  (cost=0.00..8.80 rows=1 width=0) (actual time=3.101..3.101 rows=0 loops=1)
         Filter: ((first_name)::text = 'Jonathan'::text)
         Rows Removed by Filter: 64
 Total runtime: 3.206 ms

EXPLAIN ANALYZE SELECT 1 as one FROM users WHERE "users"."first_name" = 'Jonathan';
Seq Scan on users  (cost=0.00..8.80 rows=1 width=0) (actual time=0.026..0.026 rows=0 loops=1)
   Filter: ((first_name)::text = 'Jonathan'::text)
   Rows Removed by Filter: 64
 Total runtime: 0.043 ms
```

DAMN RIGHT, for some reason my console printed 42.9ms for what is, in fact, 0.043ms! So, it's almost 100x faster.

__Damn. Right.__

So as a conclusion, listen to your mom, brush your teeth before going to bed, and make sure you know the implications of every methods you use. It could save your life. Ok, maybe just your performances. But sometimes, it's related.
  