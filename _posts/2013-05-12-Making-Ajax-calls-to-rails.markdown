---
id: 12
title: Making Ajax calls to rails
date: 2013-05-12
layout: post
---

For the past few weeks, I've been working on our new mobile website at Exec, so user's wihout our iPhone app can still easily book a house cleaning.
For a better experience, I used knockout.js to make the booking flow a single page app, and make the whole operation smoother, despite a slower connection.

Coming from a rails background (to be honest, I never even really played with sinatra), I am used to have my framework do __all the work__ for me. And by all the work, I mean, ALL THE WORK.

Building an app with knockout made me realized how spoiled we are as rails developpers;

```ruby
rails new myApp
```

And swooch, all you need to do is fill in the blanks for your views and controllers. So easy.

I'm gonna try here to give a really simple, basic explanation of how ajax works. With a noob _ish_ rails dev point of view.

#### Ajax - What the hell?
So, first thing; Javascript is a _front-end_ language. This means that the whole code in loaded in your view. Which means it has __no idea__ of what's happening in the backend.
Let me explain;

Let's say you're in Rails. You are working in your controller.

```ruby
def show
  @motorcycle = Motorcycle.find params[:id]
end
```

Here, in the show method, you want to render a page with the motorcycle querried by id in the URI. Let's say, www.jo-racing.com/motorcycles/78.
Well, what happens when a user calls that address?
The browser makes a request to my racing website's server, which knows that a get request to /motorcycles/:id goes to the show action in the motorcycles controller.
Then, inside the controller, the database is called with ActiveRecord to give the info about the motorcycle with id 78, which all is saved into @motorcycle.
Then, in the view, you can call any method Motorcycle has on @motorcycle, and it will be rendered in HTML and this HTML will be sent to the browser who made the request.

Cool, easy, flawless. Why all that was possible? Because __you're in the backend__. What happened there is that the server did all the work, and ended up rendering a page full of HTML, which got read by the browser which made it look what it's supposed to look like on the user's screen.

Now, let's say that on the page, you have a text field where you can search for another motorcycle, and it will show a list of results;

```html
<form action="motorcycles/search" method="get">
  <input type="text" id="search" value="query">
  <button type="submit">Search</button>
</form>
```

```ruby
def search
  @motorcycles = Motorcycle.where(brand: params[:query])
  
  redirect_to motorcycles_path
end
```

Again, this is easy. Once the Search button is hit, the request is made, the controller makes what it has to do, the page is refreshed and the HTML is rendered. Again, because the whole action went back inside the backend. Easy, efficient, but not the best user experience since you have to get a page refresh.

So now, let's say you're doing it in javascript;

```html
<form id="moto-search">
  <input type="text" id="search" name="query">
  <button onclick="submitForm()">Search</button>
</form>
```
Then what? What do you do in that submitForm() function? You can't act like if you were in a controller. You can't have something like 

```javascript
submitForm = function() {
  var query = $('#search').value();
  var motorcycles = Motorcycle.where(brand: query);
};
```

It just won't work. First javascript has no idea what the hell ActiveRecord is. Second, you're in the user's browser. The data is not in the user's computer. When you're in the backend, you're directly inside your own server, where your database is; But here, in javascript, you're at someone else's house, or office. No Motorcycles table there… 

So you have to start looking at your application as an API. You know, where you make calls on googlemaps to get some address information, you make a request to there API asking to access their data on their servers; Same here; You will need to provide your user some sort of way to request access to your servers to access your data;

How's that work? Well, that's what the javascript function __submitForm()__ will do. And you will need to prepare yourself to receive those requests too. Your backend will need a way to respond to those request; "Hey! Give me those info on your motorcycles!" "Ok, I know how to do that, I was expecting your call!"

So, you need a URI that the javascript function can access to ask for the information (remember, that call is made by your user's browser, from a complete unknown location);
That URI will point to a controller action, which will know how to answer when it's a javascript call;
Then your function will receive the answer and do something with this info (inject the info in the screen maybe).

So, you already have the URI, right? Our app is already cappable of getting a search query and returning the results (motorcycles#search from above), but not in the correct format; The whole goal of using javascript is not having the page refresh, hence not using redirect_to;
Let's change that if the request comes from javascript (xhr, for XMLHttpRequest)

```ruby
def search
  @motorcycles = Motorcycle.where(brand: params[:query])
  
  if request.xhr?
    render :json => @motorcycles
  else
    redirect_to motorcycles_path
  end
end
```

Now your controller knows what to do when it gets a request on /motorcycles/search with javascript;
Now let's look at what the submitForm() would look like;

```javascript
submitForm = function() {
  var query = $('#search').value();
  var uri = "http://www.jo-racing.com/motorcycles/search?query=" + query;
  
  $.get(uri, function(data) {
    // here data is the json rendered with all the motorcycles;
    // do what you want with it, like create a table, etc…
    // your DOM will be updated live without any page refresh, way better!
  });
};
```

Here, now when a user enters some terms in the search textfield and hits "Search", javascript is asynchronously (what _ajax_ stands for) calling your controller and asking for the result, and then do what you tell it to do with the json returned. No refresh, more smoothness!
  