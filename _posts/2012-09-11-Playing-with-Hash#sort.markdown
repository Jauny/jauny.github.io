---
id: 3
title: Playing with Hash#sort
date: 2012-09-11
layout: post
---

# Sorting a Hash

I wanted to understand what happened under the hood when hash.sort is called;

```ruby
hash.sort { |a, b| b[1] <=> a[1] }
```
If you can't answer, you might want to read.
***

First, let's begin by saying that we will be working on this hash

```ruby
hash = {"one"=>1, "two"=>2, "three"=>3, "four"=>4, "five"=>5}
```

##Hash#keys and Hash#values
A simple way to sort a hash keys or values is to use the methods Hash#keys and Hash#values.  
Those 2 methods are simply returning an array of the keys or the values of your hash.  So as soon as you get an array with only one of the type of values you want to work with,  it's all good!

```ruby
hash.keys
=> ["one", "two", "three", "four", "five"]
hash.values
=> [1, 2, 3, 4, 5]
```
With those arrays, it's then easy to sort them;

```ruby
hash.keys.sort
=> ["five", "four", "one", "three", "two"]
hash.keys.sort.reverse
=> ["two", "three", "one", "four", "five"]
```

"All that is incredible!", you may say. But in fact, not that much...

You got your keys or values sorted, that's amazing, but what happens if you want to sort your whole hash, keeping your keys and values paired? Well, we can use Hash#sort_by

```ruby
hash.sort_by { |key, value| key }
=> [["five", 5], ["four", 4], ["one", 1], ["three", 3], ["two", 2]]
hash.sort_by { |key, value| value }
=> [["one", 1], ["two", 2], ["three", 3], ["four", 4], ["five", 5]] 
```
Ah! That's a bit better, at least we get to choose wich element it will be sorted by. But we still don't have a choice in the order of the sort, and it will simple order it in an increasing order. We could call .reverse on it, but it's not really sexy.

##Enumerable#<=>

```ruby
hash.sort { |a, b| b[1] <=> a[1] }
=> {"five"=>5, "four"=>4, "three"=>3, "two"=>2, "one"=>1}
```
But, WHAT is that?! A smaller-than-equal-bigger-than symbol?!  
Why yes, almost! It's super complicated, but in our situation, we could call it a smaller-than-equal-OR-bigger symbol. Hmmm...!

So basically, their is a reason why we've been getting an array in return of our sorted hash. When Ruby calls a sort method, it transforms the hash into nested arrays of 2 elements, representing the pairs [key, value].

It then compares the first pair with the second, and switches them if needed. Then compares the second with the third, and again and again.
So because Ruby is lazy, it doesn't bother changing back the array into a hash. Not cool!

So how does our <=> works? It compares two elements, and returns either -1, 0 or 1.

```ruby
"a" <=> "b"
=> -1
"3" <=> "1"
=> 1
```
So when we call hash.sort, Ruby instantly transforms the hash into nested arrays of key-value pairs, and then checks the arguments;
It will then compare the arguments with <=> and switch them if it gets 1, or do nothing if it gets -1 or 0.
So here is what happens in the example;

```ruby
hash.sort { |a, b| b[1] <=> a[1] }
```
Hash#sort will first transform our hash into an array looking like that :

```ruby
[["one", 1], ["two", 2], ["three", 3], ["four", 4], ["five", 5]]
```
It them assigns the first and second elements to a and b; a = ["one", 1] and b = ["two", 2] and compares their own elements at position 1 with <=> in the order we gave, b <=> a
b[1] = 2 and a[1] = 1

```ruby
b[1] <=> a[1]
=> 1     # because it is bigger, remember?
```

In that example, because Hash#sort got 1 in return, it switches the elements in the array.  
So we end up with

```ruby
[["two", 2], ["one", 1], ["three", 3], ["four", 4], ["five", 5]]
```
It then continues the loop by doing the exact same thing, that time assigning the second and the third elements to a and b;

```ruby
a = ["one", 1], b = ["three", 3]
b[1] <=> a[1]     # b[1] == 3, a[1] == 1
=> 1
```
It returns 1 again, so the elements get switched again!

```ruby
[["two", 2], ["three", 3], ["one", 1], ["four", 4], ["five", 5]]
```
And it will just continue like that until all is sorted like we asked!

##UPDATE
Imagine you have a hash of key and values, where the values are objects with attributes.  
For example, students with names; You could call first_student.name and it would return its name, right? Check that:  
Let's say the hash looks like that;

```ruby
class = { 1 => first_student, 2 => second_student, 3 => third_student, 4 => fourth_student }  
```
How would you do if you wanted to sort your array in descending order of student's name? EASY!

```ruby
class.sort { |a, b| b[1].name <=> a[1].name }
```
Yes sir! You can even go get an attribute in the nested array's element you want! So here, for example, a[1] represent the object student, so you can call the attribute name on it. Ruby will then be able to sort your objects per name's descending alphabetical order!

##Why is it so powerful?
It is, because you have so much power through that block!  
When you write { |a, b| a[1] <=> b[1] }, the order of a[1] <=> b[1] or b[1] <=> a[1] controls the order of the sort, and the index given controls which element you sort with, either the key or the value!
  