---
title: Managing Configs and Secrets
date: 2018-03-04
layout: post
---
Although this post will use Flask for examples, this applies pretty much to any environment.

## Why do you need a config?
### Configs allow you to keep things DRY

One of the most known concepts in software engineering is to keep things DRY (Don't Repeat Yourself) and a project level config is a common pattern to handle this.

For example, instead of hardcoding the timeout delay when calling 'some_api', you store it _once_ in your project's config and load it from there.  
This way, when you need to change the timeout, you only change it once.

### Separate dev/prod/test environments

Another problem we face while building and maintaining software, is environment awareness. A lot of things end up working differently between development, testing and production.  

Having an environment-aware config system will allow you to build a software that is basically environment-agnostic and make development and maintenance easier.

### Keep your secrets, secret

Lastly, almost all projects today are using some third party APIs. Be it to load a twitter feed, offer facebook login or sending your logs to an analytics platform (you use logging extensively, right?).  

For each API, you'll have a secret key. This key needs to be kept out of source control and explicitely be a secrets to your engineers don't share it by mistake, but still be accessible throughout your code.

## So how do you handle this mess?

There are a lot of ways to handle this, and looking around for answer is kind of a mess, so I'll show how I do it most of the time.  
There are simpler and more complex ways - this one works for most small- to medium-size projects and is a good inbetween.  

### The config module

The most convenient way to handle all this mess is to create a config class for your project, and handle all the logic in there.  
Load this module when your application starts and make it accessible across your app.

So first, let's build a basic config class which will allow us to load our project level config (for now we ignore environments and secrets).

```python
class Config(dict):
	def __init__(self):
		self['SOME_API_TIMEOUT'] = 3000
		self['CONTACT_PHONE_NUMBER'] = '555-555-5555'
		self['ANOTHER_ONE'] = 'foobar'
```
Here we have a Config class that when initiated will behave like a dictionnary and offer access to mappings for our base config.  
It could be a simple mapping at this point, but using a class allows us to handle the required business logic that is coming.

### Handling different environments
Now we can add multiple subclasses to handle different configs for different environment.  

```python
class DevConfig(Config):
	def __init__(self):
		super(DevConfig, self).__init__()
		self['REDIS_ADDRESS'] = 'localhost:4545'
		self['LOG_LEVEL'] = 'DEBUG'
		
class ProdConfig(Config):
	def __init__(self):
		super(DevConfig, self).__init__()
		self['REDIS_ADDRESS'] = 'https://myapp.someredishost.com/redis'
		self['LOG_LEVEL'] = 'WARNING'
```
We now have 2 additional classes, one for our development environment and one for our production environment. They both inherit from the base Config class, so when we init either `DevConfig` or `ProdConfig` they both get the basic config, but each has a different uri to access our redis instance. We also log at a different level depending on the environment.

### Keep your secrets safe w/ dotenv
So this file with the config object is not secret. We only used it for publicly available config variables and it's all going into source control.  

We need to store our secrets in a place that won't go into source control, but will be loaded by this file.  
A nice pattern that is shared between almost all popular web frameworks (flask, node, rails, etc) is to use a `.env` file and parse it into your config file.  
Most languages have a nice "dotenv" lib that allows to easily parse the file.  

Let's create a `.env` file, that we'll make sure to add to our `.gitignore`.

```python
SECRET_KEY='abcabcdef'
API_SECRET='ohmygodkeepitforyourself'
```

Let's load it into our config now:

```python
import os
from dotenv import load_dotenv

class DevConfig(Config):
	def __init__(self):
		super(DevConfig, self).__init__()
		self['REDIS_ADDRESS'] = 'https://myapp.someredishost.com/redis'
		self['LOG_LEVEL'] = 'WARNING'
		
		load_dotenv('.env')
		for k, v in os.environ.iteritems():
			self[k] = v
```
As you see, we use `dotenv.load_dotenv` to load our `.env` file. In this case `load_dotenv` loads all the file directly into our environment variables (`os.environ`), so we then iterate over those to load them into our config object.  

But wait. If this file is out of source control, how do people get it? Well, they don't, that's the point. Your engineers will have to manually create this file, and pushing to prod will NOT add this file, so you'll need another (manual) way to add new values into your prod systems.  
This file is only used when your app runs locally, and that is why we only loaded the `.env` file into `DevConfig`.

To load secrets in production, it is a case by case basis, depending on how your manage your app in prod.  
For example, Heroku (and most hosting SaaS) allow you to add environment variables through their UI and CLI, so you can iterate over those and add them to your config from your `ProdConfig`.

```python
class ProdConfig(Config):
	def __init__(self):
		super(DevConfig, self).__init__()
		self['REDIS_ADDRESS'] = 'https://myapp.someredishost.com/redis'
		self['LOG_LEVEL'] = 'WARNING'
		
		for k, v in os.environ.iteritems():
			self[k] = v
```
This way, when your app loads in production, it will add all available env variables into the app's config.

And finally, we need to load this config module when the app starts.

```python
# app/__init__.py
from app.config import DevConfig, ProdConfig
if os.environ.get('ENVIRONMENT') is 'PRODUCTION':
	config = ProdConfig()
else:
	config = DevConfig()
	
app.config = config
```

This is obviously a very light implementation that will work for small- and mid-size projects.  
The next step is often to create a `config/` directory with different config files for each environment. For example `local.yaml`, `production.yaml`, etc. and parse those files, instead of having config data directly inside your classes. But I find most projects's config small enough that you can keep things clean and maintainable despite being directly into the class.
