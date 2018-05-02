---
title: Rails 5, Puma, NGINX, Ubuntu 16 with capistrano on Digital Ocean.
date: 2018-05-02
layout: post
---
# Rails 5, Puma, NGINX, Ubuntu 16 with capistrano on Digital Ocean.

## What is the problem
1. Local and Prod work differently. Once you have a Rails app working locally, a lot of setup has to be done to get the app in production
2. PaaS like Heroku automate everything for you, but you loose control and freedom compared to a regular VPS (ex: Heroku doesn't offer persisting file system).
3. Deploying takes a lot of steps, so you want to automate it.


## Where do we want to be
At the end of this, we should have a Rails 5 app with Puma ready for production, setup with Capistrano for automated deployements, and a DigitalOcean Droplet with Ubuntu 16 and Nginx hosting it.

It will work as follow:

- Host the code on Github
- Running `capistrano production deploy` from local will start the deploy
- Capistrano then `ssh` into the DigitalOcean VPS and runs a bunch of commands, including
  - `git clone` master branch into `/home/deploy/var/www/app/releases/current_timestamp`
  - Installs dependencies and migrate database
  - symlinks it to `/home/deploy/var/www/app/current`
  - restarts puma server for the `current` folder
- Nginx listens to port 80 to redirect requests to puma

## What do we need to setup
- add capistrano config for the automated deploys
- install nodejs
- install ruby + rbenv
- install the database
- create a `deploy` user that will be used by Capistrano
- setup root and ssh access for it
- setup some environment variables for the app (such as SECRET_KEY_BASE)
- setup nginx
- update Puma config to run in production
- setup puma as a systemd service to automatically start at boot

## Step 1: Setup Capistrano
You can see my [commit](https://github.com/Jauny/blog/commit/92ea1bbb3cde4988aae8ab508b8086cff24bf3a5) on my blog to setup everything on the Rails app.
Let's go through each steps.

Add the necessary Capistrano gems to your Gemfile's development group.

```ruby
groupe :development do
  gem 'capistrano',         require: false
  gem 'capistrano-rbenv', '~> 2.1'
  gem 'capistrano-rails',   require: false
  gem 'capistrano-bundler', require: false
  gem 'capistrano3-puma',   require: false
end
```

Those are pretty self explanatory - the additional gems add some specific tasks for Capistrano to use, such as installing rbenv, setting the correct ruby version, starting Puma once everything is ready, etc.

Run `bundle install` to install everything. You now have the `cap` command available.

Run `bundle exec cap install`. This generated the following files:

```
├── Capfile
├── config
│   ├── deploy
│   │   ├── production.rb
│   │   └── staging.rb
│   └── deploy.rb
└── lib
    └── capistrano
            └── tasks
```

- `Capfile` requires and install the necessary files. You modify it when you add a new Capistrano dependency.
- `config/deploy.rb` and `config/deploy/*.rb` are the general and stage specific config. (A stage is a deploy environment, such as _production_ or _staging_.
- `lib/capistrano/tasks` is where you can add additional rake tasks to be ran by Capistrano at deploy time. We'll keep this empty for now, as everything required is included by our gems.

We'll only setup a _production_ deploy, so I won't bother with the separate config files and keep them all commented out. Note that it's necessary to keep those files, or Capistrano will complain they are missing.

I won't go line by line here - you can refer to Capistrano's [documentation](http://capistranorb.com/documentation/getting-started/configuration/) for each property, but let me mention a few key ones.

```
server '174.138.4.110', port: 22, roles: [:web, :app, :db], primary: true
```
This line gives information about the server we want to deploy to. Adding a line adds a server to which Capistrano will deploy to. For example, you might have a different server for your database, in which case you'd have an addition server for the `:db` role.
`server` and `port` are the server info for ssh.
`roles` is the list of roles present on this server. Capistrano breaks down tasks into a notion of _roles_. You can read more on their [doc](http://capistranorb.com/documentation/getting-started/preparing-your-application/).
_You need to change the server's IP to your own. The port might be different to - but 22 is the default for ssh_.

```
set :repo_url,        'git@github.com:Jauny/blog.git'
set :application,     'blog'
set :user,            'deploy'
# set :branch,        :master
```

You'll also have to update this set of information to be yours. Capistrano requires the repo to be accessible somewhere, so that's what the `repo_url` is for.
The `application` is the name of your app. It will be used to build multiple paths, so choose something that makes sense and is not too hard to type.
`user` is the name of the user that will be used to ssh into your server to deploy. We'll later create that user into your server. Each user has its own home directory, so this will influence the paths too. `deploy` seems to be a pretty common practice.
Your app will end up being deployed at `/home/<user>/var/www/<application>/`.

`set :branch` is commented out because `:master` is the default. Update this line if you want to deploy a different branch.

The following rules are pretty standard. You'll notice `:deploy_to` which sets the path where to deploy your app, using `:user` and `:application` as mentioned.

`shared_path` is mentioned but not being explicitely set, so it is worth mentioning. It is `/home/<user>/var/www/<application>/shared/`. This folder is not mutated during deploys, so it hosts files that are shared between versions, secrets ignored from source control, etc.
Likewise, `release_path` represents the path of the version of your app currently running. It lives at `/home/<users>/var/www/<application>/current/`.

```
set :linked_files, %w{config/secrets.yml.key}
```
Here is a good example of the _shared_ directoy. `linked_files` will be symlinked from the shared folder of the application into each release directory during deployment. So here, I'm telling Capistrano to symlink `/home/<users>/var/www/<application>/shared/config/secrets.yml.key` into `/home/<users>/var/www/<application>/<release>/config/secrets.yml.key`. That allows us to ignore the secrets key file from source control but still have it added during deploys.

### Setup Rails
At this point, you might have a few things to update in your Rails app, but it shouldn't be anything major.
In my example I use sqlite in production. Sqlite works as a file and right now its location is set inside my app at `db/production.sqlite3`. So new deploy would override that so I need to move it to the shared folder.
Now that I have Capistrano setup, I know the path of my shared folder and can update my database.yml.

```
production:
  <<: *default
  database: /home/deploy/var/www/blog/shared/production.sqlite3
```

Now that we have this done, Capistrano is ready to run. But it'll fail, since our server is not ready to receive our app yet.

## Step 2: Setup our server access
The root user has too much access and it is very risky to use it for everyday tasks, both manual and automated. Let's setup a user called `deploy` that we'll for everything.

First, create the user and add it to the `sudo` group, so it gets the same access

```
adduser deploy
usermod -aG sudo deploy
```

Now we need to add the ssh key the user will be ssh'ing from (right now your local machine). Let's make sure the folder and files needed to host the ssh key exist and have the correct access

```
mkdir ~/.ssh && chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
```

`~/.ssh/autorized_keys` is the file that stores keys for ssh access. Copy the content of the `~/.ssh/id_rsa.pub` from your local machine into that file.

You now should be able to ssh into your server with the deploy user. I recommend now only using the deploy user instead of root to ssh into the box.


## Step 3: Setup our server
### Install languages
Install Ruby

```
sudo apt-get ruby
sudo apt-get build-essential
sudo apt-get install -y libssl-dev libreadline-dev zlib1g-dev
```

Then install rbenv and setup ruby 2.4

```
cd
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
exec $SHELL

git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
exec $SHELL

rbenv install 2.4.3
rbenv global 2.4.3
```

And finally, install Bundler (we'll need it to install other dependencies)

```
gem install bundler
rbenv rehash
```

### Install SQLite
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### Install nginx
```
sudo apt-get install nginx
```

We then need to update the server's firewall (`ufw`) to allow access to nginx (port 80). Let's first check the firewall status

```
$ sudo ufw status

Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx HTTP                 ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
Nginx HTTP (v6)            ALLOW       Anywhere (v6)
```

Your firewall might not be active. In which case, enable it with `sudo ufw enable`. Now you want to allow access to nginx with `sudo ufw allow 'Ngnix HTTP'`.
⚠️ Be careful! Enabling the firewall might also block ssh access - make sure 'OpenSSH' is allowed. If not, you can allow it with `sudo ufw allow 'OpenSSH'`.

If nginx was installed, started and made accessible properly, you should be able to see an Nginx page when accessing your server at `http://<your-server-ip>`.

Now that nginx is running, let's set it up for our incoming app.
Nginx uses config files founds in `/etc/nginx/sites-enabled`. Files found there are usually symlinked from `/etc/nginx/sites-available`. In our case, I put the nginx config file inside the app's folder and symlinked it from there, so it's present in the diff I linked and in my main repository. The config is very standard for a rails app with puma. You can copy paste it from [here](https://github.com/Jauny/blog/blob/92ea1bbb3cde4988aae8ab508b8086cff24bf3a5/config/nginx.conf).

I want to point out that I changed the location of the logs.
By default, nginx logs are located into the `/var/log/nginx/` folder (`/var/log/` is a standard). You can find and change the default location of the logs in `/etc/nginx/nginx.conf`. For our app, I want to centralize all our logs into our app's logs folder at `/home/deploy/var/www/blog/current/log/`, so you'll see that I've changed the log locations inside our app's nginx conf.

This brings one issue. The user used by nginx (`www-data` by default) will not have access to the log files to write to them. We need to add it to the deploy group.

```
usermod -aG deploy www-data
```

Lastly we need to add our config to `sites-avaiable` and restart nginx to load the config.

```
ls ln /home/deploy/var/www/blog/current/config/nginx.conf /etc/nginx/sites-enabled/
service nginx restart
```

### Add required environment variables
For now we only need the `SECRET_KEY_BASE`. To add a variable accessible to all shells (login, non-login, interactive or not), you can add it to your `/etc/environment` file.

```
SECRET_KEY_BASE=<your app secret key>
```

## Step 4: Setup Puma
With the `capistrano-puma` gem, we simply have to write some configs and it will be automatically be started at deploy time by Capistrano.

The gem gives us 2 choices for the config. We can either add the config directly into the capistrano configuration (`blog/config/deploy.rb`) or set a regular puma config file in our shared folder (`/home/deploy/var/www/blog/shared/config/puma.rb`). The former is very convenient but I'll demonstrate the later, for more transparency how puma works. Note that if Capistrano finds a puma config, it will ignore any other puma-related configs (so you can ignore those in my own deploy.rb, they need to be removed!).

You can find my puma config here. You'll need to copy it into `/home/deploy/var/www/blog/shared/config/puma.rb`. Each line is self explanatory and comments should help.

One thing to notice is the `bind` config, which is the location of Puma's socket. This is where Nginx is configured to send traffic, so this has to match what is in Nginx' config.
I also have some cluster-only config - it is ignored right now, but good to keep in case Puma ends up running in cluster mode.

Last thing we need is to have Puma restart automatically in case the server reboots or crashes. We'll use Ubuntu 16 new `systemd` process manager.

Add a systemd config file for Puma

```
[Unit]
Description=Puma Rails Server
After=network.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/home/deploy/var/www/blog/current
ExecStart=/home/deploy/.rbenv/bin/rbenv exec bundle exec puma -C /home/deploy/var/www/blog/shared/config/puma.rb
ExecStop=/home/deploy/.rbenv/bin/rbenv exec bundle exec pumactl -S /home/deploy/var/www/blog/shared/tmp/pids/puma.state stop
TimeoutSec=15
Restart=always

[Install]
WantedBy=multi-user.target
```

And enable the service with `systemctl enable puma`.

### We now have a working Rails 5 app with Puma and NGINX on Ubuntu 16, deployed by capistrano
Let's review what we did!

We got our app ready by adding Capistrano to it (gems and config), then we created a VPS with a deploy user and nginx, and finally added some Puma config to set it up to work in production!

Hope this helped!
