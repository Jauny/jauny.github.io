---
id: 21
title: Ajax in Rails
date: 2013-07-19
layout: post
---

_Convention over configuration_.
How many times have I heard that. It's one of the core concept around which Rails is developed. And I think it's amazing. It is the exact reason why learning Rails is easier than most other programming frameworks.
_Convention over configuration_ allows to have, most of the times, only one answer to any question. When you begin to program, it is an amazing experience.
And this is why you are often confused when you start discovering other languages, like when you start getting outside of jQuery and doing some real Javascript. 
When you have a question, even really basic -_"[How do I create a class in javascript?](http://www.phpied.com/3-ways-to-define-a-javascript-class/)"_- answers are often confusing, because you don't know which way to choose.

So this doesn't work really well with rails. Rails doesn't really like when there are confusions and a lack of convention. 
Because of that, AJAX is always really confusing. Nobody does it the same way, and no matter how it's done, it feels _weird_.

This might be one of the concept that has the most confusion at Devbootcamp, and the one that students who learnt how to make it work have the most trouble explaining.

We are lucky, because AJAX is cleaner and simpler to use today with most recent versions of Rails, HTML5 and other web standards.

Let's say you have a form on an html page.

```html
<form action="/user" method="post" id="myform">
  Username: <input type="text" name="user">
  <input type="submit" value="Submit">
<form>
```

Here, when you submit the form, your browser will submit a ```POST``` request to /user, the server will do whatever it is supposed to do, and in most of the cases, will redirect the browser to the next page.

Now if we were in the past and wanted to make the request in AJAX, here what our JS would look like;

```javascript
$("#myform").submit(function(e) {
  e.preventDefault;
  $.ajax({
    type: "POST",
    url: "/user",
    data: $(this).serialize()
  }).done(function() {
    alert("AJAX successful!");
  });
});
```

Looks hacky right?
First, ```e.preventDefault``` is telling Javascript "As soon as the form #myform is submitted, run to the browser and prevent it from submitting the form!!!".
Then, we build our AJAX request, in which we have to repeat the URL, the type, even manually ```serialize()``` the form's data.
This is ridiculous and way too repetitive for a lazy programer like me.
It definitely feels wrong.

So, as I said, we are lucky to be today, because with the new jQuery-ujs included in Rails and HTML5, it seems way more right to do some ajax;
First, HTML5 allows us to add more ```data-attributes``` giving more info about our tags. The one interesting here is ```data-remote``` which tells the browser that the form will be submitted with AJAX, so no more need for our JS to go tell the browser.

```html
<form action="/user" method="post" id="myform" data-remote="true">
  Username: <input type="text" name="user">
  <input type="submit" value="Submit">
<form>
```

Now everyone knows that the form is submitted by AJAX, thanks to data-remote, we don't need anymore to _build_ our AJAX request, but only to tell our JS what to do when a request comes back, whatever the state it can have (beforeSend, complete, success, error).

```javascript
$("#myform")
  .bind("ajax:success", function(xhr, data, status) {
    alert("AJAX successful!");
  });
```

And you can chain the states to react depending on the status of the request;

```javascript
$("#myform")
  .bind("ajax:beforeSend", function(xhr, settings) {
    alert("Loading!");
  })
  .bind("ajax:success", function(xhr, data, status) {
    alert("SUCCESS!!!!");
  })
  .bind("ajax:error", function(xhr, data, status) {
    alert("Ooops, something went wrong…");
  });
```

Doesn't look way cleaner now? Feels better for me!
  