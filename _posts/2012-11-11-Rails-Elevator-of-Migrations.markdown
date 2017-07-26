---
id: 6
title: Rails Elevator of Migrations
date: 2012-11-11
layout: post
---

![Migrations Elevator Psy](http://images.wikia.com/mlp/images/4/40/Elevator.gif)

In rails, modifications on the Database are made through migrations. Migrations are sort of like git, for databases’ schema. Every time you want to modify your database, you create a new migration file, allowing you to revert those changes easily (as soon as the migration file is good).

So migration files are most of the time built with 2 methods;
* up
* and down
The __up__ method will tell your database what to do when you “_upgrade_” your database through that migration file, while the __down__ method will be for when you “_downgrade_” through that migration file.

WTF? Yes that’s right, what am I talking about?

That’s where the __elevator__ comes in. 
Imagine your database as being inside an elevator. 
The migration files as a floor.

Anytime you migrate, your database is moving from a floor to another. The highest floor being the last migration, and the lowest, well, the first migration.

So let’s do our first migration;

```ruby
class Migration1 < ActiveRecord::Migration
  def up
    create_table :users do |t|
    t.string :name
  end
 
  def down
    drop_table :users
  end
end
```
```scala
    _____________
   | migration 1 |\/| <= migration
   |_____________|/\|    elevator
```

Here, you made your first migration, creating a table Users, which has one column, name. 
The elevator is at the first floor, being the only one available.

Now, you decide to add a column email, you make a migration file for that, which creates a new floor, and migrate (rake db:migrate) the database, which makes the elevator go to that floor.
Then you remember you also wanted to add a column nickname, so again, you create a third migration, and migrate.

```ruby
class Migration2 < ActiveRecord::Migration
  def up
    add_column :users, :email, :string
  end
 
  def down
    remove_column :users, :email
  end
end
 
class Migration3 < ActiveRecord::migration
  def up
    add_column :users, :nickname, :string
  end
 
  def down
    remove_column :users, :nickname
  end
end
```
```scala
    _____________
   | migration 3 |\/| <= migration
   |_____________|/\|    elevator
   | migration 2 |
   |_____________|
   | migration 1 |
   |_____________|
```

As you can see, your database’s elevator is at the third floor, which means it has the most recent schema you gave it. The table Users has 3 columns, name, email and nickname.

Now, what happens if you decide that all those columns are useless, and you just need names? You want to get back to the original state of the database, with the table Users having just the name column. 

Well, you will migrate back to the first migration (rake db:migrate VERSION=version_number). But what really happens?

```scala
    _____________
   | migration 3 |
   |_____________|
   | migration 2 |
   |_____________|
   | migration 1 |\/| <= migration
   |_____________|/\|    elevator
```

Your elevator will travel through the floors 3 and 2 going down, hence, the down methods from the 2 migration files will be triggered and do what they are supposed to; Delete the column nickname and delete the column email.

If you decide to get back with the columns email and nickname, you just have to migrate again to the most recent migration file, and the elevator will go up, through floors 2 and 3, and trigger their up methods.

This migration system allows you to move your database to any floor, just like if it traveled through time. As I said. It’s like git. Sort of.
  