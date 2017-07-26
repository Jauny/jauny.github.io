---
title: Closures and Callbacks in Javascript
date: 2017-01-10
layout: post
---

### A normal function
Let's declare the function:

```javascript
var add = function(x, y) {
  return x + y;
};
```

Now, we can call the function using the variable `add`

```javascript
> add(2, 3)
> 5
```

If we omit parenthesis and arguments, we can also reference the function without calling it: 

```javascript
> add
> function (x,y) { return x+y; }
```

**2 things happen when we call `add(5, 3)`:**

1. The `add` part is replaced (interpreted) with the function declaration (`function (x, y) { return x + y; }`,  
2. Parenthesis are added, containing the arguments. Then the function is run.

So `add(3, 5)` is the same as:

```javascript
> function(x, y) {
>   return x + y;
> }(3, 5)
> 5
```

### Closures
**A closure is a function that returns another function.**  
Let's leverage the `add` function we just used to create a new function called `addTen`. It adds 10 to any number.

```javascript
var addTen = function(x) {
  return add(x, 10);
}
```

As we did above, we can now reference this function with the variable `addTen`. We must add parenthesis to run the function:

```javascript
> addTen
> function (x) { return add(x, 10) }
> 
> addTen(5)
> 15
```

Now, `add(x, 10)` is printed when we reference the function. There are parenthesis, so it looks like we are calling `add`, but the function hasn't been called yet.

Why?

The reason is **Javascript’s double interpretation cycle.**  

The code is interpreted twice:  
- at load time (when the script loads)  
- at run time (when the code actually runs)  

The first time the code is interpreted:  
  
* All variables are replaced by what they actually hold. For instance, `add` is replaced by `function (x, y) { return x + y;}`
* All first level function calls run. `add(5,3)` runs and is replaced by `15`

**What's important is "first level".**   
In the example of our closure, the `return add(x, 10)` part is "nested". It lives inside another function, and won't run unless the parent function is called.

Say you load the following file:

```javascript
var add = function (x, y) {
  return x + y;
};
var addTen = function (x) {
  return add(x, 10);
};

add
add(5, 3)

addTen
addTen(5)
```

The interpreted file, once loaded, looks like this: [footnote 1]

```javascript
var add = function (x, y) {
  return x + y;
};
var addTen = function (x) {
  return add(x, 10);
};

function (x, y) {
  return x + y;
}
8

function (x) {
  return add(x, 10);
}
15
```

**That's fucking important!! -->**  
In the example of our closure, when interpreting `addTen`, the part with `add(x, 10)` isn’t executed despite parenthesis. That’s because the parent is not being executed (`addTen` is without parenthesis).

### Passing around function references
Having the function declaration in the variable is useful to call it multiple times, and from different places. But it also to "pass it around". For example, you can now pass it as an argument to another function. 

Let's say we add another math function called `multiple`:  

```javascript
var multiple = function (x, y) {
  return x * y;
};
```

And that instead of the `addTen` function, we want a `modeTen` function. It takes a number and an incrementation mode (add or multiple) and combines the number and 10 using this incrementation mode:

```javascript
var modeTen = function(x, mode) {
  return mode(x, 10);
};
```

Here we can now call our `modeTen` function with a number and either our `add` or `multiple` function:

```javascript
> modeTen(5, add)
> 15

> modeTen(5, multiple)
> 50
```

### Why does it matter?
Referencing, passing and calling function is something we keep doing in javascript. For instance, with callbacks:

```javascript
var functionWithCallback = function (name, callback) {
  console.log("hello " + name);
  
  callback(name);
};
```

This is a very simple function that prints a name and calls a callback once it’s done.  
The callback function could be just a function we use to let us know that the name was successfully printed:

```javascript
var success = function(name) {
  console.log("successfully printed " + name);
};

> functionWithCallback('jonathan', success);
> "hello jonathan"
> "successfully printed jonathan"
```

Closures are often wrongfully abused to fix a bug coming from a bad understanding of all this. Look at an example using our previous `functionWithCallback`: 

Let's say you are using an API you are not really familiar with (could be something like `res.render` in nodejs), and you want to make sure that your callback will be called with the `name` variable. You might write something like this:

```javascript
functionWithCallback('jonathan', success('jonathan'));
```

You're passing `success('jonathan')` as an argument. As we just saw, `success('jonathan')` will be called at load time. **That means you end up passing the result of the function instead of the function itself**:  
`functionWithCallback('jonathan', 'successfully printed jonathan')`. 

Not what you wanted.

But faced with a bug, and not understanding the issue, many engineers will mess around, and end up solving this problem with a closure:

```javascript
functionWithCallback('jonathan', function() {
  success('jonathan');
});
```

They end up in this situation because this callback syntax looks familiar. It's the syntax used to declare a callback inline, when it's not in a variable.

The `success` function is being called inside `functionWithCallback` with `name` passed to it as we want. So it’s enough to simply pass a reference of the `success` function as argument. Using the `success` variable without parenthesis:

```javascript
functionWithCallback(‘jonathan’, success);
```

Another example is in React, when passing a function as a prop. Let’s say we have the following React component:

```javascript
class Parent extends React.Component {
  onButtonClick() {
    console.log(‘clicked button‘);
  }

  render() {
    <Button id=”1” onClick={this.onButtonClick} />
  }
}
```

In this example, we pass `onButtonClick` to the button component. When the button is clicked, the function is called, and all is good.

But, if the `onButtonClick` function had a `buttonId` argument, the button would not know about what argument to pass:

```javascript
class Parent extends React.Component {
  onButtonClick(id) {
    console.log(‘clicked button ‘ + id); // we now pass an id as argument
  }

  render() {
    <Button id=”1” onClick={this.onButtonClick} />  // Button has no idea what “id” is
  }
}
```

Since Button doesn’t know what “id” is, we need to explicitly tell the button what the id is and to pass it as an argument when calling the function.  
One solution is to use a closure:

```javascript
render() {
  <Button id=”1” onClick={() => this.onButtonClick(“1”)} />
}
```

In this case it would work, because thanks to the closure the inner function `this.onButtonClick(“1”)` is nested and doesn’t get called at load time.  

Another solution would be to use an inner onClick function on the button component, which is often cleaner (in my opinion):

```javascript
class Parent extends React.Component {
  onButtonClick(id) {
    console.log(‘clicked button ‘ + id);
  }

  render() {
    <Button id=”1” onClick={this.onButtonClick} />
  }
}

Class Button extends React.Component {
  onClick() {
    this.props.onClick(this.props.id);
  }
}
```

This is only possible if you control the element receiving the function as props. If the component was a native HTML `<button>` for instance, this wouldn’t be an option.

A last general comment about passing functions through multiple levels. In our example of the `onButtonClick` that takes an `id` as argument, you only have to explicitly pass the `id` argument in the component that will actually call the function, and can only pass the function by reference to other components it goes through;

```javascript
class Root extends React.Component {
  onButtonClick(id) {
    console.log(‘clicked button ‘ + id);
  }

  render() {
    <Section onButtonClick={this.onButtonClick} />
  }
}

Class Section extends React.Component {
  render() {
    <button id=”1” onClick={() => this.onButtonClick(“1”)} />
  }
}
```

Note here the `onButtonClick` is from the `Root` component and we pass the function down to a button element, through the `Section` component. Despite choosing the closure solution, which we use on the props of the `button`, we don’t have to explicitly tell `Section` about the `id` argument and just pass it `onButtonClick` as a reference.

## What we learned
1. When declaring a function, using the variable holding this function only references the function, but doesn't call it. You need to add parenthesis and arguments to call and execute a function.
2. A closure is a function that returns another function. It's useful to create helper functions such as `addTen`, and in many other situations.
3. Finally, we saw how to use callbacks, pass them as an argument to another function, and use closures to avoid calling the callback at load time, when having to pass it with explicit arguments.

Hope this will help understand better the life cycle of your code and clean up some of your callbacks and unnecessary closures :)

[footnote 1] This is not entirely true as things get manipulated different ways (to dive deeper look at things like scope and encapsulation) and compiled to bytecode in something un-reable for humans. But I find giving this visual representation of the “compiled” file being very useful to understand what the code actually represents.



