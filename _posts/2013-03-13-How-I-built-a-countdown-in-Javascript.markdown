---
id: 9
title: How I built a countdown in Javascript
date: 2013-03-13
layout: post
---

Today, we are expanding our [house cleaning services](http://iamexec.com/race/) to 4 new cities; Los Angeles, Chicago, Boston and New York.
To celebrate, we are organizing a Race for the Chore, where the city with the most house cleanings booked will get those cleanings for free!

I spent the last few days in building the page for that race, and had fun building a Javascript Countdown, showing the time remaining until the end of the race.

Sounded easier than it was, but then, with some tips, I made it as easy as it sounds again!

First, I wanted the timer to be interactive. By interactive, I mean live, and that the user actually see the timer moving. So I needed to get my time up to seconds, and the timer to refresh every seconds.
Then, since we are opening to new cities such as Boston and New York, I needed a timezone-proof timer. Because the Race for the Chore finishes March 20, at 9pm PST. Not EST, or anything else.

So, let's explain the second point first, way more logic to do things upside down, right?!

To make it timezone-proof, I set my base times from my backend in Ruby.

```ruby
finish = Time.local(2013, 3, 20, 21).in_time_zone('Pacific Time (US & Canada)')
now = Time.now.in_time_zone('Pacific Time (US & Canada)')
@diff =  finish - now
```

This allows me to have the time difference between now and the end of the race in seconds.
I'll be able to use @diff in my views and my javascript.

Then, my javascript;

First, as most script in your views, you'll want to load it only once the page is loaded. Let's do this with jQuery;

```javascript
$(function() {
	// anything you want to load once the page is ready
})
```

So now, as we already calculated the time remaining until the end of the race in our Controller with Ruby, we have seconds that we want to split into Days, Hours, Minutes and Seconds.
Let's make a function that will do this;

```javascript
d = <%= @diff %>
function calculateTimes(d) {
  var diff = d;
  if (diff < 0) { diff = 0 }; // 0 and not a negative remaining time.
  
  var days = Math.floor( diff/86400 ); // 86400 seconds in a day
  diff = diff % 86400; // remove those days from the remaining time
  var hours = Math.floor( diff/3600 );
  diff = diff % 3600;
  var mins = Math.floor( diff/60 );
  var sec = Math.floor( diff%60 );
  
  return {
    diff: diff,
    days: days,
    hours: hours,
    mins: mins,
    secs: secs
  };
}
```

So here we have a function that splits the remaining seconds in days, hours, mins and secs and returns a hash with the information, so we can do, say, time = calculateTimes(d) and then call time.days, etc…

Last step, we need to get the timer to change; Substract a second every second, and placing the data inside the DOM;

```javascript
setInterval(
  function() {
    d -= 1; // remove 1 second to the remaining time
    
    $('#days').text(time.days);
    $('#hours').text(time.hours);
    $('#mins').text(time.mins);
    $('#secs').text(time.secs); // place the elements in the DOM
  }, 1000 // do this again every second
);
```

And Tadaaaa! Here you Go. Now, every seconds, you have a function that calculates the remaining time, splits it in days, hours, mins and secs, place the data in the DOM and then substract a second from the remaining time!
  