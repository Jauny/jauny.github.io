---
id: 26
title: Declare a class in Objective-C
date: 2013-08-10
layout: post
---

Yesss I started to learn Objective-C. As usual, I will try to write about what I learn here, starting from the very basic, and hopefully writing some more interesting stuff sooner or later!

Something really confusing coming from Ruby, or some other higher programming language, is the need of two files to declare a class.
The first file is the _header_, or __interface__ file. It _declares_ the instance variables and methods.
The second file is the __implementation__ file. It _implements_ each methods.

Let's start with a basic class, and then go through each element.

### Dinosaur.h

```objective-c
@interface Dinosaur : NSObject
{
    int weight;
    int numOfLegs;
}
@property int weight;
@property int numOfLegs;

- (NSString)rawr;
```

First, as explained, the _interface_ file. This is pretty simple and straight forward, it declares the instance variables and the methods. Few points might require clarification tho.

``` @interface Dinosaur : NSObject ```
This says the file is the _interface_ class, and declares the class as being Dinosaur, which inherits from NSObject.

Between the curly braces is the instance variables declaration.

``` @property ```  is to generate setters and getters for the instance variables.
Let me explain.
When you create an instance of an object, in that case an new dinosaur, you will want to set its weight and its numOfLegs, right? Well, the method that you would create for that is called a _setter_.
And after setting some values for those instance variable, you might want to access them to read them, or use them for other methods- this would be the _getter_.
So ``` @property float weight ``` will imply 2 methods:

```objective-c
- (void)setWeight:(int)w;
- (int)weight;
```

The last part is simply declaring a method that this object has, which is ``` rawr ```, which returns a string.

### Dinosaur.m

```objective-c
#import "Dinosaur.h"

@implementation Dinosaur

@synthesize weight, numOfLegs;

- (NSString)rawr
{
    return @"RRRAAAWWWWWRRRRRRRRRRR";
}
```

``` @synthesize ``` is the other half of ``` @property ``` and implies the implementation of the methods for the getters and the setters.
``` @synthesize weight ``` generates this:

```objective-c
- (void)setWeight:(int)w
{
    weight = w;
}
- (int)weight
{
    return weight;
}
```

And finally we have the implementation of the method rawr which simply return a string.

Now, let's use this new class we just built!

### main.m

```objective-c
#import "Dinosaur.h"

// Create a new dinosaur called dino
Dinosaur *dino = [[Dinosaur alloc] init];

// Set its weight and number of legs
[dino setWeight:450];
[dino setNumOfLegs:8];

// Get its weight and number of legs
[dino weight];
[dino numOfLegs];

// Call its methods rawr
[dino rawr];
```
  