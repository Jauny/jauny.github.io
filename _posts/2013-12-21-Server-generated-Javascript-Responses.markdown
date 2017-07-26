---
id: 28
title: Server-generated Javascript Responses
date: 2013-12-21
layout: post
---

DHH wrote an [article](https://37signals.com/svn/posts/3697-server-generated-javascript-responses) on Signal vs Noice on Server-generated Javascript Responses, which reminded of how to write good and _unobstructive_ javascript in Rails.

I'm not gonna lie, it's exactly what I learnt at DevBootcamp, but I feel like I haven't been writing it as well as I could.

I've written [something](http://www.jypepin.com/posts/21) on Ajax in Rails already, and as I say there, as a Rails beginner, Ajax is a tricky concept to grasp, because of the lack of _conventions over configurations_ Rails imposes.

Without a proper understanding, it seems really counter-intuitive (and I still don't really agree with everything), and it's really easy to make a mess.
But as soon as you get it, you are empowered to right better code and better UX (who likes page reloading nowadays?).

So first, let's analyse the Status Quo.

```ruby
= form_for @movie do |f|
  = f.checkbox :seen
  = f.submit
```

Here in our view, we have a form which is basically a checkbox to mark a movie as seen or not.
You check/uncheck the checkbox and submit it.

Right now, it hits the controller like any other action.

```ruby
def update
   @movie = Movie.find params[:id]
   @movie.update_attributes params[:movie]
   
   redirect_to :back
end
```

Then the movie's page refreshes with the updated information. Maybe something is different in the view, like a green border around the movie's poster, or whatever.

Still, the UX isn't amazing, because for an action as simple as marking a movie as seen, the whole page refreshes. It's 1999 on AOL all over again!

And this is when Server-generated Javascript Response comes in. Basically what we want, to avoid having the page to reload, is to update the model __asynchronously__.

Bare with me, it's a complicated word (YES OK I GOOGLED IT) but basically it's saying that the request will be made in _parallel_, and some of it will be handled by Javascript, instead of Ruby.

First, we have to add an attribute to our form to tell rails that we want the request to be AJAX;

```ruby
= form_for @movie, remote: true do |f|
  = f.checkbox :seen
  = f.submit
```

See? We added __remote: true__. It's telling our form to send a request in AJAX, which is means Asynchronous JavaScript and XML. It's the Asynchronous I was talking about ;)

Now we have to tell our controller to look for it and be ready!

```ruby
def update
   @movie = Movie.find params[:id]
   @movie.update_attributes params[:movie]
   
   respond_to do |format|
     format.html { redirect_to :back }
     format.js
   end
end
```

See here, we added a __respond_to__ block, which allows to give different format of request that the controller needs to get ready to recieve.

_format.html_ is for the regular request (somebody might have javascript deactivated or something), which will do the usual redirect.

_format.js_ tells our controller "HEY, LOOK FOR SOMETHING IN JAVASCRIPT THAT LOOKS LIKE IT WOULD BE ABLE TO TAKE CARE OF IT!".
So when our controller receives a request in ajax, it will look for a javascript files that should be able to take care of it.
Rails being awesome, you don't have to give anymore info, and our awesomely smart controller will know to go look for a js file called the same thing as the action, in the views folder.
I don't fully agree with the js file being inside the views folder, but I guess it makes sense; It will always go inside the same views folder and look either for the .html file if it redirects, or for a js file if it's an ajax call.

I still find it more intuitive to go put the file in asset/javascript/movies/update.js, but WHATEVER, I DIDN'T BUILD RAILS.

So here, you need a file update.js in /views/movies/.

```ruby
$('#movie').html('<%= j render @movie %>');
```

Really simple case. Here jQuery looks for a div with id="movie" (the div that contains your movie's info) and renders the partial '_movie.html.erb' (the partial that you render inside #movie).

__j__ means [__escape_javascript__](http://api.rubyonrails.org/classes/ActionView/Helpers/JavaScriptHelper.html#method-i-escape_javascript). It is a Rails helper to make sure it will render correctly single and double quotes for the .html (or any other dom-filling) function.

Finally, let's see what the '_movie.html.erb' could look like;

```ruby
<%= @movie.title %>

<% if @movie.seen? %>
  (seen)
<% end %>

<%= @movie.plot %>
```

See here? If the movie is marked as seen, _(seen)_ shows.

From a UX perspective, clicking the checkbox, submitting the form and having to wait for the page to reload to see _(seen)_ appear is pretty lame and bad.
With Ajax, when you submit the form, only this part will be re-rendered, making _(seen)_ appear, without reloading the page (since it's implemented in the DOM by javascript).

And, VOILA!
  