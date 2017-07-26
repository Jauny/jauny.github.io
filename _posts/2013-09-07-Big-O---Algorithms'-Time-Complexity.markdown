---
id: 27
title: Big-O - Algorithms' Time Complexity
date: 2013-09-07
layout: post
---

One of the most important thing to think about when developping an algorithm is its time complexity. Or, in other words, how long this algorithm will take to run, depending on the size of the data.

When analysing an algorithm's time complexity, there are 3 scenarios to consider;

1. __Best-case__: When the data is in the best form possible when the algorithm is used, making it as efficient as it gets.
2. __Average-case__: The average run time that is expected for the algorithm in most cases.
3. __Worst-case__: When the data is in the worst form, making the algorithm as slow as it gets. This is the case that is often used to _rate_ the time complexity of an algorithm.

### Best-case scenario

Provides insights on the optimal circumstances for the algorithm. For example, think about a sequential search.

A simple implementation of a sequential search would be to iterate over each element of an array until it finds the value it's looking for and return true - or false if the value isn't present.

The best-case scenario for such an algorithm would be if the value _v_ we are looking for is the first element of the array.

No matter the size of the data, the _time complexity_ would always be 1, which we write __O(1)__, read "big O 1".

You can see already how this scenario is rarely used - it is not representative enough of the real efficiency of our program.
Yet, if you know in advance what the data will look like, this scenario is interesting, allowing you to find the most efficient algorithm for you specific case.

### Average-case scenario

Let's say we have a collection __Sn__ of _n_ sets of data, __Si__ being a set of data of random size such that __Si∈Sn__.
Calculating the average-case scenario consists of giving a probability __Pr__ to each __Si__ in the way that:

![image of sum of Probabilities](http://i.imgur.com/OBvSLEr.png)

We then calculate __T__, the average time spent on each Si, __t(Si)__, weighted by probabilities.

![image of Tac](http://i.imgur.com/py0Iqlh.png)

Average case scenario is useful when you are not sure what the data will look like, and expect to have a lot of of it. Your main objective here is to find an algorithm that is as efficient as possible, as often as possible, and you can deal with edge cases where it will be (too) long.

### Worst-case scenario

This is the most often used scenario to compare algorithms, because it allows to know what can happen in the worst case.
For __Sn__, the worst-case is the max __t(Si)__ for __Si∈Sn__, denoted:

![image of worst-case](http://i.imgur.com/Rkmonlw.png)

In addition of being the most used for comparing algorithms, sometimes you can't do anything without knowing the worst case scenario.
Imagine you are an open-heart surgeon, even if you find a way to operate that is really efficient and risk-less, say, 98% of the time, but the patient dies the other 2%, well, even if the 98% performance is incredible, you just cannot accept the death of the patients 2% of the time!

So you need to thoroughly analyze the worst-case time complexity of your algorithm if you absolutely need something efficient 100% of the time.
  