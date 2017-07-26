---
id: 20
title: Changing a Getter behavior for better polymorphism
date: 2013-07-09
layout: post
---

Polymorphic associations are awesome. In rails, even better.
It's so easy to use, there is no excuse to do without them. But sometimes, it's so easy and all pre-made for you, that it's tricky to decide how to play/modify some behavior.

Let's say you have an airline, and you want to save the reason why people are canceling a flight. Pretty straight forward, right?

First you create your new model, let's call it CancelReason.

```ruby
class CancelReason < ActiveRecord::Base
  belongs_to :flight
  attr_accessor :reason, :flight_id
end

class Flight < ActiveRecord::Base
  has_many :cancel_reasons
end

class FlightsController < ApplicationController
  def cancel
    …
    self.cancel_reasons.create :reason => params[:reason]
    …
  end
end
```

So now, when one of your customer cancels a flight, you ask why and it saves a CancelReason linked to you flight. Then if you want to pull stats on what is the cause for most cancellations, you can just retreive all your reasons and see.

#### Cancel all the things!
But let's introduce something else; Trips. A Trip is a group of flights, either because your customer had a stop to go to his destination, or because he wants to go round the world, etc.
Trips can be cancelled.

```ruby
class Trip < ActiveRecord::Base
  has_many :flights
end

class TripsController < ApplicationController
  def cancel
    @trip.jobs.each do |job|
      job.cancel
    end
  end
end
```

Again here, nothing's wrong. Somebody cancels a trip, it cancels all the flights; You still could ask for a reason, and the reason would get added to all the flights cancelled.

But this introduces a problem;
Let's say I book a flight to go to Perth, Australia. Maybe my trip will have 3 flights; One from NYC to SF. Then SF to Syndey. Then Sydney to Perth.
I loose my job, and cancel my flight, giving as a reason "too expensive".
Then somebody from Melbourne books a flight to Perth, which is direct, but have troubles with customer service and decides to cancel, giving as an excuse "bad experience".

When the airline data analysts will make statistics on why people are canceling, they are going to get all the reasons and group them and count them;
3 found the service too expensive, 1 had a bad experience. Clearly, we need to lower our prices, and for now on, the customer service might not be urgent.
HOW INNOCENT! Just because my trip had 3 flights, their data is all messed up!

#### A hint of polymorphism, please!
So, instead of adding a reason to flights when a trip is cancelled, let's make CancelReason polymorphic and add a cancel reason to a trip itself!

```ruby
class CancelReason < ActiveRecord::Base
  belongs_to :thing, polymorphic: true
  attr_accesor :reason, :thing_id, :thing_type
end

class Flight < ActiveRecord::Base
  has_many :cancel_reasons, :as => :thing
end

class Trip < ActiveRecord::Base
  has_many :cancel_reasons, :as => :thing
end

class TripsController < ApplicationController
  def cancel
    @trip.cancel_reasons.create reason: params[:reasons]
  end
end

```
Good! So now, when we cancel a trip, it will create a reason for the trip itself, and not for the flights anymore (I'll let you work around the flights controller to not create any reason when they are being cancelled as part of a trip's cancellation).

So now, when our data analysts will call all the reasons, only one reason for "too expensive" will appear, as it is supposed to.

But now, if you get one of the flights from the cancelled trip, and call @flight.cancel_reasons on it, you'll have nothing!

#### alias_method ftw
So you want to modify you cancel_reasons getter method to return you the flight's cancel_reason, unless the flight is part of a trip, and in that case, it should return the trip's cancel reasons!

```ruby
class Flight < ActiveRecord::Base
  alias_method :original_cancel_reasons, :cancel_reasons

  def cancel_reasons
    if self.original_cancel_reasons.present?
      original_cancel_reasons
    else
      self.trip.cancel_reasons
    end
  end
end
```

Here, we check if the flight has its own cancel_reasons. If not, it might be because it's part of a trip, so we will return the trip's cancel_reasons!

And tada, you now have a fully functioning polymorphism with some method aliasing to keep the code as clean as possible!
  