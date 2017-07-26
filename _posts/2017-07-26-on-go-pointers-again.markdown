---
title: On Pointers in Go - Really
layout: post
date: 2017-07-26
---
I wrote about pointers in Go in this [previous post](/2017/On-Go-Pointers/).  

And I still banged my head for an hour on something just now. So here's another post, so I really, like REALLY understand to always, ALWAYS use pointers. Unless I really know what I'm doing and why I don't want a pointer.  

So here, let's say we have a `Person` struct and a `changeName` function  

```golang
type Person struct {
    Name string
}

func changeName(p Person) {
    p.Name = "Jonathan"
}
```

In this case, we all know what happens - changeName accepts a *value* and not a pointer, so actually a copy of the value is passed in, and mutating it inside the function's scope won't mutate it in the outer scope.  

```golang
mike := Person{Name: "Mike"}
changeName(mike)

fmt.Println(mike.Name)
=> Mike
```

We need to pass in a reference to the *value*, using a *pointer*.  

```golang
func changeName(p *Person) {
    p.Name = "Jonathan"
}

changeName(&mike)
fmt.Println(mike)
=> Jonathan
```

Now let's build a team!  

```golang
type Team struct {
    People []Person
}

mike := Person{
    Name: "Mike"
}
team := Team{
    People: []Person{mike},
}

changeName(mike)
fmt.Println(mike.Name)
=> Jonathan

fmt.Println(team.People[0].Name)
=> Mike
```

WHAT?! That little thing ruined me for ~an hour today.  
Here it's pretty obvious, `Team.People` is a list of `Person` not `*Person`, so it hold *copiieeessss* for persons. When you edit the original `mike`, it doesn't update the copy held in `team.People`.
When dealing with 1000s of lines of code, and more functions adding/removing stuff and being called in deeper nested scopes, it becomes a little more tricky to figure out.  

The thing I want to communicate here is that, I *thought* I had fixed my pointer-related issues, but I didn't *everywhere*.  

So here is the learning here; Use **pointers ALL THE TIME. EVERYWHERE.** And, to make it easier, don't push additional cognitive load to your mind by actually having to think about pointers and figure out "is that variable a pointer already or not? Etc" and just create functions for everything, which will handle the pointer mess, so in your code, you are actually always dealing with pointers and you don't care.  

Look:  

```golang
type Person struct {
    Name string
}

func newPerson(name string) *Person {
    return &Person{
        Name: name
    }
}

func changeName(p *Person) {
    p.Name = "Jonathan"
}

type Team struct {
    People []*Person
}

func newTeam() *Team {
    return &Team{
        People: []*Person{}
    }
}

func (t *Team) addPerson(p *Person) {
    t.People = append(t.People, p)
}
```

This seems like a lot of boilerplate at first, but once you've done that, all the pointer logic is handled in those methods. Call them *class* methods, or *helper* methods or whatever. But that way, you can forget about pointers, and still using them correctly. Look how easier and cleaner doing the previous manipulation is when using those functions:  

```golang
team := newTeam()
mike := newPerson("mike")

team.addPerson(mike)

fmt.Println(mike.Name)
=> Mike
fmt.Println(team.People[0].Name)
=> Mike

changeName(mike)
fmt.Println(mike.Name)
=> Jonathan
fmt.Println(team.People[0].Name)
=> Jonathan
```

Not one single * or & here now. Easy as 1,2,3.  

So here we go again, POINTER ALL THE TIME.
