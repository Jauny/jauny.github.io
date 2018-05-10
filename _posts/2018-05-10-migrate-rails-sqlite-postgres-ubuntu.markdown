---
title: Migrate Rails 5 from Sqlite3 to Postgres on Ubuntu 16
date: 2018-05-10
layout: post
---

## Prepare Rails and local environment
First, let's install postgres. On Mac, `brew install postgres` should do the trick. On other systems, looks at the [Postgres official install page](https://www.postgresql.org/download/).  

Then, switch the Rails app to using Postgres.  

In your `Gemfile`, remove the sqlite3 gem and add the postgres one

```
# gem 'sqlite3'
gem 'pg'
```

and update your `config/database.yml`. It should now look like this  

```
default: &default
  adapter: postgresql
  encoding: unicode
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>

development:
  <<: *default
  database: blog_development
  
test:
  <<: *default
  database: blog_test
  
production:
  <<: *default
  database: blog_production
  username: deploy
  password: <%= ENV['POSTGRES_BLOG_PASSWORD'] %>
```

The development and test sections are standard and Rails will handle everything. Pay attention to the production section. We'll be manually creating the database, the user and its password, so you'll have to use matching values.

You now should be able to have Rails setup the database.

```
bin/rails db:setup
```


## Prepare your Ubuntu 16.04 server
Postgres is available on apt-get, so we'll use this to install it.  
As usual, start by updating your packages and then installing the required packages

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install postgresql postgresql-contrib libpq-dev
```

This will install Postgres and create a Linux user `postgres` with access. Since we are doing deploys and most of our management through the user `deploy`, we want to give access to this user too.

PostgreSQL manages database access permissions using the concept of *roles*. Let's switch to the `postgres` user to create a new role for our `deploy` user.  

```
$ su - postgres
# if prompted for password, it is the same as your current user's

# now login into postgres and create a new role
$ psql
postgres=> CREATE ROLE deploy WITH CREATEDB CREATEROLE LOGIN PASSWORD 'passwordyouwanttouse';
```

Note that the role created has the same name as the Linux user we want to use, which is the *username* set in `config/database.yml`.  

If we check all roles available with `\du`, we see the newly created role

```
postgres=> \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 deploy    | Create role, Create DB                                     | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

Now that we have a role for our `deploy` user, we can switch back to it and create the `blog_production` database

```
$ su - deploy

$ psql postgres
postgres=> create database blog_production;
CREATE DATABASE
postgres=> \q

$ psql -l
                                     List of databases
      Name       |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------------+----------+----------+-------------+-------------+-----------------------
blog_production  | deploy   | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
postgres         | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
```

Since we set *password* to be `ENV['POSTGRES_BLOG_PASSWORD']` in our `config/database.yml`, the last thing we have to do is to add our database password as an env variable.  
In Ubuntu, a good place to put environment variables that your want to be accessible from all shells (interactive or not, login or not) is `/etc/environment`. Let's add the following line
`POSTGRES_BLOG_PASSWORD=passwordyouwanttouse` to it.

## Done!
You now have postgres installed on Ubuntu 16.04 and the `deploy` user with correct access to the `blog_production` database we manually created.  
Your Rails app is setup to work with development and test databases, and knows to find the password in `/etc/environment` for the production one.  

The good thing is that we didn't have to change anything to our deploy systems - I use Capistrano, and can simply run `cap production deploy` to deploy my new app and use Postgres.

**Next**  
We now have postgres, but it's empty! Next post will be about migrating data from sqlite to postgres.
