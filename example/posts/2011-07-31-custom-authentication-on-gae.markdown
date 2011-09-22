---
title: Custom Authentication for Google App Engine apps
layout: post
time: '17:45'
---

![Google App Engine](http://upload.wikimedia.org/wikipedia/en/3/38/Google_App_Engine_Logo.png)

<!--begin excerpt-->
[Google App Engine](http://code.google.com/appengine) is a widely used and most popular [PaaS](en.wikipedia.org/wiki/Platform_as_a_service) solution provided by Google. App Engine provides the developer with a wide range of apis which can be used to develop web applications using any [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) compliant Frameworks ([Webapp](http://code.google.com/appengine/docs/python/tools/webapp/), [Tipfy](http://www.tipfy.org), [Django](http://www.django.org), [Bottle](http://bottlepy.org), [Tornado](http://www.tornadoweb.org) etc.).
<!--end excerpt-->
One of the apis App Engine provides is the [users api](http://code.google.com/appengine/docs/python/users/overview.html), which most of the developers confuses for an api which provides user creation, authentication for the application. But this api only authenticates Google Accounts (can be the application developer or any third-party Google Account) using [OAuth](http://oauth.net/). You can't really user this api to create or manage users for your application.

Remember when I told you that every application you write for GAE is a WSGI Application? WSGI is just a standard for the web application to talk to the backend HTTP server. That means a WSGI application can't run by itself. It needs an HTTP server to listen on and execute the code you have written. Its the HTTP Server which handles all the server stuffs used for authentication such as setting cookies. Now, GAE has a [sandbox](code.google.com/appengine/docs/python/runtime.html), which is a restrictive environment for your application code to run. For example, your application is restricted for file operations and certain modules are restricted from importing. So you can't really set up a cookie from your application code since its not an HTTP Server code. Here is our problem now. How do you do a custom authentication for a Google App Engine application?

You can achieve this by writing a middleware to your WSGI application. There are many authentication libraries available for this purpose. Popular ones are [Beaker](http://beaker.groovie.org/), [GAE-Sessions](https://github.com/dound/gae-sessions), [gaeutilities](http://gaeutilities.appspot.com/session). But I liked the GAE-Sessions library better than the other ones since its the [fastest](https://github.com/dound/gae-sessions/wiki/comparison-with-alternative-libraries) of them all. GAE-Sessions use [memcache](code.google.com/appengine/docs/memcache/)/[datastore](code.google.com/appengine/docs/datastore/) to store the session information. To use this library, just copy the gaesessions directory to your application directory. The middleware for your application is as simple as shown in the code below

{% highlight python %}
from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="a random and long string")
    return app
{% endhighlight %}

Save the above code to a file named `appengine_config.py`. You can use `gaesessions.get_current_session()` to get a dictionary to store all the session information. You can either use `session.set_quick(<session-var>, <value>)` method to use application memcache for storing session info. Otherwise it'll be stored to the datastore. Getting session info is as easy as `session.get(<session-var>)` and `session.pop_quick(<session-var>)` will remove the information from the session. All the dictionary like indexed operations will be persisted to the database.

{% highlight python %}
from gaesessions import get_current_session
session = get_current_session()

# setting user session information
session.set_quick('user', 'authenticated_user_info')
# getting user session
user = session.get('user')
# removing session info
session.pop_quick('user')
{% endhighlight %}

The default session lifetime is 7 days. You may configure how long a session lasts by calling `SessionMiddleware` with a `lifetime` parameter, e.g., `lifetime=datetime.timedelta(hours=2)`). You can schedule a cron job for cleaning up all the expired session info for your application by creating a handler file like this.

{% highlight python %}
# cleanup_sessions.py
from gaesessions import delete_expired_sessions
while not delete_expired_sessions():
    pass
{% endhighlight %}

Make sure you have a `cron.yaml` with the correct info.

{% highlight yaml %}
cron:
- description: daily session cleanup
  url: /cleanup_sessions
  schedule: every 24 hours
{% endhighlight %}

You can find a complete sample application [here](https://github.com/dound/gae-sessions/blob/master/demo).