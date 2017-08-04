---
title: Removing elements from slice during loop
date: 2017-08-04
layout: post
---

During a loop, golang doesn't make a copy of the list you are iterating over, but instead just updates the list on the fly. It can be an issue when you are removing elements from the list.  

For example, let's say you want to filter the list to keep only numbers that are multiples of 3 (`%3 == 0`). With a list `[1,2,3,6]`, at index 2, 3 would get removed, and 6 would then be moved to index 3. i would then get incremented to 3, and no elements are at index 3 anymore (6 was moved to index 2) so the iteration would end, and 6 would never be removed.  

One solution would be to create a new empty slice, and do the opposite; Add numbers that are NOT divisble by 3 and add those to the new slice instead.  

```golang
slice := []int{1,2,3,6}
var newSlice []int

for _, n := range slice {
    if n % 3 != 0 {
        newSlice = append(newSlice, n)
    }
}
```

Ok, this would work. But it's limited.  

What happens if you need to do some computation for each element, and once the computation is successful, you remove the element from the list. A complete success case would empty the list, but if an error occurs, you return the list with remaining elements that have not been removed.  
The previous solution isn't great, because you are using an additional slice, and then have to add the remaining elements to it. It's ok, but a bit counter intuitive because you are _adding_ elements instead of _removing_ them.  

```golang
for _, n := range slice {
    if err := compute(n); err != nil {
        newSlice = append(newSlice, slice[i:]) // add elements that failed to newSlice
        return errors.New("something happened", newSlice) 
    }
}
```

Here comes the reverse loop.  

The best solution to counter the index update issue is to loop from the end of the slice. In that case, removing elements won't affect the remaining elements' indexes.  

```golang
for _, n := range slice {
    if err := compute(n); err != nil {
        // return the slice with only successful elements removed
        return errors.New("something happened", slice)
    }
    slice = append(slice[:i], slice[i+1:]...) // updating the original slice on the fly, and it's ok
}
```

It's nothing fancy, but it's always good to remember this. With languages like Python, you can just use a neat little list comprehension to modify a list on the fly and not have to think about this;  

```python
[n for n in slice if x % 3 != 0]
```

I love Go, but sometimes I feel like it's lacking the little nice syntactic sugar some other languages offer. Sometimes it's too much, but this kind of easy things should be handled in modern languages.
