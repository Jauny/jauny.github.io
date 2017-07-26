---
id: 19
title: Post-login redirection to requested page with Devise
date: 2013-06-17
layout: post
---

Often, the login redirection has a static redirection to say, root_path or user_path.

When a logged out user tries to access a page that requires to be logged in, it is better, for a good user experience, to dynamically redirect them to that requested page after they logged in.

I did not find much resources on that, and the few explainations I found seemed way too unclear, instable or just didn't feel simple/good enough.

So here is what I found with Devise, which works like a charm and is really simple.

Devise has that method called ```stored_location_for(resource)``` which, as its name says, stores the location the resource (user, admin, etc.) is coming from before signing in.

By default, after signing in, Devise calls ```after_sign_in_path(resource)``` to get the path to redirect to, which more or less returns ```resource_path``` by default.

So, now we are aware of those two methods, let's simply rewrite ```after_sign_in_path``` using ```stored_location_for```!

```ruby
class ApplicationController << ActionController::Base
  protect_from_forgery
  
  def after_sign_in_path(resource)
  sign_in_url = url_for(:action => 'new', :controller => 'sessions', :only_path => false, :protocol => 'http')
  
    if request.referer == sign_in_url
      super
    else
      stored_location_for(resource) || request.referer || root_path
    end
  end
end
```
So here, the first step is to check if the request was originally made from were the default redirection is. If it is, let's keep the magic from Devise, and call ```super``` so we are sure we are not missing anything.

If it's not the case, we return ```stored_location_for``` to get the original request, and if it wasn't stored, we get request.referer, and finally if this is not available either, our last hope is to return to the root_path.

I had to look deep inside Devise's github to find this, and no answer on stackoverflow seemed to be using this solution, so here it is!
  