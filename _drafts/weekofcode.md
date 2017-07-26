---
title: Week Of Code 24
date: 2017-7-17
layout: post
---
This week, I'm doing HackerRank Week of Code 34. I've never done something like that in the past, so I thought it'd be interesting to do so.  
The main reason I'm doing this is for fun, obviously. But I also think that it's good to do those kind of exercises regularly, to stay fresh on algorithms, data structure and other concepts you don't get to use in an every day job.  

I'm pretty bad at all that, so I don't expect to be able to finish all of the exercises, and that's ok. I'll just keep notes along the week, and if I'm not too ashamed of the results, I'll post it :D

## Day 1: Once in a Tram
Time: about 10 minutes  
Goal: from a 6 digit number, find the next "lucky" number. A number is lucky when the sum of the first 3 digits == the sum of last 3 digits.  
Example: 165912 is lucky because sum of 1 + 6 + 5, and 9 + 1 + 2 both == 12.  

#### Solution:
Basically need to split the number in 2 ints and compare. When they are not equals, increment by 1.  
I'm sure there is a way better way in doing so, by doing some arithmetic comparison on numbers types I've heard of, but I'm bad at Maths, and the tests cases are passing with brute force, which doesn't seem too bad in Python anyways.

#### My algorithm is as follow:
1. Split the number in 2 digits and compare.
2. If they are equals and it's not the original number, return the number.
3. Call original method for number + 1.

```python
def split(x):
    """Split x into 3 first and last digits and return the sum of each."""
    split = [int(n) for n in str(x)]
    a, b = split[:3], split[3:]
    return [sum(a), sum(b)]

def onceInATram(x, start=True):
    """Return next lucky number starting from x."""
    a, b = split(x)
    if a == b and not start:
        return x

    while a != b:
        return onceInATram(x+1, False)
```

#### What did I learn?
That was pretty easy, but I refreshed my mind of list comprehension and how Python can look clever for some things. Another language would have made it harder to split an int into an array of ints.  
I'm sure a lot of people would argue that showing neat lamba one liners, but lambdas are always confusing. Map would work too, but would make the code a bit more verbose.  

`x.toString().split('').map(x => parseInt(x))` in Javascript is still longer and takes some time to parse.  
`x.to_s.chars.map(&:to_i)` is also a bit more complex in ruby.  


## Day 2: Maximum Gcd and Sum
Time: almost an hour  
Goal: From 2 arrays of length n, find x and y such as x is from array 1 and y from array 2, and gcd(x, y) is the biggest gcd from all possible pairs. In case 2 pairs have the same gcd, return the biggest sum of x + y.  
Example: [3 1 4 2 8] and [5 2 12 8 3] return 16 because biggest gcd of all possible pairs is gcd(8, 8) == 8. sum(8, 8) == 16.  

#### Solution
My algorithm is "correct" in the sense that it returns the correct result, but fails half of the test cases because of timeouts. The inputs can get really big, and I'm not able to optimize to better than O(n^2) :\  
Right now I'm basically iterating over each array with a nested loop.  
I tried:  
- convert arrays to list to remove duplicates
- sort array, to break out of the loop earlier (once your gcd is > than remaining elements)

This exercise was interesting but again very focused on Maths. I don't know much about arithmetics so I'm not aware of tricks we can use to deal with pairs / gcd. Maybe there is no trick and I'm just not seeing it. Will see once the day is over and I can see successful submitions.  

#### My algorithm is as follow
```python
import sys
import fractions

def maximumGcdAndSum(A, B):
def maximumGcdAndSum(A, B):
    A = sorted(set(A), reverse=True)
    B = sorted(set(B), reverse=True)
    max_gcd = 0
    gcd_sum = 0

    for a in A:
        for b in B:
            if (max_gcd) >= a:
                return gcd_sum
            if (max_gcd) >= b:
                break

            gcd = fractions.gcd(a, b)
            if  gcd > max_gcd or (gcd == max_gcd and a + b > gcd_sum):
                max_gcd = gcd
                gcd_sum = a + b

    return gcd_sum
```
This is the highest ranked solution, interestingly enough this one seems actually wrong because test cases are failing instead of timing out. I'm wondering if there is a hedge case I'm missing, such as large negative numbers.  
Having `max_gcd > a and max_gcd > b` instead of a `or` doesn't fail but more cases are timing out.

### What did I learn?
Not sure - it's kind of tricky that hackerrank doesn't let you see all test cases inputs and outputs, so you can debug; I mean, that's how real life works. If you can't see i/o then debugging becomes just aiming in the dark. It's too bad. It might be something very obvious. Or I might just be bad at algorithms and optimization (I actually am!).  
That's ok tho, this is fun, just need to make sure to not start thinking you are a bad engineer just because you can't solve all those problems (also true the other way round!).  

