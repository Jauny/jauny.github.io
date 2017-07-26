---
title: On pointers in Golang
date: 2017-06-03
layout: post
---
_I'm learning Go, and it's my first typed language, so I might write a few posts about things I learn._

In Golang, functions can be passed both pointers and direct references to objects. You can also declare those function on both pointers and references.  
It's a great thing, but be careful that the result is definitely not the same. In one short sentence, you could say that you should always use pointers if you want mutability, and always use direct references if you want immutability.  

The reason is that in Golang, when an object is passed by reference to a new scope (for example a function's scope), a copy of the object is passed, not the object itself. Consequently, mutating that copy will not result in mutating the original object. By definition, passing a pointer and mutating the value the pointer points to will mutate the original object.  

Let me show you some code.  

Let's first declare 2 structs, Person and People.  

```go
type Person struct {
    name string
}

type People struct {
    members []Person
}
```

Let's declare a Person and see it's address and it's pointer address outside and inside of a function:  

```go
func checkAddr(p Person, pt *Person) {
    fmt.Printf("Address of p inside function: %p", &p)
    fmt.Printf("Address of pt inside function: %p", pt)
}

p := Person{}
fmt.Printf("Address of p outside of function: %p", &p)
checkAddr(p, &p)

=> Address of p outside of function: 0x1040c108
=> Address of p inside function 0x1040c110
=> Address of pt inside function: 0x1040c108
```
As we can see, the address of p outside and inside the functions is different, since a copy of p is passed to the function.  
But pt points to the correct address of p.  

Let's see what happens with functions when trying to mutate a direct reference:  
```go
func badMutation(p Person) {
    p.name = "from Growth"
}
p.name = "Jonathan"
fmt.Printf("p's name is %s", p.name)
badMutation(p)
fmt.Printf("p's name is %s", p.name)

=> p's name is Jonathan
=> p's name is Jonathan
```

The name doesn't get updated here. Let's try with a pointer:  

```go
func mutation(p *Person) {
    p.name = "from Growth"
}
fmt.Printf("p's name is %s", p.name)
mutation(p)
fmt.Printf("p's name is %s", p.name)

=> p's name is Jonathan
=> p's name is from Growth
```

Now it works, because we are correctly referencing the correct object from the pointer inside the function.  

What about declaring a function ON a struct? Same thing:

```go
func (people People) badAddMember() {
    p := Person{name: "Jon"}
    people.members = append(people.members, p)
}

group := People{
    members: []Person{
        Person{name: "Jonathan"},
    }
}
fmt.Printf("The group has %d member(s)", len(group.members))
group.badAddMember()
fmt.Printf("The group has %d member(s)", len(group.members))

=> The group has 1 member(s)
=> The group has 1 member(s)
```

We see here the original group object was not updated with the new Person. This was weird to me since we're declaring the function directly on the object, how and when could it get copied? It's because this is just syntactic sugar:
```go
func (people People) badAddMember() {}
people.badAddMember()
// is exactly the same as
func badAddMember(people People) {}
badAddMember(people)
```

With this in mind, it totally makes more sense, right?! Let's try again using pointers:  

```go
func (people *People) addMember() {
    p := Person{name: "Jon"}
    people.members = append(people.members, p)
}
fmt.Printf("The group has %d member(s)", len(group.members))
group.addMember()
fmt.Printf("The group has %d member(s)", len(group.members))

=> The group has 1 member(s)
=> The group has 2 member(s)
```

Now it works!  

Something to note here; I declared `People.members` as a slice of Person (`[]Person`). According to what we just saw, unless you really want immutability, it is recommended to always deal with object through their pointers. Following this, we should have declared `People.members` as a slice of Person pointers, such as `[]*Person`. This way, when accessing a Person, you directly access its pointer and can safely mutate without having the think if you need to use the pointer or not.  

Go is fun, if you haven't tried it yet, you should definitely try. It's quick to learn and has amazing documentations and a very good [Tour of Golang](https://tour.golang.org/welcome/1).  

You can play around with my code snippets on the post's [playground](https://play.golang.org/p/7Kem0I8ix4).

EDIT: Continued on [this new post](/2017/on-go-pointers-again/).
