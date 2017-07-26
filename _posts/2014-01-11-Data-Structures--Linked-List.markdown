---
id: 29
title: Data Structures- Linked List
date: 2014-01-11
layout: post
---

A linked list is a data structure in which elements are arranged in linear order (like an array).
But unlike an array, where the order is determined by the _index_ of each element in it, the order in a Linked List is determined by a pointer (or multiple ones) in each element of the list.

There are multiple types on Linked List, but here, I'll use a Doubly Linked List.

In a __Doubly Linked List__ L, each element has 3 attributes;

* __key__, which represents the data,
* __next__, a pointer to its successor, and
* __prev__, pointing to its predecessor.

For an element E, ```E.prev == nil``` means E is the list's __head__. The first element in the list. On the contrary, ```E.next == nil``` means E is the __tail__. The last element of the list.

Here is what an Element would look like:

```ruby
class Element
  attr_accessor :key, :prev, :next
  
  def initialize(args)
    @key = args[:key]
    @next = args[:nex]
    @prev = args[:prev]
  end
end
```
And here are 2 elements, one being the head.
As you can see, ```head.next``` points to tail and ```tail.prev``` points to head.

```ruby
head = Element.new key: 13
tail = Element.new key: 25, prev: head
head.next = tail
```

This is a really simple implementation of Element. Here I create the element and link them manually.

Our list needs its own class to implement basic operations such as

* ```insert``` to add an element (element becomes the new  head)
* ```delete``` to remove en element
* ```search``` to look for an element
* ```minimum``` and ```maximum``` to find the smallest and biggest element

Here would be an implementation of that class:

```ruby
class LinkedList
  attr_reader :head
  
  def initialize(element=nil)
    @head = element
  end
end

head = Element.new key: 13
list = LinkedList.new head

list.head 
=> #<Element:0x007f878aafc198 @key=13, @next=nil, @prev=nil>
```
The list is initialized with an element which becomes the head (and the tail being the only element). The element can be nil, in which case the list would be empty.

Now let's create the ```insert``` method, to allow us to add new elements to the list:

```ruby
def insert(element)
  el.next = @head
  @head.prev = el if @head
  @head = el
end
```
So what exactly is happening here?

1. The new element's _next_ attribute is set to point to the list's current head (insert adds elements in front of the list, remember?),
2. list head's _prev_ is set to point to our element, and
3. our list's ```@head``` is set to our new element.

![Add element to linked list](http://i.imgur.com/SMLwddC.png)

As you can see, in this example we had a linked list where the head is 9. We ```insert```ed the element with ```key: 25```, which becomes the new head.

On the opposite, let's now implement ```delete```, which will allow us to remove an element from our list:

```ruby
def delete(element)
  el.prev ? el.prev.next = el.next : @head = el.next
  el.next.prev = el.prev if el.next
end
```

1. On line 1, we check if the element has a predecessor by checking if its ```.prev``` exists. If it does, we set its predecessor ```.next``` to point to our element's successor. If our element doesn't have a predecessor, it means it's our list head. In that case, we set the head to point to its successor.
2. Then, we do the exact opposite; Unless our element is the tail, we set its successor to point to its predecessor.

![Delete element from linked list](http://i.imgur.com/xk5nwFs.png)

As you can see, in this example we removed 4. Hence, ```16.next``` now points to 1 and ```1.prev``` points to 16. No more 4.

Finally, let's implement ```search```, allowing us to find an element from a key in the list (makes more sense to look for a key than an element). 
If the element we are looking for is not in the list, we will return ```nil```:

```ruby
def search(key)
  x = @head
  while x && x.key != key
    x = x.next
  return x
end
```

Here the search works like a _sequential search_. It starts from the head, it iterates over every element until it finds an element with the key we are looking for. 
If no element has the key we are looking for, it will iterate until the last element of our list, which has ```.next == nil```, which will be returned.

Here. I'm done with Linked List.

This is obviously a really simple implementation in ruby, which I do for learning purposes. 

__Other types of linked lists__

* __Singly Linked Lists__ are linked lists where nodes have only one pointer, to its _successor_.
* __Sorted Linked Lists__'s linear order corresponds to the linear order of keys stored in elements of the list (e.g. 1->2->3->4).
* __Circular Linked Lists__ have the _prev_ pointer of the head point to the tail, and the tail's _next_ pointer point to the head.

_Both images are screenshots from the incredible book "Introduction to algorithms, 3rd edition" written by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein._
  