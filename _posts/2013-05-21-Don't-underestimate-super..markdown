---
id: 13
title: Don't underestimate super.
date: 2013-05-21
layout: post
---

Here at Exec, I've been working for a bit now into having a system to allow us to log whatever happens in the system;

Either a modification is made by an admins through the admin's dashboard, or a user directly throught the website, we wanted to be able to track everything and easily access the history of a job, a user's info, etc.

For that purpose, I created an Audit model, which, through polymorphism, can be used no matter who 'generates' that audit, and for which model it is;

```ruby
create_table "audits" do
  t.text     "notes"
  t.string   "author_type"
  t.integer  "author_id"
  t.string   "thing_type"
  t.integer  "thing_id"
  t.datetime "created_at"
  t.datetime "updated_at"
end

class Audit < ActiveRecord::Base
  belongs_to :thing, polymorphic: true
  belongs_to :author, polymorphic: true
end
```
Basic enough class to be able to create a helper method in ApplicationController;

```ruby
class ApplicationController < ActionController::Base
  def audit(args)
    Audit.create! args
  end
end
```
Pretty basic class, but since it is (twice!) polymorphic, you can't have a simple ApplicationController method that allows you to create an Audit without having to set everything all the time.

```ruby
audit author_type: 'Admin', author_id: @admin.id, 
      thing_type: 'Job', thing_id: @job.id, 
      notes: "Changed job #{job.id}'s date."
```
Not so convenient to always have to write all that…
A first step would be to extract, for example, the _thing_ data by redefining audit inside of the _Thing_ Controller and using super.

```ruby
def update
  @job.date = new_date
  audit author_type: 'Admin', author_id: @admin.id, 
        notes: "Changed date."
end

def audit(args)
  super(args.merge(thing_type: 'Job', thing_id: @job.id))
end
```
As you can see here, I don't have to set the thing type and id anymore, because I added a new __audit__ helper method in my Job controller, that accepts the still needed arguments and calls super with those arguments and the thing data.

But I still have to set my author, since the job's audit could be generated by either an admin or a user.

The difference here is that, if the _user_ is doing the modification, the update action will be called by a different controller than if it was my _admin_ doing the same modification on the same job. Why? Because my admin uses our internal admin's dashboard, when my user is using his own dashboard.

Hence I have 2 JobsControllers, one inheriting from AdminsController and another one inheriting from WebController.

So when audit is called in my JobsController, super looks first into the related inheriting controller for an audit method, before grabing the __audit__ method inside ApplicationController.

So let's go inside my AdminsController.

```ruby
class AdminsController < ApplicationController
  def audit(args)
    super(args.merge(author_type: 'Admin', author_id: @admin.id))
  end
end
```
I'm inside my AdminsController, so I know the action is always triggered by my admin here. Same thing if I was in my web controller with the author being user.

So now, when I call audit inside my JobsController, I don't have to set the author data anymore either, and just have to set what matters there, the notes field. Let's have a last look at my inheritance here;

```ruby
class JobController < AdminsController
  def update
    @job.date = new_date    
    audit notes: "Changed date to #{new_date}."
  end
  
  private
  def audit(args)
    super(args.merge(thing_type: 'Job', thing_id: @job.id))
  end
end

# super then travels to AdminsController
class AdminsController < ApplicationController
  def audit(args)
    super(args.merge(author_type: 'Admin', author_id: @admin.id))
  end
end

# super then again, travels to the parent, ApplicationController
# where the audit is actually being created!
class ApplicationController < ActionController::Base
  def audit(args)
    Audit.create! args
  end
end
```
  